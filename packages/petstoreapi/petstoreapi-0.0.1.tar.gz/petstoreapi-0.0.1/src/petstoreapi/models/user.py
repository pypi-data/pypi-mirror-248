from uuid import UUID
from pydantic import BaseModel
from typing import List


class User(BaseModel):
    uuid: UUID | None = None
    first_name: str
    last_name: str
    avatar_image_name: str | None = None
    username: str
    email: str | None = None
    pets: List[UUID] = []
