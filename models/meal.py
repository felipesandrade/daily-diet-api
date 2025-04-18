from database import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_name = db.Column(db.String(80), nullable=False)
    meal_description = db.Column(db.String(255), nullable=False)
    meal_date_time = db.Column(db.DateTime, nullable=False)
    meal_on_diet = db.Column(db.Boolean, nullable=False, default=False)
