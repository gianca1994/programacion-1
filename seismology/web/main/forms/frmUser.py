from flask_wtf import FlaskForm
from wtforms import PasswordField,SubmitField, BooleanField
from wtforms.fields.html5 import EmailField
from wtforms import validators

# Clase definida para crear un nuevo usuario
class UserCreateForm(FlaskForm):

    # Definimos el email, la password, la confirmacion de la pass, si es o no admin y el boton submit para enviar el frm
    email = EmailField("Email", [validators.Required(message = "Email is required"),validators.Email(message = "Format invalid")])
    password = PasswordField("Password", [validators.Required(), validators.EqualTo("confirm", message = "Passwords must match")])
    confirm = PasswordField("Repeat Password")
    admin = BooleanField("Admin")
    submit = SubmitField("Send")

# Clase definida para editar un usuario ya creado
class UserEditForm(FlaskForm):

    # Definimos el email del usuario, si es o no admin (true or false) y por ultimo la variable submit para enviar la info del formulario
    email = EmailField("Email", [validators.Required(message = "Email is required"), validators.Email(message = "Format invalid")])

    admin = BooleanField("Admin")
    submit = SubmitField("Send")