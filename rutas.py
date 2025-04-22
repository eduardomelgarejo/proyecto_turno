from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from models import db, Usuario,TurnoProfesional


# Definimos un blueprint para organizar las rutas
main_bp = Blueprint('main', __name__)

# Ruta de Login
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identificador = request.form['identificador']
        password = request.form['password']

        # Buscar por nombre de usuario o correo
        usuario = Usuario.query.filter(
            (Usuario.nombre_usuario == identificador) | (Usuario.correo == identificador)
        ).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            return redirect(url_for('main.dashboard'))  # Cambié 'dashboard' para usar el blueprint

        flash("Usuario o contraseña incorrectos.", "danger")  # Mostrar error
        return render_template('login.html')

    return render_template('login.html')


# Ruta de Registro
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre_usuario = request.form['username']
        contraseña = request.form['password']
        tipo_usuario = request.form['role']

        if Usuario.query.filter_by(nombre_usuario=nombre_usuario).first():
            flash('El nombre de usuario ya está en uso', 'warning')
            return redirect(url_for('main.register'))  # Cambié 'register' para usar el blueprint

        user = Usuario(nombre_usuario=nombre_usuario, tipo_usuario=tipo_usuario)
        user.set_password(contraseña)
        db.session.add(user)
        db.session.commit()

        flash('Usuario registrado con éxito', 'success')
        return redirect(url_for('main.login'))  # Cambié 'login' para usar el blueprint

    return render_template('register.html')


# Ruta de Dashboard
@main_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.tipo_usuario == 'admin':
        return render_template('panel_admin.html')
    elif current_user.tipo_usuario == 'profesional':
        return render_template('panel_profesional.html')
    elif current_user.tipo_usuario == 'paciente':
        return render_template('panel_usuario.html')
    elif current_user.tipo_usuario == 'ambos':
        return render_template('panel_ambos.html')
    else:
        return "Tipo de usuario no reconocido", 403


# Ruta de Logout
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))  # Cambié 'login' para usar el blueprint


# Ruta Home
@main_bp.route('/')
def home():
    return redirect(url_for('main.login'))  # Cambié 'login' para usar el blueprint


# Ruta para gestionar profesionales
@main_bp.route('/gestionar_profesionales')
@login_required
def gestionar_profesionales():
    # Lógica para gestionar profesionales
    return render_template('gestionar_profesionales.html')

@main_bp.route('/gestionar_turnos')
def gestionar_turnos():
    # Obtener todos los turnos
    turnos = TurnoProfesional.query.all()
    return render_template('gestionar_turnos.html', turnos=turnos)

@main_bp.route('/eliminar_turno/<int:id_turno>', methods=['GET'])
def eliminar_turno(id_turno):
    turno = TurnoProfesional.query.get(id_turno)
    if turno:
        db.session.delete(turno)
        db.session.commit()
    return redirect(url_for('main.gestionar_turnos'))

@main_bp.route('/agendar_turno', methods=['GET', 'POST'])
def agendar_turno():
    if request.method == 'POST':
        id_usuario = request.form['id_usuario']
        fecha = request.form['fecha']
        hora_entrada = request.form['hora_entrada']
        hora_salida = request.form['hora_salida']

        # Crear el nuevo turno
        nuevo_turno = TurnoProfesional(id_usuario=id_usuario, fecha=fecha,
                                       hora_entrada=hora_entrada, hora_salida=hora_salida)
        db.session.add(nuevo_turno)
        db.session.commit()
        return redirect(url_for('main.gestionar_turnos'))

    # Si es un GET, mostramos el formulario
    usuarios = Usuario.query.all()  # Asumiendo que los usuarios son los profesionales
    return render_template('agendar_turno.html', usuarios=usuarios)




