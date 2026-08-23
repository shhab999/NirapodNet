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
from .models import Message

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
    return crud.get_messages(db)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    db = SessionLocal()

    try:
        while True:
            data = await websocket.receive_json()

            message = Message(
                sender_id=data["sender_id"],
                content=data["content"]
            )

            db.add(message)
            db.commit()
            db.refresh(message)

            await manager.broadcast({
                "client_id": data.get("client_id"),
                "id": message.id,
                "sender": message.sender.username,
                "sender_id": message.sender.id,
                "content": message.content,
                "timestamp": message.timestamp.isoformat()
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    finally:
        db.close()