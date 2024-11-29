from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    studios = db.Column(db.String(255), nullable=False)
    producers = db.Column(db.String(255), nullable=False)
    winner = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<Movie {self.title} ({self.year})>"
