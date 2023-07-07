from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    mobile = db.Column(db.String(30))
    email = db.Column(db.String(80))
    pickup = db.Column(db.String(160))
    drop = db.Column(db.String(160))
    date = db.Column(db.Date)
    time = db.Column(db.Time)
    vehicle = db.Column(db.String(80))

    def __init__(self, name, mobile, email, pickup, drop, date, time, vehicle):
        self.name = name
        self.mobile = mobile
        self.email = email
        self.pickup = pickup
        self.drop = drop
        self.date = date
        self.time = time
        self.vehicle = vehicle
