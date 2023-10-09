from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
from users import schemas


def add_user(db: Session, user: schemas.User):
    db_user = models.User(email=user.email
                          , user_name=user.user_name, password=user.password,
                          is_superuser=user.is_superuser)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def del_user(db: Session, id: int):
    user = db.query(models.User).get(id)
    if not user:
        raise HTTPException(status_code=400, detail="User doesn't Exist")
    user_name = user.user_name
    db.delete(user)
    db.commit()
    return {user_name + "is deleted"}


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def show_users(db: Session):
    return db.execute(select(models.User.user_name, models.User.email))
