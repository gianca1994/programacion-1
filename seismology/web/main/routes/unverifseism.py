from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_breadcrumbs import register_breadcrumb
from ..forms.unverified_seism_form import UnverifiedSeismEditForm
import requests, json
from flask_login import login_required, LoginManager
from ..utilities.functions import sendRequest


unverified_seism = Blueprint("unverified_seism", __name__, url_prefix="/unverified-seism")

@unverified_seism.route("/")
@login_required
@register_breadcrumb(unverified_seism, ".", "Unverified Seisms")
def index():
    r = sendRequest(method="get", url="/unverified-seisms", auth=True)
    unverified_seisms = json.loads(r.text)["Unverified-seisms"]
    title = "Unverified Seisms List"

    return render_template("unverified-seisms.html", title=title, unverified_seisms=unverified_seisms)

@unverified_seism.route("/view/<int:id>")
@login_required
@register_breadcrumb(unverified_seism, ".view", "Unverified Seism")
def view(id):

    r = sendRequest(method="get", url="/unverified-seism/"+str(id), auth=True)

    if (r.status_code == 404):
        flash("Seism not found", "danger")

        return redirect(url_for("unverified_seism.index"))

    unverified_seism = json.loads(r.text)
    title = "Unverified Seism View"

    return render_template("unverified-seism.html", title=title, unverified_seism=unverified_seism)

@unverified_seism.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
@register_breadcrumb(unverified_seism, ".edit", "Edit Unverified Seism")
def edit(id):

    form = UnverifiedSeismEditForm()

    if not form.is_submitted():
        r = sendRequest(method="get", url="/unverified-seism/"+str(id), auth=True)

        if (r.status_code == 404):
            flash("Unvrified Seism not found","danger")

            return redirect(url_for("unverified_seism.index"))

        unverified_seism = json.loads(r.text)
        form.depth.data = unverified_seism["depth"]
        form.magnitude.data = unverified_seism["magnitude"]
        form.verified.data = unverified_seism["verified"]

    if form.validate_on_submit():
        unverified_seism = {"depth": form.depth.data, "magnitude": form.magnitude.data, "verified": form.verified.data}
        data = json.dumps(unverified_seism)
        r = sendRequest(method="put", url="/unverified-seism/" + str(id), data=data, auth=True)
        flash("Unverified Seism edited", "success")

        return redirect(url_for("unverified_seism.index"))
    return render_template("unverfied-seismEdit_form.html", form=form, id=id)

@unverified_seism.route("/delete/<int:id>")
@login_required
def delete(id):
    r = sendRequest(method="delete", url="/unverified-seism/"+str(id), auth=True)
    flash("Unverified Seism deleted", "danger")

    return redirect(url_for("unverified_seism.index"))