from pydantic import BaseModel, Field
from typing import Optional


class UpdateReview(BaseModel):
    taste: Optional[float] = None
    price_to_quality: Optional[float] = None
    hygiene: Optional[float] = None
    service: Optional[float] = None
    description: Optional[str] = None
