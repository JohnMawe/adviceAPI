from datetime import datetime, timezone
from app.database import db

class Advice(db.Model):
    __tablename__ = "advice"
    advice_id = db.Column(db.Integer, primary_key=True)
    advice = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    author_id = db.Column(db.Integer, db.ForeignKey("author.author_id"))
    author = db.relationship("Author", back_populates="advices")
    
    def __str__(self):
        return f"Advice: {self.advice_id}: {self.advice}"

class Author(db.Model):
    __tablename__ = "author"
    author_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    second_name = db.Column(db.Text, nullable=False)
    date_joined = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    advices = db.relationship("Advice", back_populates="author")

    def __str__(self):
        return f"Author {self.first_name} {self.second_name}"
