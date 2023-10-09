from pydantic import BaseModel
from datetime import date


class Reservation(BaseModel):
    room_type: str
    start_date: date
    End_date: date
