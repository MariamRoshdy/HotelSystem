from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from core.utils import get_db
from users import schemas as user_schemas
from users import crud as user_crud
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated

api_router = APIRouter(prefix='/user', tags=['User module'])


@api_router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                db: Session = Depends(get_db)):
    user = user_crud.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if form_data.password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}



@api_router.post("/")
def register(user: user_schemas.User, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.add_user(db=db, user=user)


@api_router.get("/")
def get_users(db: Session = Depends(get_db)):
    return user_crud.show_users(db)


@api_router.delete("/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_crud.del_user(db, user_id)
