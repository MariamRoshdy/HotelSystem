from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_superuser = Column(Boolean)


class RoomTypes(Base):
    __tablename__ = "room_types"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(String, unique=True)
    description = Column(String)
    capacity = Column(Integer)
    price = Column(Integer)

    
class Reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_type = Column(String, ForeignKey("room_types.type"))
    total_rooms = Column(Integer)
    start_date = Column(Date)
    End_date = Column(Date)