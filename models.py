from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class Clients(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(3000))
    name = db.Column(db.String(1000))
    is_admin = db.Column(db.String(1000))


class Fields(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.Integer)
    name_prize = db.Column(db.String(3000))
    location_ship = db.Column(db.String(3000))
    hits_client = db.Column(db.String(3000))


class Prizes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(3000))
    file = db.Column(db.String(3000))
    description = db.Column(db.String(3000))


class FieldsAndClients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer)
    id_field = db.Column(db.Integer)
    numbers_hits = db.Column(db.Integer)


class ClientAndPrizes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_client = db.Column(db.Integer)
    prizes = db.Column(db.String(3000))
