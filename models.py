from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    vyska = db.Column(db.Float, nullable=False)  # Výška v metrech nebo cm (např. 1.75)
    vaha = db.Column(db.Float, nullable=False)   # Váha v kg (např. 70.5)

    def __repr__(self):
        return f"<Person {self.name}, {self.vyska}m, {self.vaha}kg>"
