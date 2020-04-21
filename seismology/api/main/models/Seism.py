from main import db

# -------------------------------------------------------------------------------------#
# Creamos la clase Seism con (db.Model) para que cree una tabla en la base de datos
# -------------------------------------------------------------------------------------#

class Seism(db.Model):
    # Definimos los atributos que van a llevar las tablas de la DB.
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    magnitude = db.Column(db.Float(9), nullable=False)
    latitude = db.Column(db.String(99), nullable=False)
    longitude = db.Column(db.String(99), nullable=False)
    depth = db.Column(db.Integer, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    sensorid = db.Column(db.Integer, nullable=False)

    # Creamos la funcion __repr__ que nos mostrara los datos de cada seism que carguemos.
    def __repr__(self):
        return '<Seism: %r %r %r %r %r %r %r >' % (
            self.datetime, self.magnitude, self.latitude, self.longitude, self.depth, self.verified, self.sensorid)

    # Convertir un obj a JSON
    def to_json(self):
        seism_json = {
            'id': self.id,
            'datetime': datetime(self.datetime),
            'magnitude': float(self.magnitude),
            'latitude': str(self.latitude),
            'longitude': str(self.longitude),
            'depth': int(self.depth),
            'verified': bool(self.verified),
            'sensorid': int(self.sensorid),
        }
        return seism_json

    @staticmethod
    # Convertir de JSON a obj
    def from_json(seism_json):
        id = seism_json.get('id')
        datetime = seism_json.get('datetime')
        magnitude = seism_json.get('magnitude')
        latitude = seism_json.get('latitude')
        longitude = seism_json.get('longitude')
        depth = seism_json.get('depth')
        verified = seism_json.get('verified')
        sensorid = seism_json.get('sensorid')
        return Seism(id=id,
                     datetime=datetime,
                     magnitude=magnitude,
                     latitude=latitude,
                     longitude=longitude,
                     depth=depth,
                     verified=verified,
                     sensorid=sensorid,
                     )
