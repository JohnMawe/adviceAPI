from app import create_app
from app.database import db


app = create_app()

# set application contex for for SQLAlchemy to know how to create sql tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])