from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import select
from sqlalchemy.orm import Session

from core.utils import get_db
from database import models
from schemas import user as user_schema
from core import security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )

    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(email=username, db=db)
    if user is None:
        raise credentials_exception
    return user


def authenticate_user(email: str, password: str, db: Session):
    user = get_user_by_email(email=email, db=db)
    print(user)
    if not user:
        return False
    if password != user.password:
        return False
    return user


def add_user(db: Session, user: user_schema.User):
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
