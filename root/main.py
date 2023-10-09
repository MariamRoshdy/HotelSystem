from fastapi import FastAPI
from database import engine
from api.v1.user.user import api_router as user_router
from api.v1.room.room import api_router as room_router
from api.v1.reservation.reservation import api_router as reservation_router

import models

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(user_router)
app.include_router(room_router)
app.include_router(reservation_router)
