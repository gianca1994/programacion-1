from .. import db
from main.models import UserModel, SensorModel
from flask import request, Blueprint
from flask_jwt_extended import create_access_token
from main.mail.functions import sendMail
from main.auth.decorators import admin_required

# Utilizamos Blueprint para generar rutas y lo almacenamos en la variable auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

# La función integrada nos permitirá definir la ruta para el login y el metodo POST, escritura...
@auth.route('/login', methods=['POST'])

# Definimos el login, para el inicio de sesion del usuario
def login():
    # Validamos si hay un email duplicado y alojamos en la variable user. Si hay un duplicado nos da error 404.
    user = db.session.query(UserModel).filter(UserModel.email == request.get_json().get('email')).first_or_404()

    # Definimos el "If" para verificar si la contraseña ingresada es correcta.
    if user.validate_pass(request.get_json().get('password')):

        # Utilizamos "create_access_token" para crear un token para que el usuario lo use cuando quiera hacer
        # acciones que requieran autenticaciony lo almacenamos en la variable...
        access_token = create_access_token(identity=user)

        # Alojamos el id, email y token de acceso en la variable data
        data = '{"id":"' + str(user.id) + '","email":"' + str(user.email) + '","access_token":"' + access_token + '"}'

        # Nos devueve la variable con todos los datos dentro y el codigo 200.
        return data, 200
    # Si no
    else:
        # Nos devuelve error 401 "Contraseña incorrecta"
        return 'Incorrect password', 401

# Register eliminado, porque estabamos duplicando la misma accion...


# La función integrada nos permitirá definir la ruta para el checkeo y el metodo GET, lectura.
@auth.route("/checksensors", methods=["GET"])
# La función integrada nos permitirá decir que solo los admins pueden ingresar a esta seccion.
@admin_required
# Definimos checkStatus para...
def checkStatus():
    # Alojamos en sensors, todos los sensores de la db filtrados por active y status.
    sensors = (db.session.query(SensorModel).filter(SensorModel.active == True).filter(SensorModel.status == False).all())
    # Definimos los IF para el envio de emails.
    if sensors:
        # Alojamos en la variable admins, los usuarios traidos de la db, filtrados por "admin"
        admins = db.session.query(UserModel).filter(UserModel.admin == True).all()
        if admins:
            adminList = [admin.email for admin in admins]
            sendMail(adminList, "Deactivated sensors", "mail/sensor", sensorList=sensors)
        # Nos retorna los datos del sensor
        return jsonify({"sensors": [sensor.to_json() for sensor in sensors]})
    else:
        return "There're no deactivated sensors", 200


