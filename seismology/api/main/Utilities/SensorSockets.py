from main import db
from main.models import SensorModel, SeismModel
import socket, time

# Crear socket
def createSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(2)
    return s

# Checkear estado sensor
def checkSensor(id):
    sensor = db.session.query(SensorModel).get_or_404(id)
    s = create_socket()
    if s:
        s.sendto(b" ", (sensor.ip, sensor.port))

        d = s.recvfrom(1024)[0]
        sensors.status = True
        db.session.add(sensor)
        db.session.commit()

# Llamar a sensores
def callSensors(app):
    with app.app_context():
        s = create_socket()
        while s:
            sensors = (db.session.query(SensorModel).filter(SensorModel.active == True).filter(SensorModel.status == True).all())
            for sensor in sensors:
                s.sendto(b" ", (sensor.ip, sensor.port))

                d = s.recvfrom(1024)[0]
                seism = SeismModel.from_json(d)
                seism.sensorId = sensor.id
                db.session.add(seism)
                db.session.commit()
            time.sleep(2)
