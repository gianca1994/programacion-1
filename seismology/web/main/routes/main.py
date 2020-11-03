from flask import Blueprint, redirect, url_for, current_app, make_response, flash
from flask_breadcrumbs import register_breadcrumb
from ..forms.frmLogin import LoginForm
from flask_login import logout_user, login_user
import requests, json
from .auth import User


main = Blueprint("main", __name__, url_prefix="/")

@main.route("/")
@register_breadcrumb(main, "breadcrumbs.", "Home")
def index():
    return redirect(url_for("verified_seism.index"))

@main.route("/login", methods=["POST"])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():

        # Enviamos la peticion de logueo con los datos cargados en la variable "data", a la API.
        data = '{"email":"' + loginForm.email.data + '", "password":"' + loginForm.password.data + '"}'
        r = requests.post(current_app.config["API_URL"]+"/auth/login", headers={"content-type":"application/json"}, data = data)

        # Si la peticion se realiza con exito, cargamos los valores devueltos por la API en la variable "user"
        if r.status_code == 200:
            user_data = json.loads(r.text)
            user = User(id = user_data.get("id"), email = user_data.get("email"), admin = user_data.get("admin"))

            # Logueamos al usuario
            login_user(user)

            # Creamos la redireccion y Seteamos la coockie con el TOKEN
            req = make_response(redirect(url_for("main.index")))
            req.set_cookie("access_token", user_data.get("access_token"), httponly=True)
            return req
        else:
            # Si no, mostramos...
            flash("User or password incorrect", "danger")
    return redirect(url_for("main.index"))

@main.route("/logout")
def logout():
    # Creamos la request, vaciamos la cockie y deslogueamos al usuario.
    req = make_response(redirect(url_for("main.index")))
    req.set_cookie("access_token", "", httponly=True)
    logout_user()
    return req
