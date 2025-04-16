from database import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    on_diet = db.Column(db.Boolean, nullable=False, default=False)
