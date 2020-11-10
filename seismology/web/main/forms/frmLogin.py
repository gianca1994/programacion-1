from wtforms import PasswordField,SubmitField
from wtforms.fields.html5 import EmailField
from flask_wtf import FlaskForm
from wtforms import validators


class LoginForm(FlaskForm):
    # Definimos el email, contraseña y el "enviar" en el formulario.
    email = EmailField("E-mail",
                       [validators.Required(message="E-mail is require"),validators.Email(message='Format_Invalid')])
    password = PasswordField("Password", [validators.Required()])
    submit = SubmitField("Login")
