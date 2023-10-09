from sqlalchemy import update
from sqlalchemy.orm import Session
from database import models
from schemas import room as room_schema


def update_room(db: Session, room_type: room_schema.RoomType): # not workiing
    room = get_room_by_type(db, room_type)
    if room_type.price is not None:
        update(room).values(price=room_type.price)
    db.commit()
    db.refresh(room)
    return room


def get_room_by_type(db: Session, type: str):
    return db.query(models.RoomTypes).filter(models.RoomTypes.type == type).first()


def add_room_type(db: Session, room_type: room_schema.RoomType):
    db_room = models.RoomTypes(type=room_type.type, description=room_type.description
                               , capacity=room_type.capacity, price=room_type.price)
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def list_room_types(db: Session):
    return db.query(models.RoomTypes).all()
