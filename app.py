from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from config import DevelopmentConfig
from models import db, User, Alumno
from blueprints.auth.routes import auth
from blueprints.maestros.routes import maestros
from blueprints.alumnos.routes import alumnos

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    # Intentar cargar un usuario normal
    user = db.session.get(User, int(user_id))
    if user:
        return user
    # Si no es un usuario normal, intentar cargar un alumno
    return db.session.get(Alumno, int(user_id))

# Register blueprints
app.register_blueprint(auth, url_prefix='/login')
app.register_blueprint(maestros, url_prefix='/maestros')
app.register_blueprint(alumnos, url_prefix='/alumnos')

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404

if __name__ == "__main__":
    with app.app_context():
        # Eliminar todas las tablas existentes
        db.drop_all()
        # Crear todas las tablas
        db.create_all()
        # Crear un usuario administrador por defecto
        admin = User(email='admin@example.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
    app.run(debug=True)