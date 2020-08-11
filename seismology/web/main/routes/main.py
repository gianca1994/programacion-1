from flask import Blueprint, redirect, url_for
from . import verifseism

main = Blueprint("main", __name__, url_prefix="/")

@main.route("/")
def index():
    return redirect(url_for("verifseism.index"))