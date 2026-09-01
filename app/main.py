from pathlib import Path
from fastapi import FastAPI, Request, Depends, Query
from fastapi.responses import HTMLResponse
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status

from .auth import get_current_user

from .database import engine, get_db
from .models import Base
from . import schemas, crud

from fastapi import WebSocket, WebSocketDisconnect
from .websocket import manager
from .database import SessionLocal
from .models import (
    Base,
    User,
    Message,
    UserSession,
    SOSEvent,
    Broadcast,
    CheckIn,
)
BASE_DIR = Path(__file__).resolve().parent

security = HTTPBearer()

app = FastAPI(title="NirapodNet")

# Create SQLite tables on startup
Base.metadata.create_all(bind=engine)

# Static files
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")

# -----------------------
# HTML Pages
# -----------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# -----------------------
# System API
# -----------------------

@app.get("/api")
def api_status():
    return {
        "system": "NirapodNet",
        "status": "online"
    }


# -----------------------
# User API
# -----------------------

@app.post("/users", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return crud.create_user(db, user)


@app.post(
    "/api/register",
    response_model=schemas.UserResponse,
    status_code=201,
)
def register_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(User)
        .filter(User.username == user.username)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    return crud.create_user(db, user)


@app.post(
    "/api/login",
    response_model=schemas.LoginResponse,
)
def login_user(
    credentials: schemas.LoginRequest,
    db: Session = Depends(get_db),
):
    user = crud.authenticate_user(
        db,
        credentials.username,
        credentials.password,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    expires_at = (
        datetime.now(timezone.utc)
        + timedelta(hours=24)
    )

    session = crud.create_session(
        db,
        user_id=user.id,
        expires_at=expires_at,
    )

    return {
        "token": session.token,
        "user": user,
        "expires_at": session.expires_at,
    }


@app.post("/api/logout")
def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    crud.delete_session(db, token)

    return {
        "message": "Logged out successfully"
    }


@app.get(
    "/api/me",
    response_model=schemas.UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@app.get("/users", response_model=list[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


# -----------------------
# Message API
# -----------------------

@app.post("/messages", response_model=schemas.MessageResponse)
def create_message(
    message: schemas.MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message.sender_id = current_user.id

    return crud.create_message(db, message)


@app.get("/messages", response_model=list[schemas.MessageResponse])
def list_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    messages = (
        db.query(Message)
        .order_by(Message.timestamp.asc())
        .all()
    )

    return [
        {
            "id": message.id,
            "client_id": message.client_id,
            "sender_id": message.sender_id,
            "sender": message.sender.username,
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
        }
        for message in messages
    ]

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
):
    db = SessionLocal()

    try:
        user = crud.get_session_user(db, token)

        if user is None:
            await websocket.close(code=1008)
            return

        await manager.connect(
            websocket,
            user.id,
        )

        while True:
            data = await websocket.receive_json()

            client_id = data.get("client_id")
            content = data.get("content")

            if not client_id or not content:
                await websocket.send_json({
                    "type": "error",
                    "error": "Invalid message",
                })
                continue

            existing = (
                db.query(Message)
                .filter(
                    Message.sender_id == user.id,
                    Message.client_id == client_id,
                )
                .first()
            )

            if existing:
                await websocket.send_json({
                    "type": "ack",
                    "client_id": client_id,
                    "message_id": existing.id,
                    "sender_id": existing.sender_id,
                    "sender": existing.sender.username,
                    "content": existing.content,
                    "timestamp": existing.timestamp.isoformat(),
                })
                continue

            message = Message(
                client_id=client_id,
                sender_id=user.id,
                content=content,
            )

            db.add(message)
            db.commit()
            db.refresh(message)

            await websocket.send_json({
                "type": "ack",
                "client_id": client_id,
                "message_id": message.id,
                "sender_id": user.id,
                "sender": user.username,
                "content": content,
                "timestamp": message.timestamp.isoformat(),
            })

            await manager.broadcast(
                {
                    "type": "message",
                    "client_id": client_id,
                    "id": message.id,
                    "sender": user.username,
                    "sender_id": user.id,
                    "content": content,
                    "timestamp": message.timestamp.isoformat(),
                },
                exclude=websocket,
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    finally:
        db.close()