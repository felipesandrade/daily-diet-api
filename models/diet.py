from database import db

class Diet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)
    is_diet = db.Column(db.Boolean, nullable=False, default=False)
