from main import db
from main.models import SensorModel, SeismModel
import socket
import time

# Crear socket
def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2)
        return s
    except socket.error:
        print('Failed to create socket')
        return None

# Checkear estado sensor
def check_sensor(id):
    sensor = db.session.query(SensorModel).get_or_404(id)
    s = create_socket()
    if s:
        s.sendto(b" ", (sensor.ip, sensor.port))
        try:
            d = s.recvfrom(1024)[0]
            sensors.status = True
            db.session.add(sensor)
            db.session.commit()
        except socket.timeout:
            print("Sensor" + sensor.name + " no responde")

# Llamar a sensores
def call_sensors(app):
    with app.app_context():
        s = create_socket()
        while s:
            sensors = (
                db.session.query(SensorModel)
                    .filter(SensorModel.active == True)
                    .filter(SensorModel.status == True)
                    .all()
            )
            for sensor in sensors:
                s.sendto(b" ", (sensor.ip, sensor.port))
                try:
                    d = s.recvfrom(1024)[0]
                    seism = SeismModel.from_json(d)
                    seism.sensorId = sensor.id
                    db.session.add(seism)
                    db.session.commit()
                except socket.timeout:
                    sensor.status = False
                    db.session.add(sensor)
                    db.session.commit()
                    print("Sensor " + sensor.name + " no responde")
            time.sleep(2)
