from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Alumno(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apaterno = db.Column(db.String(80), nullable=False)
    amaterno = db.Column(db.String(80), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    grupo = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Alumno {self.nombre} {self.apaterno}>"

class Pregunta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.String(255), nullable=False)
    respuesta_a = db.Column(db.String(255), nullable=False)
    respuesta_b = db.Column(db.String(255), nullable=False)
    respuesta_c = db.Column(db.String(255), nullable=False)
    respuesta_d = db.Column(db.String(255), nullable=False)
    respuesta_correcta = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Pregunta {self.pregunta}>"

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)