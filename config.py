import os

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///advice.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False