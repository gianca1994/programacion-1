from main import db

# -------------------------------------------------------------------------------------#
# Creamos la clase User con (db.Model) para que cree una tabla en la base de datos
# -------------------------------------------------------------------------------------#

class User(db.Model):
    # Definimos los atributos que van a llevar las tablas de la DB
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(99), nullable=False)
    email = db.Column(db.String(99), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    # Creamos la funcion __repr__ que nos mostrara los datos de cada user que carguemos.
    def __repr__(self):
        return '<User: %r %r %r >' % (self.password, self.email, self.admin)
