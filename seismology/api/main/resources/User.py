from flask_restful import Resource
from flask import request, jsonify
from main.models import UserModel
from .. import db
from main.auth.decorators import admin_required


# -------------------------------------------------------------------------------------#
# Creamos la clase para el recurso "User".
# -------------------------------------------------------------------------------------#

class User(Resource):

    #  @admin_required
    # Definimos "GET" para obtener un recurso de una coleccion y su "ID".
    def get(self, id):
        # Asignamos a la variable "user" un usuario traido de la db, si no existe, error 404.
        user = db.session.query(UserModel).get_or_404(id)
        # Nos devuelve el usuario guardado en la variable "user" en formato "JSON".
        return user.to_json()

    #  @admin_required
    # Ahora para modifcar un recurso definimos un "PUT".
    def put(self, id):
        # Asignamos 2 variables, en user guardamos un usuario traido de la db, si no existe, error 404.
        user = db.session.query(UserModel).get_or_404(id)
        # Extraemos los valores a modificar de la info consultada, en formato json y guarda en "data".
        data = request.get_json().items()

        # Utilizamos un FOR para recorrer el diccionario y evalua el contenido alojado en data.
        for key, value in data:
            setattr(user, key, value)
        # Agregamos un nuevo usuario a la db.
        db.session.add(user)
        # Actualizamos la db.
        db.session.commit()

        # Nos devuelve el usuario que creamos nuevo con un codigo "201 (CREATED!!)".
        return user.to_json(), 201

    #  @admin_required
    # Por ultimo definimos un "delete" para borrar un usuario de la coleccion.
    def delete(self, id):
        # Borra un usuario especificado por id, en caso de no existir nos da un error 404.
        user = db.session.query(UserModel).get_or_404(id)

        # Borramos un usuario a la db.
        db.session.delete(user)
        # Actualizamos la db.
        db.session.commit()

        # Nos devuelve el usuario que deseamos borrar con un codigo "204 (NO HAY CONTENIDO!!)".
        return 'User deleted Succesfully', 204


# -------------------------------------------------------------------------------------#
# Creamos la clase para la coleccion "Users".
# -------------------------------------------------------------------------------------#

class Users(Resource):

    #  @admin_required
    # Definimos "GET" para obtener la coleccion de "Usuarios".
    def get(self):
        # Hacemos un pedido a la base de datos de que traiga a todos los usuarios almacenados en la db.
        users = db.session.query(UserModel).all()

        # Nos devolvera en formato json la lista de usuarios de la coleccion.
        return jsonify({'Users': [user.to_json() for user in users]})

    # Definimos "POST" para crear un recurso y alojarlo en la coleccion "SENSORS".
    def post(self):
        # Traemos la coleccion de recursos y la alojamos en la variable "user"
        user = UserModel.from_json(request.get_json())
        # Traemos el email de la db y lo filtramos por usuario
        emailinuse = db.session.query(UserModel).filter(UserModel.email == user.email).scalar() is not None
        # Si el email esta en uso, osea, se intenta duplicar
        if emailinuse:
            # Nos retorna que el email ya esta en uso con un codigo 409.
            return "Email already in use", 409
        # Si no
        else:
            # Agregamos un nuevo usuario y actualizamos la db.
            db.session.add(user)
            db.session.commit()

            # Nos devuelve el usuario AGREGADO con un codigo "201 (CREADO!!)".
            return user.to_json(), 201


class UsersInfo(Resource):
    # Obtenemos la lista de los recursos
    def get(self):
        users = db.session.query(UserModel)
        # Devolvemos la misma, con un formato publico, para los users que no estan logueados...
        return jsonify({"Users": [user.to_json_public() for user in users]})
