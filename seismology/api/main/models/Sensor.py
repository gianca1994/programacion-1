from .. import db
from .User import User as UserModel


# -------------------------------------------------------------------------------------#
# Creamos la clase Sensor con (db.Model) para que cree una tabla en la base de datos
# -------------------------------------------------------------------------------------#

class Sensor(db.Model):
    # Definimos los atributos que van a llevar las tablas de la DB.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(99), nullable=False)
    ip = db.Column(db.String(99), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    active = db.Column(db.Boolean, nullable=False)

    # Clave foranea
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # Relaciones entre tablas
    user = db.relationship('User', back_populates='sensors', uselist=False, single_parent=True)
    seisms = db.relationship('Seism', back_populates='sensor', passive_deletes='all')

    # Creamos la funcion __repr__ que nos mostrara los datos de cada Sensor que carguemos.
    def __repr__(self):

        # Nos devuelve un sensor con 5 atributos.
        return '<Sensor: %r %r %r %r %r >' % (
            self.name, self.ip, self.port, self.status, self.active)

    # Para convertir un obj a JSON, primero definimos "to_json".
    def to_json(self):

        # Asignamos a la variable user, los recursos traidos de la db por id, si no existe, saldra error 404.
        self.user = db.session.query(UserModel).get(self.userId)

        # Realiza la operacion
        try:
            sensor_json = {'id': self.id, 'name': (self.name), 'ip': (self.ip), 'port': self.port,
                           'status': self.status, 'active': self.active, 'user': self.user.to_json()
                           }

        # Si algo pasa o ocurre mal...
        except:
            sensor_json = {'id': self.id, 'name': self.name, 'ip': self.ip, 'port': self.port, 'status': self.status,
                           'active': self.active, 'userId': self.userId
                           }

        # Devolvemos la variable con los valores asignados.
        return sensor_json

    @staticmethod
    # Para convertir de JSON a obj, primero definimos "from_json".
    def from_json(sensor_json):

        # Luego asiganmos a las variables, los valores traidos del JSON usando "sensor_json.get", para en cada caso.
        id = sensor_json.get('id')
        name = sensor_json.get('name')
        ip = sensor_json.get('ip')
        port = sensor_json.get('port')
        status = sensor_json.get('status')
        active = sensor_json.get('active')
        userId = sensor_json.get('userId')

        # Devolvemos el Sensor con todos los argumentos en forma de OBJETO
        return Sensor(id=id, name=name, ip=ip, port=port, status=status, active=active, userId=userId)
