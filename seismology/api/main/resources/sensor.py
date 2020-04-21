from flask_restful import Resource
from flask import request

SENSORS = {
    1: {'name': 'Sensor1', 'status': 'activaded'},
    2: {'name': 'Sensor2', 'status': 'disabled'},
}

# -------------------------------------------------------------------------------------#
# Creamos la clase para el recurso "Sensor".
# -------------------------------------------------------------------------------------#

class Sensor(Resource):

# -------------------------------------------------------------------------------------#
# Primero definimos "GET" para obtener el recurso de la coleccion "SENSORS" y su "ID".
# -------------------------------------------------------------------------------------#

    def get(self, id):
        if int(id) in SENSORS:
            # Si el ID del recurso existe, nos devuelve lo siguiente:
            return SENSORS[int(id)]
        # Si no existe, nos devuelve el siguiente error de cliente "404", con el mensaje.
        return 'Sensor not found', 404

# -------------------------------------------------------------------------------------#
# Ahora definimos "PUT" para modificar un recurso de la coleccion "SENSORS".
# -------------------------------------------------------------------------------------#

    def put(self, id):
        # Verificamos si existe el "Sensor".
        if int(id) in SENSORS:
            # Si existe, traemos el "Sensor" del diccionario y lo cargamos en la variable.
            sensor = SENSORS[int(id)]
            # Extraemos los valores a modificar de la info consultada, en formato json y guarda en "data".
            data = request.get_json()
            # Actualizo el diccionaro "sensor", con los nuevos datos de "data".
            sensor.update(data)
            # Nos devuelve el sensor modificado con un codigo "201" (EXITO!).
            return sensor, 201
        # Si no esta el sensor, nos devuelve el mensaje con un codigo "404" (Error de cliente).
        return 'Sensor not found', 404

# -------------------------------------------------------------------------------------#
# Definimos "DELETE" para eliminar un recurso de la coleccion "SENSORS".
# -------------------------------------------------------------------------------------#

    def delete(self, id):
        # Verificamos si existe el "Sensor".
        if int(id) in SENSORS:
            del SENSORS[int(id)]
            # Nos devuelve el mensaje de borrado con un codigo "204".
            return 'Successful deletion', 204
        # Si no esta el sensor, nos devuelve el mensaje con un codigo "404" (Error de cliente).
        return 'Sensor not found', 404

# -------------------------------------------------------------------------------------#
# Definimos "POST" para crear un recurso y alojarlo en la coleccion "SENSORS".
# -------------------------------------------------------------------------------------#

    def post(self):
        # Extraemos los valores a agregar, en formato json y guarda en "sensor".
        sensor = request.get_json()
        # Generamos un acumulador, asi cada vez aumenta el ID en 1 "+1" y nunca se va a repetir.
        id = int(max(SENSORS.keys())) + 1
        # Creamos una nueva entrada "SENSORS", al que le damos el valor de "sensor".
        SENSORS[id] = sensor
        # Nos devuelve el sensor que se acaba de crear con un codigo de exito "201".
        return SENSORS[id], 201

# -------------------------------------------------------------------------------------#
# Creamos la clase para la coleccion "Sensors".
# -------------------------------------------------------------------------------------#

class Sensors(Resource):

# -------------------------------------------------------------------------------------#
# Usamos el metodo "GET" para obtener la coleccion de recursos "SENSORS".
# -------------------------------------------------------------------------------------#
    def get(self):
        # Nos devuelve la coleccion "SENSORS".
        return SENSORS
