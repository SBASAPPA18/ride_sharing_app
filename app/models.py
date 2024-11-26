from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class RideStatus(str, enum.Enum):
    REQUESTED = "requested"
    ACCEPTED = "accepted"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    phone_number = Column(String)
    is_active = Column(Boolean, default=True)
    is_driver = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    rides_as_driver = relationship("Ride", back_populates="driver", foreign_keys="Ride.driver_id")
    rides_as_passenger = relationship("Ride", back_populates="passenger", foreign_keys="Ride.passenger_id")

class Ride(Base):
    __tablename__ = "rides"

    id = Column(Integer, primary_key=True, index=True)
    pickup_location = Column(String)
    dropoff_location = Column(String)
    pickup_latitude = Column(Float)
    pickup_longitude = Column(Float)
    dropoff_latitude = Column(Float)
    dropoff_longitude = Column(Float)
    status = Column(Enum(RideStatus), default=RideStatus.REQUESTED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign Keys
    passenger_id = Column(Integer, ForeignKey("users.id"))
    driver_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    passenger = relationship("User", back_populates="rides_as_passenger", foreign_keys=[passenger_id])
    driver = relationship("User", back_populates="rides_as_driver", foreign_keys=[driver_id])
    payment = relationship("Payment", back_populates="ride", uselist=False)

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    status = Column(String)  # pending, completed, failed
    payment_method = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign Key
    ride_id = Column(Integer, ForeignKey("rides.id"))
    
    # Relationship
    ride = relationship("Ride", back_populates="payment")
