from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from common.utils import get_db
from users import schemas as user_schemas
from users import crud as user_crud
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

api_router = APIRouter(prefix='/user', tags=['User module'])




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
