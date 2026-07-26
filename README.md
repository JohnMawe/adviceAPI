# Advice Saver API

A simple RESTful API built with Flask, SQLAlchemy, and SQLite for storing and managing advice. This project demonstrates the fundamentals of backend API development, including CRUD operations, request validation, database integration, and automated testing with Pytest.

# Features

- Create a new advice
- Retrieve all advice
- Retrieve advice by ID
- Update existing advice
- Delete advice
- Input validation
- Consistent JSON responses
- Automated tests with Pytest

---

# Tech Stack

- Python 3.13
- Flask
- SQLAlchemy
- SQLite
- Pytest
- Coverage

---

# Project Structure
```bash
adviceAPI/
│
├── app/
│   ├── __init__.py          # Flask application factory
│   ├── advice_routes.py     # API endpoints
│   ├── database.py          # SQLAlchemy instance
│   ├── models.py            # Database models
│   ├── utility.py           # Helper functions
│   └── schemas.py           # Reserved for future request/response schemas
│
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   └── test_advice.py       # API tests
│
├── instance/
│   └── advice.db            # SQLite database
│
├── config.py                # Application configuration
├── run.py                   # Application entry point
├── Pipfile
├── Pipfile.lock
└── README.md
```

---

# Installation

Clone the repository:
```bash
git clone <repository-url>
cd adviceAPI
```

Install dependencies:
```bash
pipenv install
```

Activate the virtual environment:
```bash
pipenv shell
```

---

# Running the Application

Start the development server:

```bash
python run.py
```

The API will be available at:
```bash
http://127.0.0.1:5000
```

---

## API Endpoints

Method | Endpoint | Description
GET | "/" | API welcome message

GET | "/advice" | Retrieve all advice

GET | "/advice/<id>" | Retrieve advice by ID

POST | "/advice" | Create new advice

PUT | "/advice/<id>" | Update existing advice

DELETE | "/advice/<id>" | Delete advice

---

## Example Request:

### Create Advice

POST "/advice"

{

    "advice": "Always write tests before pushing to production."
}

## Example success response:

{

    "success": true,
    "message": "Advice saved successfuly",
    "data": {
        "advice_id": 1,
        "advice": "Always write tests before pushing to production."
    }
}

---

# Validation

The API validates incoming requests by ensuring:

- The request body is valid JSON.
- The "advice" field is present.
- The "advice" field is a string.
- The "advice" field is not empty.

Invalid requests return descriptive JSON error messages with the appropriate HTTP status code.

---

## Running Tests

Run all tests:
```bash
python -m pytest
```

Run tests with coverage:
```bash
python -m pytest --cov=app --cov-report=term-missing
```

---

# Learning Objectives

This project demonstrates:

- Flask application factory pattern
- Flask Blueprints
- SQLAlchemy ORM
- SQLite integration
- REST API design
- CRUD operations
- Request validation
- JSON responses
- HTTP status codes
- Automated API testing with Pytest
- Code coverage analysis

---

# Future Improvements

- Use Pydantic schemas for validation
- Add pagination for listing advice
- Add filtering and search
- Add OpenAPI/Swagger documentation
- Replace "db.create_all()" with Flask-Migrate

---

# License

This project is intended for learning and educational purposes.