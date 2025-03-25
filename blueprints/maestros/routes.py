from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Alumno, Pregunta, db, User
from datetime import datetime, date

maestros = Blueprint('maestros', __name__, template_folder='../../templates')

@maestros.route('/')
@maestros.route('/inicio')
@login_required
def inicio():
    if not isinstance(current_user, User):
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('alumnos.inicio'))
    return render_template('maestros/inicio.html')

@maestros.route('/registro', methods=['GET', 'POST'])
@login_required
def registro():
    if not isinstance(current_user, User):
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('alumnos.inicio'))

    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        apaterno = request.form.get('apaterno')
        amaterno = request.form.get('amaterno')
        fecha_nacimiento = request.form.get('fecha_nacimiento')
        grupo = request.form.get('grupo')
        email = request.form.get('email')
        password = request.form.get('password')

        # Imprimir los datos recibidos para debug
        print(f"Datos recibidos: nombre={nombre}, apaterno={apaterno}, amaterno={amaterno}, "
              f"fecha_nacimiento={fecha_nacimiento}, grupo={grupo}, email={email}, password={'*' * len(password) if password else None}")

        # Validar que todos los campos estén llenos
        campos_vacios = []
        if not nombre: campos_vacios.append('Nombre')
        if not apaterno: campos_vacios.append('Apellido Paterno')
        if not amaterno: campos_vacios.append('Apellido Materno')
        if not fecha_nacimiento: campos_vacios.append('Fecha de Nacimiento')
        if not grupo: campos_vacios.append('Grupo')
        if not email: campos_vacios.append('Correo Electrónico')
        if not password: campos_vacios.append('Contraseña')

        if campos_vacios:
            flash(f'Los siguientes campos son requeridos: {", ".join(campos_vacios)}', 'danger')
            return render_template('maestros/registro.html')

        # Validar que el grupo sea uno de los permitidos
        grupos_permitidos = ['IDGS801', 'IDGS802', 'IDGS803', 'IDGS804', 'IDGS805']
        if grupo not in grupos_permitidos:
            flash('Grupo no válido', 'danger')
            return render_template('maestros/registro.html')

        # Validar y convertir la fecha de nacimiento
        try:
            fecha_nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            # Calcular edad
            hoy = date.today()
            edad = hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
            
            if edad < 0 or edad > 100:
                raise ValueError("Edad fuera de rango")
        except ValueError as e:
            flash('La fecha de nacimiento debe ser una fecha válida (YYYY-MM-DD)', 'danger')
            return render_template('maestros/registro.html')

        # Verificar si el email ya existe
        if Alumno.query.filter_by(email=email).first():
            flash('El correo electrónico ya está registrado', 'danger')
            return render_template('maestros/registro.html')

        # Crear nuevo alumno
        alumno = Alumno(
            nombre=nombre,
            apaterno=apaterno,
            amaterno=amaterno,
            fecha_nacimiento=fecha_nac,
            edad=edad,
            grupo=grupo,
            email=email
        )
        alumno.set_password(password)

        try:
            db.session.add(alumno)
            db.session.commit()
            flash('Alumno registrado exitosamente', 'success')
            return redirect(url_for('maestros.inicio'))
        except Exception as e:
            db.session.rollback()
            print(f"Error al registrar alumno: {str(e)}")  # Debug
            flash('Error al registrar el alumno', 'danger')
            return render_template('maestros/registro.html')

    return render_template('maestros/registro.html')

@maestros.route('/agregar_pregunta', methods=['GET', 'POST'])
@login_required
def agregar_pregunta():
    if not isinstance(current_user, User):
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('alumnos.inicio'))

    if request.method == 'POST':
        # Obtener datos del formulario
        pregunta = request.form.get('pregunta')
        respuesta_a = request.form.get('respuesta_a')
        respuesta_b = request.form.get('respuesta_b')
        respuesta_c = request.form.get('respuesta_c')
        respuesta_d = request.form.get('respuesta_d')
        respuesta_correcta = request.form.get('respuesta_correcta')

        # Validar que todos los campos estén llenos
        if not all([pregunta, respuesta_a, respuesta_b, respuesta_c, respuesta_d, respuesta_correcta]):
            flash('Todos los campos son requeridos', 'danger')
            return redirect(url_for('maestros.agregar_pregunta'))

        # Validar que la respuesta correcta sea una de las opciones válidas
        if respuesta_correcta not in ['A', 'B', 'C', 'D']:
            flash('Respuesta correcta no válida', 'danger')
            return redirect(url_for('maestros.agregar_pregunta'))

        # Crear nueva pregunta
        nueva_pregunta = Pregunta(
            pregunta=pregunta,
            respuesta_a=respuesta_a,
            respuesta_b=respuesta_b,
            respuesta_c=respuesta_c,
            respuesta_d=respuesta_d,
            respuesta_correcta=respuesta_correcta
        )

        try:
            db.session.add(nueva_pregunta)
            db.session.commit()
            flash('Pregunta agregada exitosamente', 'success')
            return redirect(url_for('maestros.inicio'))
        except Exception as e:
            db.session.rollback()
            flash('Error al agregar la pregunta', 'danger')
            return redirect(url_for('maestros.agregar_pregunta'))

    return render_template('maestros/agregar_pregunta.html')

@maestros.route('/lista_alumnos')
@login_required
def lista_alumnos():
    if not isinstance(current_user, User):
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('alumnos.inicio'))
    alumnos = Alumno.query.all()
    return render_template('maestros/lista_alumnos.html', alumnos=alumnos) 