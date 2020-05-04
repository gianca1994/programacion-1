from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SensorModel


# -------------------------------------------------------------------------------------#
# Creamos la clase para el recurso "Sensor".
# -------------------------------------------------------------------------------------#

class Sensor(Resource):

    # Primero definimos "GET" para obtener el recurso de la coleccion "SENSORS" y su "ID".
    def get(self, id):
        # Asignamos a la variable "sensor" un sensor traido de la db, en caso de no existir, nos dara error 404.
        sensor = db.session.query(SensorModel).get_or_404(id)

        # Nos devuelve el sensor pedido por id en formato JSON.
        return sensor.to_json()

    # Ahora definimos "PUT" para modificar un sensor.
    def put(self, id):

        # Verificamos si existe el "Sensor", si esta lo almacena en "sensor, sino nos da error 404.
        sensor = db.session.query(SensorModel).get_or_404(id)
        # En la variable data guardamos los datos obtenidos.
        data = request.get_json().items()

        # Utilizamos un FOR para recorrer el diccionario y evalua el contenido alojado en data.
        for key, value in data:
            setattr(sensor, key, value)
        # Agregamos un sensor.
        db.session.add(sensor)
        # Realiza la operacion, actualiza la db y retorna el sensor en formato JSON. Codigo 201.
        try:
            db.session.commit()
            # Codigo "201 (Nuevo recurso Creado)".
            return sensor.to_json(), 201
        # Si algo pasa o ocurre mal...
        except Exception as error:
            # Error "400 (Solicitud incorrecta)".
            return str(error), 400

    # Definimos "DELETE" para eliminar un recurso de la coleccion "SENSORS".
    def delete(self, id):
        # Verificamos si existe el "Sensor", si existe, lo almacena en la variable sensor, sino nos dara error 404.
        sensor = db.session.query(SensorModel).get_or_404(id)

        # Ahora eliminaremos registro del sensor asignado a la variable "sensor".
        db.session.delete(sensor)

        # Realiza la operacion, actualiza la db. Codigo 204.
        try:
            db.session.commit()
            # Nos devuelve el mensaje de borrado con un codigo "204 (No hay contenido)".
            return 'Successful deleted sensor', 204

        # Si algo pasa o ocurre mal...
        except Exception as error:
            # Realiza un rollback y retrocede y nos retorna un error "400 (Solicitud incorrecta)"
            db.session.rollback()
            return str(error), 400


# -------------------------------------------------------------------------------------#
# Creamos la clase para la coleccion "Sensors".
# -------------------------------------------------------------------------------------#

class Sensors(Resource):

    # Usamos el metodo "GET" para obtener la coleccion de recursos "SENSORS".
    def get(self):

        # Definimos la variable "page" para decir cuantas paginas tendremos.
        page = 1
        # Definimos "perpage" para decir cuantos sensores mostrara cada pagina.
        perpage = 10

        # Traemos la coleccion de sensores de la db y la alojamos en la variable "sensors".
        sensors = db.session.query(SensorModel)
        # Filtraremos el/los sensores a mostrar "request.get_json().items()" y los almacenaremos en la variable.
        filters = request.get_json().items()

        # Utilizamos un FOR para recorrer el diccionario y evalua el contenido alojado en filters.
        for key, value in filters:
            # Utilizamos condicionales para filtrar por partes...
            if key == "userId":
                sensors = sensors.filter(SensorModel.userId == value)
            if key == "user":
                if value:
                    sensors = sensors.filter(SensorModel.userId != None)
                else:
                    sensors = sensors.filter(SensorModel.userId is None)
                if key == "name":
                    sensors = sensors.filter(SensorModel.name == value)
                if key == "ip":
                    sensors = sensors.filter(SensorModel.ip == value)
                if key == "port":
                    sensors = sensors.filter(SensorModel.port == value)
                if key == "active":
                    sensors = sensors.filter(SensorModel.active == value)
                if key == "status":
                    sensors = sensors.filter(SensorModel.status == value)
                if value == "active.desc":
                    sensors = sensors.order_by(SensorModel.active.desc())
                if value == "status.desc":
                    sensors = sensors.order_by(SensorModel.status.desc())
                if value == "name.desc":
                    sensors = sensors.order_by(SensorModel.name.desc())

                # Definimos los if dentro de for para paginas y cantidad de sensores mostrados por pagina.
                if key == "page":
                    page = value
                if key == "perpage":
                    perpage = value

        # Alojamos en la variable sensors, todos los sensores obtenidos de las paginas.
        sensors = sensors.paginate(page, perpage, True, 500)

        # Nos devuelve la coleccion con los sensores filtrados.
        return jsonify({"Sensors": [sensor.to_json() for sensor in sensors.items]})

    # Definimos "POST" para agregar un sensor a la coleccion.
    def post(self):
        # Traemos la coleccion de sensores de la db y la alojamos en la variable "sensors".
        sensor = SensorModel.from_json(request.get_json())
        # Añadimos un sensor a la coleccion
        db.session.add(sensor)

        # Realiza la operacion
        try:
            # Actualiza la db y nos devuelve el mensaje de creado con un codigo "201 (Nuevo recurso Creado)".
            db.session.commit()
            return sensor.to_json(), 201
        # Si algo pasa o ocurre mal...
        except Exception as error:
            # Nos retorna el error "400 (Solicitud incorrecta)"
            return str(error), 400
