import pytest
from app import create_app
from app.database import db
from config import TestingConfig
from app.models import Advice, Author

@pytest.fixture
def client():
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()

        yield app.test_client()
    
        # cleans-up and rest the database for a fresh start in every test
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
