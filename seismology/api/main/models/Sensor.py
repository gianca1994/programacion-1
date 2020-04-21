from main import db

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
    userid = db.Column(db.Integer, nullable=False)

    # Creamos la funcion __repr__ que nos mostrara los datos de cada Sensor que carguemos.
    def __repr__(self):
        return '<Sensor: %r %r %r %r %r %r >' % (
            self.name, self.ip, self.port, self.status, self.active, self.userid)
