from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_breadcrumbs import register_breadcrumb
from ..forms.login_form import  LoginForm
import requests, json
from ..utilities.functions import sendRequest

verifseism = Blueprint("verifseism", __name__, url_prefix="/verified-seism")

@verifseism.route("/")
def index():
    r = requests.get(current_app.config["API_URL"]+"/verified-seisms",headers={"content-type":"application/json"})
    verifseism = json.loads(r.text)["Verified-seisms"]
    title = "VerifiedSeisms-List"

    return render_template("verified-seisms.html", title=title, verifseism=verifseism)

@verifseism.route("/view/<int:id>")
def view(id):
    r = requests.get(current_app.config["API_URL"]+"/verified-seism/"+str(id),headers={"content-type":"application/json"})
    if (r.status_code == 404):
        return redirect(url_for("verifseism.index"))

    verifseism = json.loads(r.text)
    title = "VerifiedSeism-View"

    return render_template("verified-seism.html", title=title, verifseism=verifseism)




verified_seism = Blueprint("verified_seism", __name__, url_prefix="/verified-seism")

@verified_seism.route("/")
@register_breadcrumb(verified_seism, ".", "Verified Seisms")
def index():
    r = sendRequest(method="get", url="/verified-seisms")
    verified_seisms = json.loads(r.text)["Verified-seisms"]
    title = "Verified Seisms List"
    loginForm = LoginForm()

    return render_template("verified-seisms.html", title=title, verified_seisms=verified_seisms, loginForm=loginForm)

@verified_seism.route("/view/<int:id>")
@register_breadcrumb(verified_seism, ".view", "View")
def view(id):
    r = sendRequest(method="get", url="/verified-seism/" + str(id))

    if (r.status_code == 404):
        return redirect(url_for("verified_seism.index"))

    verified_seism = json.loads(r.text)
    title = "Verified Seism View"
    loginForm = LoginForm()

    return render_template("verified-seism.html", title=title, verified_seism=verified_seism, loginForm=loginForm)