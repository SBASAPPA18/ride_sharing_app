from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from . import crud, models, schemas, security
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Ride Sharing API",
    description="A FastAPI-based ride sharing application with PostgreSQL backend",
    version="1.0.0"
)

# Authentication endpoints
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# User endpoints
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(
    current_user: models.User = Depends(security.get_current_active_user)
):
    return current_user

@app.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

# Ride endpoints
@app.post("/rides/", response_model=schemas.Ride)
def create_ride(
    ride: schemas.RideCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    return crud.create_ride(db=db, ride=ride, passenger_id=current_user.id)

@app.get("/rides/", response_model=List[schemas.Ride])
def read_rides(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    rides = crud.get_rides(db, skip=skip, limit=limit)
    return rides

@app.get("/rides/{ride_id}", response_model=schemas.Ride)
def read_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    ride = crud.get_ride(db, ride_id=ride_id)
    if ride is None:
        raise HTTPException(status_code=404, detail="Ride not found")
    return ride

@app.post("/rides/{ride_id}/accept")
def accept_ride(
    ride_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    if not current_user.is_driver:
        raise HTTPException(status_code=400, detail="User is not a driver")
    return crud.assign_driver(db=db, ride_id=ride_id, driver_id=current_user.id)

@app.post("/rides/{ride_id}/status/{status}")
def update_ride_status(
    ride_id: int,
    status: models.RideStatus,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    ride = crud.get_ride(db, ride_id=ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    if ride.driver_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this ride")
    return crud.update_ride_status(db=db, ride_id=ride_id, status=status)

# Payment endpoints
@app.post("/payments/", response_model=schemas.Payment)
def create_payment(
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    return crud.create_payment(db=db, payment=payment)

@app.get("/payments/{payment_id}", response_model=schemas.Payment)
def read_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    payment = crud.get_payment(db, payment_id=payment_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment
