from flask_restful import Resource
from flask import request

SENSORS = {
    1: {'name': 'Sensor01', 'status': 'activaded'},
    2: {'name': 'Sensor02', 'status': 'disabled'},
}

#RECURSO SENSOR
class Sensor(Resource):
    #OBTENER RECURSO
    def get(self, id):
        if int(id)in SENSORS:
            return SENSORS[int(id)]
        return 'Sensor not found', 404

    #MODIFICAR RECURSO
    def put(self, id):
        if int(id) in SENSORS:
            sensor = SENSORS[int(id)]
            data = request.get_json()
            sensor.update(data)
            return sensor, 201
        return 'Sensor not found', 404

#ELIMINAR RECURSO
    def delete(self, id):
        if int(id) in SENSORS:
            del SENSORS[int(id)]    
                return 'Successful deletion', 204
        return 'Sensor not found', 404


#RECURSO SENSORS
class Sensors(Resource):
    #OBTENER LISTA DE RECURSOS
        def get(self):
            return SENSORS

#INSERTAR RECURSO
    def post(self):
        sensor = request.get_json()
        print(SENSORS.keys())
        print(max(SENSORS.keys()))
        id = int(max(SENSORS.keys())) + 1
        SENSORS[id] = sensor
        return SENSORS[id], 201
