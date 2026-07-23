from datetime import datetime, timezone
from app.database import db

class Advice(db.Model):
    __tablename__ = "advice"
    advice_id = db.Column(db.Integer, primary_key=True)
    advice = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    
    def __str__(self):
        return f"Advice: {advice_id}. {advice}"

# class Author(db.Model):
