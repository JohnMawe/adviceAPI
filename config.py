import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///advice.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
