from sqla_wrapper import SQLAlchemy
import os
db = SQLAlchemy(os.getenv("DATABASE_URL", "sqlite:///podatkovna-baza.sqlite"))

class Komentar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avtor = db.Column(db.String)
    vsebina = db.Column(db.String)


class Uporabnik(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column (db.String)
    geslo = db.Column(db.String)
    sejna_vrednost = db.Column(db.String)
