from flask import Flask
from config import Config
from app.database import db
from app.advice_routes import advice_bp
from app.author_routes import author_bp
from app.webui_routes import webui_bp

def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder="../UI/webui/templates",
        static_folder="../UI/webui/static"
    )
    app.config.from_object(config_class)
    db.init_app(app)
    app.register_blueprint(advice_bp)
    app.register_blueprint(author_bp)
    app.register_blueprint(webui_bp)
    
    # import models so that SQLAlchemy knows about them
    from app import models
    return app
    