from typing import Optional

from pydantic import BaseModel
class Book(BaseModel):
    title: str
    year: int
    rating: Optional[float]

Book(title="Dune", year=1965)  # no rating passed