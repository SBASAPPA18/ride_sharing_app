from sqlalchemy.orm import Session
from . import models, schemas, security
from fastapi import HTTPException, status
from typing import List, Optional

# User operations
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        full_name=user.full_name,
        phone_number=user.phone_number,
        is_driver=user.is_driver
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# Ride operations
def create_ride(db: Session, ride: schemas.RideCreate, passenger_id: int):
    db_ride = models.Ride(
        **ride.dict(),
        passenger_id=passenger_id
    )
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    return db_ride

def get_ride(db: Session, ride_id: int):
    return db.query(models.Ride).filter(models.Ride.id == ride_id).first()

def get_rides(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ride).offset(skip).limit(limit).all()

def get_user_rides(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Ride).filter(
        (models.Ride.passenger_id == user_id) | (models.Ride.driver_id == user_id)
    ).offset(skip).limit(limit).all()

def update_ride_status(db: Session, ride_id: int, status: models.RideStatus):
    db_ride = get_ride(db, ride_id)
    if not db_ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    db_ride.status = status
    db.commit()
    db.refresh(db_ride)
    return db_ride

def assign_driver(db: Session, ride_id: int, driver_id: int):
    db_ride = get_ride(db, ride_id)
    if not db_ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    if db_ride.driver_id:
        raise HTTPException(status_code=400, detail="Ride already has a driver")
    db_ride.driver_id = driver_id
    db_ride.status = models.RideStatus.ACCEPTED
    db.commit()
    db.refresh(db_ride)
    return db_ride

# Payment operations
def create_payment(db: Session, payment: schemas.PaymentCreate):
    db_payment = models.Payment(**payment.dict(), status="pending")
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payment(db: Session, payment_id: int):
    return db.query(models.Payment).filter(models.Payment.id == payment_id).first()

def update_payment_status(db: Session, payment_id: int, status: str):
    db_payment = get_payment(db, payment_id)
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db_payment.status = status
    db.commit()
    db.refresh(db_payment)
    return db_payment
