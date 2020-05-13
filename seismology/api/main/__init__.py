import os
from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail

api = Api()
# Variable utilizada para hacer todas las consultas...
db = SQLAlchemy()
# Variable jwt utilizada para manejar las "Secret Key".
jwt = JWTManager()
# Variable que usaremos para los emails del remitente.
sendmail = Mail()


def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Verifica si existe o no una DB con ese nombre y si no existe la crea...
    if not os.path.exists(os.getenv("SQLALCHEMY_DATABASE_PATH") + os.getenv("SQLALCHEMY_DATABASE_NAME")):
        # Crea una base de datos con ese nombre.
        os.mknod(os.getenv('SQLALCHEMY_DATABASE_PATH') + os.getenv('SQLALCHEMY_DATABASE_NAME'))

    # Si esta en "TRUE", TRACKEA eventos
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Ahora indicamos la url de nuestra base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.getenv('SQLALCHEMY_DATABASE_PATH') + os.getenv(
        'SQLALCHEMY_DATABASE_NAME')
    db.init_app(app)

    # Aca traemos el key del token ingresado en el .env como tambien el timpo de expiracion...
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)

    # Ahora haceremos las conecciones de las claves foraneas cuando iniciamos el servidor...
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def PrimaryKeys(conection, conection_record):
            # Comando para activar las claves foraneas.
            conection.execute('pragma foreign_keys=ON')
        with app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', PrimaryKeys)

    # Traemos la clave secreta desde el ".env"
    from .auth import routes
    # Importamos de la carpeta "resources" todos los recursos agregados en "__init__.py".
    import main.resources as resources

    api.add_resource(resources.UserResource, '/user/<id>')
    api.add_resource(resources.UsersResource, '/users')
    api.add_resource(resources.SensorResource, '/sensors/<id>')
    api.add_resource(resources.SensorsResource, '/sensors')
    api.add_resource(resources.VerifSeismResource, '/verif-seisms/<id>')
    api.add_resource(resources.VerifSeismsResource, '/verif-seisms')
    api.add_resource(resources.UnverifSeismResource, '/unverif-seisms/<id>')
    api.add_resource(resources.UnverifSeismsResource, '/unverif-seisms')

    app.config["MAIL_HOSTNAME"] = os.getenv("MAIL_HOSTNAME")
    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS")
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["FLASKY_MAIL_SENDER"] = os.getenv("FLASKY_MAIL_SENDER")

    # Iniciamos la "app".
    sendmail.init_app(app)
    api.init_app(app)
    app.register_blueprint(auth.routes.auth)

    return app
