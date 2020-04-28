from .. import db
from datetime import datetime as dt
from .Sensor import Sensor as SensorModel


# -------------------------------------------------------------------------------------#
# Creamos la clase Seism con (db.Model) para que cree una tabla en la base de datos
# -------------------------------------------------------------------------------------#

class Seism(db.Model):
    # Definimos los atributos que van a llevar las tablas de la DB.
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    magnitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.String(99), nullable=False)
    longitude = db.Column(db.String(99), nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)

    # Relaciones entre tablas
    sensorId = db.Column(db.Integer, db.ForeignKey('sensor.id', ondelete='RESTRICT'), nullable=False)
    sensor = db.relationship('Sensor', back_populates='seisms', uselist=False, single_parent=True)

    # Creamos la funcion __repr__ que nos mostrara los datos de cada seism que carguemos.
    def __repr__(self):
        # Nos devuelve un seism con 6 atributos.
        return '<Seism: %r %r %r %r %r %r >' % (
            self.datetime, self.magnitude, self.latitude, self.longitude, self.depth, self.verified)

    # Para convertir un obj a JSON, primero definimos "to_json".
    def to_json(self):
        # Asignamos a la variable sensor, los recursos traidos de la db por id, si no existe, saldra error 404.
        self.sensor = db.session.query(SensorModel).get_or_404(self.sensorId)

        # Realizamos la operacion...
        seism_json = {
            'id': self.id, 'datetime': self.datetime.strftime('%Y-%m-%d %H:%M:%S'), 'magnitude': str(self.magnitude),
            'latitude': str(self.latitude), 'longitude': str(self.longitude), 'depth': self.depth,
            'verified': self.verified, 'sensorid': self.sensorid, 'sensor': self.sensor.to_json()
        }

        # Devolvemos la variable con los valores asignados.
        return seism_json

    @staticmethod
    # Para convertir de JSON a obj, primero definimos "from_json".
    def from_json(seism_json):
        # Luego asiganmos a las variables, los valores traidos del JSON usando "seism_json.get", para en cada caso.
        id = seism_json.get('id')
        datetime = dt.strptime(seism_json.get('datetime'), '%Y-%m-%d %H:%M:%S')
        magnitude = seism_json.get('magnitude')
        latitude = seism_json.get('latitude')
        longitude = seism_json.get('longitude')
        depth = seism_json.get('depth')
        verified = seism_json.get('verified')
        sensorid = seism_json.get('sensorid')

        # Devolvemos el Seism con todos los argumentos en forma de OBJETO
        return Seism(id=id, datetime=datetime, magnitude=magnitude, latitude=latitude, longitude=longitude,
                     depth=depth, verified=verified, sensorid=sensorid)
