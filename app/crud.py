from sqlalchemy.orm import Session

from . import models
from . import schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(db: Session):
    return db.query(models.User).all()


def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(
        sender_id=message.sender_id,
        content=message.content
    )

    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message


def get_messages(db: Session):
    return (
        db.query(models.Message)
        .order_by(models.Message.timestamp)
        .all()
    )