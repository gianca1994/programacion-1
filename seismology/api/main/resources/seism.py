from flask_restful import Resource
from flask import request

VERIF_SEISMS = {
    1: {'datatime': '01/01/2019', 'magnitude': '7,1'},
    2: {'datatime': '02/01/2019', 'magnitude': '9.6'},
}
UNVERIF_SEISMS = {
    1: {'datetime': '03/02/2020', 'magnitude': '4.0'},
    2: {'datatime': '04/02/2020', 'magnitude': '9.9'},
}

# -------------------------------------------------------------------------------------#
# Creamos la clase para verificar el recurso "Seism".
# -------------------------------------------------------------------------------------#

class VerifSeism(Resource):

    # Definimos "GET" para obtener un recurso de una coleccion y su "ID".
    def get(self, id):
        if int(id) in VERIF_SEISMS:
            # Si el recurso existe, nos devolvera:
            return VERIF_SEISMS[int(id)]
        # Si el recurso no esta, nos devuelve el mensaje "Seism not found", es un error en el cliente.
        return 'Seism not found', 404

# -------------------------------------------------------------------------------------#
# Creamos la clase para verificar la COLECCION de recursos "Seisms"
# -------------------------------------------------------------------------------------#

class VerifSeisms(Resource):

    # Luego definimos un "GET" para obtener la coleccion
    def get(self):
        # Con el return nos devolvera la coleccion de Seisms.
        return VERIF_SEISMS

# -------------------------------------------------------------------------------------#
# Creamos la clase para trabajar sobre algun recurso "UnverifSeism" de la coleccion.
# -------------------------------------------------------------------------------------#

class UnverifSeism(Resource):
    # Definimos "GET" para obtener un "UNVERIF_SEISMS" con su id de la coleccion.
    def get(self, id):
        # Si el "Unverif_Seisms" existe en la coleccion.
        if int(id) in UNVERIF_SEISMS:
            # Nos devuelve los datos del "Unverif_Seisms".
            return UNVERIF_SEISMS[int(id)]
        # En caso de no existir, nos devuelve un error 404 con el siguiente mensaje.
        return 'Seism not found', 404

    # Ahora para modifcar un recurso definimos un "PUT".
    def put(self, id):
        # Si existe, un unverif_seism asignado a ese id.
        if int(id) in UNVERIF_SEISMS:
            # Si existe, traemos el "UNVERIF_SEISMS" del diccionario y lo cargamos en la variable.
            seism = UNVERIF_SEISMS[int(id)]
            # Extraemos los valores a modificar de la info consultada, en formato json y guarda en "data".
            data = request.get_json()
            # Actualizo el diccionaro "seism", con los nuevos datos de "data".
            seism.update(data)
            # Nos devuelve el seism modificado con un codigo "201" (EXITO!).
            return seism, 201
        # Si no esta el seism, nos devuelve el mensaje con un codigo "404" (Error de cliente)
        return 'Seism not found', 404

    # Por ultimo definimos un "delete" para borrar un seism de la coleccion.
    def delete(self, id):
        # Si el "Unverif_Seisms" buscado por el id, existe en la coleccion.
        if int(id) in UNVERIF_SEISMS:
            # Lo elimina.
            del UNVERIF_SEISMS[int(id)]
            # Y nos devuelve el cod. 204 con el mensaje:
            return 'Successful deletion', 204
        # En caso de no existir, nos devuelve el 404 con su mensaje de fallo en el cliente.
        return 'Seism not found', 404

# -------------------------------------------------------------------------------------#
# Creamos la clase para VER la COLECCION de recursos "Seisms"
# -------------------------------------------------------------------------------------#

class UnverifSeisms(Resource):
    # Aca definimos un "GET" en esta clase para obtener la coleccion de seisms.
    def get(self):
        # Nos retorna la coleccion completa de seisms...
        return UNVERIF_SEISMS