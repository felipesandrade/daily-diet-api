from database import db
from flask_login import UserMixin

class Meal(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    meal_name = db.Column(db.String(80), nullable=False)
    meal_description = db.Column(db.String(255), nullable=False)
    meal_date_time = db.Column(db.DateTime, nullable=False)
    meal_on_diet = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='meal')
