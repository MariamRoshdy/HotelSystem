from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from core.utils import get_db
from schemas import user as user_schemas
from crud import user as user_crud
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated
from core.security import create_access_token
from schemas.token import Token

api_router = APIRouter(prefix='/user', tags=['User module'])


@api_router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):
    user = user_crud.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@api_router.post("/")
async def register(user: user_schemas.User, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.add_user(db=db, user=user)


@api_router.get("/")
async def get_users(db: Session = Depends(get_db)):
    return user_crud.show_users(db)


@api_router.delete("/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return user_crud.del_user(db, user_id)
