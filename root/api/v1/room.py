from fastapi import Depends, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session
from core.utils import get_db
from schemas import room as room_schema
from crud import room as room_crud

api_router = APIRouter(prefix='/room', tags=['Room module'])


@api_router.post("/")
def add_room(room: room_schema.RoomType, db: Session = Depends(get_db)):
    db_room = room_crud.get_room_by_type(db, room.type)
    if db_room:
        raise HTTPException(status_code=400, detail="Room type already exists")
    return room_crud.add_room_type(db=db, room_type=room)


# @api_router.put("/")   # not workiing
# def update_room(room: schemas.RoomType, db: Session = Depends(get_db)):
#     db_room = crud.get_room_by_type(db, room.type)
#     if not db_room:
#         raise HTTPException(status_code=400, detail="Room type doesn't exist")
#     return crud.update_room(db=db, room_type=room)


@api_router.get("/")
def show_rooms(db: Session = Depends(get_db)):
    return room_crud.list_room_types(db)
