from datetime import datetime
from app.database import db

class Advice(db.Model):
    __tablename__ = "advice"
    advice_id = db.Column(db.Integer, primary_key=True)
    advice = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
