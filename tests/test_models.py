import pytest
from app.models import User, Ride  # Adjust imports based on your actual models

def test_user_model_creation():
    """
    Test the basic creation of a User model
    """
    user = User(
        username="testuser", 
        email="test@example.com", 
        hashed_password="hashedpassword"
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"

def test_ride_model_creation():
    """
    Test the basic creation of a Ride model
    """
    ride = Ride(
        driver_id=1, 
        passenger_id=2, 
        start_location="Test Start", 
        end_location="Test End"
    )
    assert ride.start_location == "Test Start"
    assert ride.end_location == "Test End"