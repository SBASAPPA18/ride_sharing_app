from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from .models import RideStatus

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    phone_number: str
    is_driver: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class RideBase(BaseModel):
    pickup_location: str
    dropoff_location: str
    pickup_latitude: float
    pickup_longitude: float
    dropoff_latitude: float
    dropoff_longitude: float

class RideCreate(RideBase):
    pass

class Ride(RideBase):
    id: int
    status: RideStatus
    created_at: datetime
    updated_at: Optional[datetime]
    passenger_id: int
    driver_id: Optional[int]

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    amount: float
    payment_method: str

class PaymentCreate(PaymentBase):
    ride_id: int

class Payment(PaymentBase):
    id: int
    status: str
    created_at: datetime
    ride_id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
