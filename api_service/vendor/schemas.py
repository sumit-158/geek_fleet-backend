from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RequestVendor(BaseModel):
    vendor_name: str = Field(..., example="Hunge&Hpoe")
    location: str = Field(..., example="Patna")
    description: str = Field(..., example="something")
    morning_timing: float = Field(..., example=8.30)
    evening_timing: float = Field(..., example=7.30)


class RequestReview(BaseModel):
    taste: float
    price_to_quality: float
    hygiene: float
    service: float


class VendorList(BaseModel):
    vendor_id: str
    vendor_name: str = Field(..., example="Hunge&Hpoe")
    location: str = Field(..., example="Patna")
    description: str = Field(..., example="something")
    morning_timing: float = Field(..., example=8.30)
    evening_timing: float = Field(..., example=7.30)
    created_by: str
    last_updated_by: str
    created_on: datetime
    status: str


class UpdateVendor(BaseModel):
    vendor_name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    morning_timing: Optional[float] = None
    evening_timing: Optional[float] = None
