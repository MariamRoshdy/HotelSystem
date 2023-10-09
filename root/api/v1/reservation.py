from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter
api_router = APIRouter(prefix='/Reservation', tags=['Reservation module'])


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")




@api_router.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

# @api_router.post("/")
# def make_reservation(reservation: pydantic_reservation, db: Session = Depends(get_db)):
#      #user = get_
