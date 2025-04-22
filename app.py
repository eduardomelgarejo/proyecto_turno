from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db
from rutas import main_bp  # Importamos el blueprint

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

# Registrar el blueprint
app.register_blueprint(main_bp)

@login_manager.user_loader
def load_user(user_id):
    from models import Usuario  # Importamos Usuario aquí para evitar problemas de importación circular
    return Usuario.query.get(int(user_id))

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
        app.run(debug=True)
    except SystemExit as e:
        print("⚠️ La aplicación se cerró con SystemExit:", e)
    except Exception as e:
        print("⚠️ Error al iniciar la app:", e)
