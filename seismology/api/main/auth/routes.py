from .. import db
from main.models import UserModel
from flask import request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

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
        access_token = create_access_token(identity=user.id)

        # Alojamos el id, email y token de acceso en la variable data
        data = '{"id":"' + str(user.id) + '","email":"' + str(user.email) + '","access_token":"' + access_token + '"}'

        # Nos devueve la variable con todos los datos dentro y el codigo 200.
        return data, 200
    # Si no
    else:
        # Nos devuelve error 401 "Contraseña incorrecta"
        return 'Incorrect password', 401

# Register eliminado, porque estabamos duplicando la misma accion...