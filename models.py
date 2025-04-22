
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(UserMixin, db.Model):
    __tablename__ = 'Usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50), unique=True, nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    nombre_completo = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)
    fecha_nacimiento = db.Column(db.Date)
    tipo_usuario = db.Column(db.Enum('paciente', 'profesional', 'ambos', 'admin'), nullable=False)

    def set_password(self, password):
        self.contraseña = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)

    # Requerido por Flask-Login
    def get_id(self):
        return str(self.id_usuario)

    # Estos ya los provee UserMixin, pero si quieres sobreescribirlos:
    def is_active(self):
        return True

    def is_authenticated(self):
        return True



    
class Profesional(db.Model):
    __tablename__ = 'Profesionales'
    id_profesional = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), unique=True)
    especialidad = db.Column(db.String(100))
    perfil = db.Column(db.Text)

class FichaPaciente(db.Model):
    __tablename__ = 'FichaPaciente'
    id_ficha = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'), unique=True)
    rut = db.Column(db.String(12), unique=True)
    antecedentes_medicos = db.Column(db.Text)
    alergias = db.Column(db.Text)
    medicamentos_actuales = db.Column(db.Text)
    observaciones = db.Column(db.Text)
    fecha_creacion = db.Column(db.Date)

class TurnoProfesional(db.Model):
    __tablename__ = 'TurnosProfesionales'
    id_turno = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    fecha = db.Column(db.Date)
    hora_entrada = db.Column(db.Time)
    hora_salida = db.Column(db.Time)

class SolicitudCambioTurno(db.Model):
    __tablename__ = 'SolicitudCambioTurno'
    id_solicitud = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    motivo = db.Column(db.Text)
    fecha_solicitud = db.Column(db.DateTime)
    estado = db.Column(db.String(20))

class HistorialAtencion(db.Model):
    __tablename__ = 'HistorialAtenciones'
    id_atencion = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    id_profesional = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    fecha = db.Column(db.Date)
    motivo = db.Column(db.Text)
    diagnostico = db.Column(db.Text)
    tratamiento = db.Column(db.Text)

class AlertaReserva(db.Model):
    __tablename__ = 'AlertasReserva'
    id_alerta = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    tipo_alerta = db.Column(db.String(50))
    mensaje = db.Column(db.Text)
    fecha = db.Column(db.DateTime)

class Chat(db.Model):
    __tablename__ = 'Chat'
    id_chat = db.Column(db.Integer, primary_key=True)
    id_emisor = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    id_receptor = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    mensaje = db.Column(db.Text)
    fecha_envio = db.Column(db.DateTime)

class Box(db.Model):
    __tablename__ = 'Boxes'
    id_box = db.Column(db.Integer, primary_key=True)
    tipo_box = db.Column(db.String(100))
    capacidad = db.Column(db.Integer)
    equipamiento = db.Column(db.Text)
    disponible = db.Column(db.Boolean)
    id_profesional = db.Column(db.Integer, db.ForeignKey('Profesionales.id_profesional'))

class DisponibilidadBox(db.Model):
    __tablename__ = 'DisponibilidadBox'
    id_disponibilidad = db.Column(db.Integer, primary_key=True)
    id_box = db.Column(db.Integer, db.ForeignKey('Boxes.id_box'))
    fecha = db.Column(db.Date)
    hora_inicio = db.Column(db.Time)
    hora_fin = db.Column(db.Time)

class CentroAyuda(db.Model):
    __tablename__ = 'CentroAyuda'
    id_ayuda = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    tipo_solicitud = db.Column(db.String(50))
    mensaje = db.Column(db.Text)
    fecha = db.Column(db.DateTime)
    estado = db.Column(db.String(20))

class Reserva(db.Model):
    __tablename__ = 'Reservas'
    id_reserva = db.Column(db.Integer, primary_key=True)
    id_paciente = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    id_profesional = db.Column(db.Integer, db.ForeignKey('Usuarios.id_usuario'))
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    estado = db.Column(db.String(20))
