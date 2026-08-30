from email.mime import message

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import engine, get_db
from .models import Base
from . import schemas, crud

from fastapi import WebSocket, WebSocketDisconnect
from .websocket import manager
from .database import SessionLocal
from .models import Message, User

app = FastAPI(title="NirapodNet")

# Create SQLite tables on startup
Base.metadata.create_all(bind=engine)

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# HTML templates
templates = Jinja2Templates(directory="app/templates")


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


@app.get("/users", response_model=list[schemas.UserResponse])
def list_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


# -----------------------
# Message API
# -----------------------

@app.post("/messages", response_model=schemas.MessageResponse)
def create_message(
    message: schemas.MessageCreate,
    db: Session = Depends(get_db)
):
    return crud.create_message(db, message)


@app.get("/messages", response_model=list[schemas.MessageResponse])
def list_messages(db: Session = Depends(get_db)):

    messages = (
        db.query(Message)
        .order_by(Message.timestamp.desc())
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
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    db = SessionLocal()

    try:
        while True:
            data = await websocket.receive_json()

            client_id = data.get("client_id")
            content = data.get("content")
            sender_id = data.get("sender_id")

            if not client_id or not content or not sender_id:
                await websocket.send_json({
                    "type": "error",
                    "error": "Invalid message"
                })
                continue

            sender = (
                db.query(User)
                .filter(User.id == sender_id)
                .first()
            )

            if sender is None:
                await websocket.send_json({
                    "type": "error",
                    "client_id": client_id,
                    "error": "Invalid sender"
                })
                continue
            
            existing = (
                db.query(Message)
                .filter(Message.client_id == client_id)
                .first()
            )

            if existing:
                await websocket.send_json({
                    "type": "ack",
                    "client_id": data.get("client_id"),
                    "message_id": existing.id,
                })
                continue

            message = Message(
                client_id=data["client_id"],
                sender_id=data["sender_id"],
                content=data["content"],
            )

            db.add(message)
            db.commit()
            db.refresh(message)

            await websocket.send_json({
                "type": "ack",
                "client_id": client_id,
                "message_id": message.id,
            })

            await manager.broadcast({
                "type": "message",
                "client_id": client_id,
                "id": message.id,
                "sender": sender.username,
                "sender_id": message.sender_id,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    finally:
        db.close()