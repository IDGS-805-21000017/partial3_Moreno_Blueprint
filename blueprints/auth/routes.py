from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Alumno, db
from forms import LoginForm, RegisterForm

auth = Blueprint('auth', __name__, template_folder='../../templates')

@auth.route('/')
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if isinstance(current_user, User):
            return redirect(url_for('maestros.inicio'))
        else:
            return redirect(url_for('alumnos.inicio'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        tipo_usuario = request.form.get('tipo_usuario')

        if not email or not password:
            flash('Por favor ingrese su correo y contraseña', 'danger')
            return redirect(url_for('auth.login'))

        if tipo_usuario == 'admin':
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('maestros.inicio'))
        else:
            alumno = Alumno.query.filter_by(email=email).first()
            if alumno and alumno.check_password(password):
                login_user(alumno)
                return redirect(url_for('alumnos.inicio'))

        flash('Correo o contraseña incorrectos', 'danger')
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('¡Registro exitoso!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))