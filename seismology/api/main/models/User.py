from .. import db
from werkzeug.security import generate_password_hash, check_password_hash


# -------------------------------------------------------------------------------------#
# Creamos la clase User con (db.Model) para que cree una tabla en la base de datos
# -------------------------------------------------------------------------------------#

class User(db.Model):
    # Definimos los atributos que van a llevar las tablas de la DB
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(99), nullable=False)
    email = db.Column(db.String(99), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)

    # Relaciones entre tablas
    sensors = db.relationship('Sensor', back_populates='user')

    # @property funcionaria como la funcion get, para obtener el valor del atributo.
    @property
    def plain_password(self):
        # En caso de no poder leer el atributo, nos dara el siguiente error..
        raise AttributeError('Password cant be read')

    @plain_password.setter
    # Definimos plain_password para darle un valor a password
    def plain_password(self, password):
        # Llamar la funcion generate_password_hash() para generar una contraseña encriptada y la almacenamos en password.
        self.password = generate_password_hash(password)

    # Definimos validate_pass para verificar que la contraseña sea correcta al iniciar sesion.
    def validate_pass(self, password):
        # Retornamos funcion check_password_hash(), compara la password de la db con la que ingreso el usuario.
        return check_password_hash(self.password, password)

    # Creamos la funcion __repr__ que nos mostrara los datos de cada user que carguemos.
    def __repr__(self):
        # Nos devuelve un usuario con 3 atributos.
        return '<User: %r %r >' % (self.id, self.email)

    # Para convertir un obj a JSON, primero definimos "to_json".
    def to_json(self):
        # Creamos una variable en este caso llamada "user_json" a la que le asignaremos los valores de: id y email.
        user_json = {'id': self.id, 'email': str(self.email), "admin": self.admin}

        # Devolvemos la variable con los valores asignados.
        return user_json

    # Para convertir de JSON a obj, primero definimos "from_json".
    def from_json(user_json):
        # Luego asiganmos a las variables, los valores traidos del JSON usando "user_json.get", para en cada caso.
        id = user_json.get('id')
        password = user_json.get('password')
        email = user_json.get('email')
        admin = user_json.get('admin')

        # Devolvemos el usuario con todos los argumentos en forma de OBJETO
        return User(id=id, plain_password=password, email=email, admin=admin)

    def to_json_public(self):
        user_json = {"id": self.id, "email": str(self.email)}
        return user_json