from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os

api = Api()
# Variable utilizada para hacer todas las consultas...
db = SQLAlchemy()


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

    # Iniciamos la "app".
    db.init_app(app)
    api.init_app(app)
    return app
