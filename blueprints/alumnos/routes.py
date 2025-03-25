from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Pregunta, db

alumnos = Blueprint('alumnos', __name__, template_folder='../../templates')

@alumnos.route('/')
@alumnos.route('/inicio')
@login_required
def inicio():
    return render_template('alumnos/inicio.html')

@alumnos.route('/realizar_examen', methods=['GET', 'POST'])
@login_required
def realizar_examen():
    if request.method == 'POST':
        # Obtener todas las preguntas
        preguntas = Pregunta.query.all()
        respuestas_correctas = 0
        
        # Verificar cada respuesta
        for pregunta in preguntas:
            respuesta_usuario = request.form.get(f'pregunta_{pregunta.id}')
            if respuesta_usuario == pregunta.respuesta_correcta:
                respuestas_correctas += 1
        
        # Calcular calificación
        total_preguntas = len(preguntas)
        calificacion = (respuestas_correctas / total_preguntas) * 100 if total_preguntas > 0 else 0
        
        return render_template('alumnos/resultado.html', 
                             calificacion=calificacion,
                             respuestas_correctas=respuestas_correctas,
                             total_preguntas=total_preguntas)
    
    preguntas = Pregunta.query.all()
    return render_template('alumnos/realizar_examen.html', preguntas=preguntas) 