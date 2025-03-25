# Sistema de Exámenes con Flask

Este proyecto implementa un sistema de exámenes utilizando Flask, con una arquitectura basada en blueprints y autenticación de usuarios.

## Estructura del Proyecto

```
├── app.py                 # Aplicación principal
├── config.py             # Configuración de la aplicación
├── models.py             # Modelos de la base de datos
├── blueprints/           # Módulos de la aplicación
│   ├── auth/            # Autenticación
│   ├── alumnos/         # Funcionalidad para alumnos
│   └── maestros/        # Funcionalidad para maestros
└── templates/           # Plantillas HTML
```

## Implementación de Blueprints

### 1. Configuración Principal (app.py)

```python
from flask import Flask
from blueprints.auth.routes import auth
from blueprints.maestros.routes import maestros
from blueprints.alumnos.routes import alumnos

app = Flask(__name__)

# Registro de blueprints
app.register_blueprint(auth, url_prefix='/login')
app.register_blueprint(maestros, url_prefix='/maestros')
app.register_blueprint(alumnos, url_prefix='/alumnos')
```

### 2. Estructura de Blueprints

Cada blueprint sigue una estructura similar:

```python
from flask import Blueprint, render_template

# Creación del blueprint
maestros = Blueprint('maestros', __name__, template_folder='../../templates')

# Rutas del blueprint
@maestros.route('/')
def inicio():
    return render_template('maestros/inicio.html')
```

## Sistema de Autenticación

### 1. Configuración de Login Manager

```python
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
```

### 2. Modelos de Usuario

Se implementan dos tipos de usuarios:

```python
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

class Alumno(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
```

### 3. Carga de Usuarios

```python
@login_manager.user_loader
def load_user(user_id):
    # Intenta cargar un usuario normal
    user = db.session.get(User, int(user_id))
    if user:
        return user
    # Si no es un usuario normal, intenta cargar un alumno
    return db.session.get(Alumno, int(user_id))
```

### 4. Rutas de Autenticación

```python
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        tipo_usuario = request.form.get('tipo_usuario')
        
        if tipo_usuario == 'admin':
            user = User.query.filter_by(email=email).first()
        else:
            user = Alumno.query.filter_by(email=email).first()
            
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('maestros.inicio' if tipo_usuario == 'admin' else 'alumnos.inicio'))
```

## Características Principales

1. **Separación de Responsabilidades**
   - Cada blueprint maneja su propia funcionalidad
   - Rutas organizadas por tipo de usuario
   - Plantillas separadas por módulo

2. **Autenticación Flexible**
   - Soporte para múltiples tipos de usuarios
   - Redirección basada en el tipo de usuario
   - Protección de rutas con `@login_required`

3. **Seguridad**
   - Contraseñas hasheadas
   - Validación de tipos de usuario
   - Protección contra acceso no autorizado

## Uso del Sistema

1. **Inicio de Sesión**
   - Acceso a través de `/login`
   - Selección de tipo de usuario (admin/alumno)
   - Redirección automática según el tipo

2. **Panel de Maestros**
   - Acceso a `/maestros`
   - Gestión de alumnos
   - Creación de preguntas

3. **Panel de Alumnos**
   - Acceso a `/alumnos`
   - Realización de exámenes
   - Visualización de resultados

## Requisitos

- Python 3.x
- Flask
- Flask-Login
- SQLAlchemy
- MySQL/MariaDB

## Instalación

1. Clonar el repositorio
2. Crear entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configurar la base de datos en `config.py`
5. Ejecutar la aplicación:
   ```bash
   python app.py
   ``` 