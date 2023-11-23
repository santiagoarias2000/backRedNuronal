from pydantic import BaseModel
from typing import Optional


class Movies(BaseModel):
    id: int
    name: str
    gender: str
    image: Optional[str]


class MoviesId(BaseModel):
    id: int
