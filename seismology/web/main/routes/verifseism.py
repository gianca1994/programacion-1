from flask import Blueprint, render_template, current_app, redirect, url_for
import requests, json

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