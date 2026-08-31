from sqlalchemy.orm import Session

from . import models
from . import schemas

#-----------------
# users
#-----------------

def create_user(db: Session, user: schemas.UserCreate):
    existing = (
        db.query(models.User)
        .filter(models.User.username == user.username)
        .first()
    )

    if existing:
        return existing

    db_user = models.User(username=user.username)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(models.User).all()

#------------------
#Messages
#--------------------

def create_message(db: Session, message: schemas.MessageCreate):
    existing = (
        db.query(models.Message)
        .filter(
            models.Message.sender_id == message.sender_id,
            models.Message.client_id == message.client_id
        )
        .first()
    )

    if existing:
        return {
            "id": existing.id,
            "client_id": existing.client_id,
            "sender_id": existing.sender_id,
            "sender": existing.sender.username,
            "content": existing.content,
            "timestamp": existing.timestamp
        }

    db_message = models.Message(
        client_id=message.client_id,
        sender_id=message.sender_id,
        content=message.content,
    )

    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return {
        "id": db_message.id,
        "client_id": db_message.client_id,
        "sender_id": db_message.sender_id,
        "sender": db_message.sender.username,
        "content": db_message.content,
        "timestamp": db_message.timestamp
    }


def get_messages(db: Session):
    messages = (
        db.query(models.Message)
        .order_by(models.Message.timestamp)
        .all()
    )

    return [
        {
            "id": m.id,
            "client_id": m.client_id,
            "sender_id": m.sender_id,
            "sender": m.sender.username,
            "content": m.content,
            "timestamp": m.timestamp
        }
        for m in messages
    ]
