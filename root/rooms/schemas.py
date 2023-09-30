from pydantic import BaseModel


class RoomType(BaseModel):
    type: str
    description: str | None = None
    capacity: int | None = None
    price: int | None = None