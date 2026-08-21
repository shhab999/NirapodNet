from sqlalchemy.orm import Session

from . import models
from . import schemas

# users

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

#Messages

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(
        sender_id=message.sender_id,
        content=message.content
    )

    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return {
        "id": db_message.id,
        "sender_id": db_message.sender.id,
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
            "sender_id": m.sender.id,
            "sender": m.sender.username,
            "content": m.content,
            "timestamp": m.timestamp
        }
        for m in messages
    ]
