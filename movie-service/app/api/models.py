#~/movie-service/api/models.py

from typing import List
from pydantic import BaseModel

class Movie(BaseModel):
    name: str
    plot: str
    genres: List[str]
    casts: List[str]