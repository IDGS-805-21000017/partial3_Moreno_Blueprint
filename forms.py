from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', 
        validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class AlumnoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apaterno = StringField('Apellido Paterno', validators=[DataRequired()])
    amaterno = StringField('Apellido Materno', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de Nacimiento', validators=[DataRequired()])
    grupo = StringField('Grupo', validators=[DataRequired()])
    submit = SubmitField('Registrar')