from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, FloatField, IntegerField, validators

class UnverifiedSeismEditForm(FlaskForm):

    # Definimos las variables profundidad como un integer y la variable magnitude como un flotante
    depth = IntegerField(label="Depth", validators=[validators.DataRequired(message="Only whole numbers are allowed")])
    magnitude = FloatField(label="Magnitude", validators=[validators.DataRequired(message="Only numbers with decimals are allowed")])

    # Definimos Verified = booleano para el check box (true or false) y el submin para enviar la info del formulario
    verified = BooleanField()
    submit = SubmitField("Send")