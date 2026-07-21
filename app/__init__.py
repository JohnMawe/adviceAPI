from flask import Flask
from config import Config
from app.database import db
from app.routes import advice_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(advice_bp)
    
    # import models so that SQLAlchemy knows about them
    from app import models
    return app