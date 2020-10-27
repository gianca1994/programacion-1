from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, FloatField, IntegerField, validators, SelectField
from wtforms.fields.html5 import DateTimeLocalField as Dtime

class UnverifiedSeismEditForm(FlaskForm):

    # Definimos las variables profundidad como un integer y la variable magnitude como un flotante
    depth = IntegerField(label="Depth", validators=[validators.DataRequired(message="Only whole numbers are allowed")])
    magnitude = FloatField(label="Magnitude", validators=[validators.DataRequired(message="Only numbers with decimals are allowed")])

    # Definimos Verified = booleano para el check box (true or false) y el submin para enviar la info del formulario
    verified = BooleanField()
    submit = SubmitField("Send")


class SeismFilterForm(FlaskForm):

    datetimeFrom = Dtime(label="From Datetime", format="%Y-%m-%dT%H:%M", validators=[validators.optional()])
    datetimeTo = Dtime(label="To Datetime", format="%Y-%m-%dT%H:%M", validators=[validators.optional()])
    depth_min = IntegerField(label="Depth Min", validators=[validators.optional()])
    depth_max = IntegerField(label="Depth Max", validators=[validators.optional()])
    magnitude_min = FloatField(label="Magnitude Min", validators=[validators.optional()])
    magnitude_max = FloatField(label="Magnitude Max", validators=[validators.optional()])
    sensorId = SelectField(label="Sensor Associated", validators=[validators.optional()], coerce=int)

    # Boton para filtrar los sismos
    submit = SubmitField(label="Filter")
    # Boton para descargar los sismos que deseemos
    download = SubmitField(label="Download")
