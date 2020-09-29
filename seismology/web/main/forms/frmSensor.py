from flask_wtf import FlaskForm
from wtforms import BooleanField, IntegerField, SelectField, StringField, SubmitField
from wtforms import validators

# Creamos la clase para agregar un nuevo sensor
class SensorCreateForm(FlaskForm):

    # Definimos las variables, name, ip, port, status, active, userId y las validaciones son "Obligatorias" para poder crear un sensor.
    name = StringField(label="Name", validators=[validators.DataRequired(message="Field with mandatory requirement")])
    ip = StringField(label="Ip", validators=[validators.DataRequired(message="Field with mandatory requirement")])
    port = IntegerField(label="Port", validators=[validators.InputRequired(message="Field with mandatory requirement")])
    status = BooleanField(label="Status")
    active = BooleanField(label="Active")
    userId = SelectField(label="User Associated", validators=[validators.InputRequired(message="Field with mandatory requirement")], coerce=int)

    # Boton de envio del paquete...
    submit = SubmitField(label="Send")

# Creamos la clase para editar un sensor existente
class SensorEditForm(FlaskForm):

    # Definimos las variables, name, ip, port, status, active, userId y las validaciones son "Obligatorias" para poder editar un sensor.
    name = StringField(label="Name", validators=[validators.DataRequired(message="Field with mandatory requirement")])
    ip = StringField(label="Ip", validators=[validators.DataRequired(message="Field with mandatory requirement")])
    port = IntegerField(label="Port", validators=[validators.InputRequired(message="Field with mandatory requirement")])
    status = BooleanField(label="Status")
    active = BooleanField(label="Active")
    userId = SelectField(label="User Associated", validators=[validators.InputRequired(message="Field with mandatory requirement")], coerce=int)

    # Boton de envio del paquete...
    submit = SubmitField(label="Send")

# Creamos la clase para filtrar un sensor de la lista de sensores
class SensorFilterForm(FlaskForm):

    # Definimos las variables, name, status, active, userId y las validaciones son "opcional" para poder filtrar por 1, 2, 3 o las 4 opciones al mismo tiempo, si asi se quiere.
    name = StringField('Name', [validators.optional()])
    status = BooleanField('Status', [validators.optional()])
    active = BooleanField('Active', [validators.optional()])
    userId = SelectField('Users', [validators.optional()], coerce=int)

    # Boton de envio del paquete...
    submit = SubmitField("Filter")