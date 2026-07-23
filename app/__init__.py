from flask import Flask
from config import Config
from app.database import db
from app.advice_routes import advice_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    app.register_blueprint(advice_bp)
    
    # import models so that SQLAlchemy knows about them
    from app import models
    return app