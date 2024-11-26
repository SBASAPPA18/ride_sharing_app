# Ride Sharing Application

A FastAPI-based ride sharing application with PostgreSQL backend, Docker containerization, and OAuth2 authentication.

## Features

- User Management (Passengers and Drivers)
- Ride Management (Create, Accept, Update Status)
- Payment Processing
- JWT-based Authentication
- OpenAPI Documentation
- Docker Containerization

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- PostgreSQL

## Project Structure

```
ride_sharing_app/
│
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic models
│   ├── crud.py         # Database operations
│   ├── database.py     # Database configuration
│   └── security.py     # Authentication and authorization
│
├── docker-compose.yml   # Docker compose configuration
├── Dockerfile          # FastAPI service dockerfile
└── requirements.txt    # Python dependencies
```

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ride_sharing_app
```

2. Build and run the containers:
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- OpenAPI documentation: `http://localhost:8000/docs`
- Alternative documentation: `http://localhost:8000/redoc`

## API Endpoints

### Authentication
- POST `/token` - Get access token

### Users
- POST `/users/` - Create new user
- GET `/users/me/` - Get current user
- GET `/users/` - List all users

### Rides
- POST `/rides/` - Create new ride
- GET `/rides/` - List all rides
- GET `/rides/{ride_id}` - Get specific ride
- POST `/rides/{ride_id}/accept` - Accept ride (drivers only)
- POST `/rides/{ride_id}/status/{status}` - Update ride status

### Payments
- POST `/payments/` - Create payment
- GET `/payments/{payment_id}` - Get payment details

## Security

The application implements:
- JWT token-based authentication
- Password hashing using bcrypt
- Role-based access control
- Secure database connection

## Development

To run the application in development mode:

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## Testing

To run tests:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request
