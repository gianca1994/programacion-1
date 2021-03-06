from flask import Blueprint, render_template, current_app, redirect, url_for, flash, request
from flask_breadcrumbs import register_breadcrumb
from ..forms.frmUser import UserEditForm, UserCreateForm
import json
from flask_login import login_required, LoginManager
from ..utilities.Functions import sendRequest
#from .auth import admin_required


user = Blueprint("user", __name__, url_prefix="/user")

@user.route("/")
@login_required
#@admin_required
@register_breadcrumb(user, ".", "Users")
def index():

    fact={}
    if "page" in request.args:
        fact["page"] = request.args.get("page", "")
    else:
        if "page" in fact:
            del fact["page"]

    r = sendRequest(method="get", url="/users", auth=True, data=json.dumps(fact))

    if r.status_code != 200:
        return redirect(url_for("user.index"))
    else:
        print(r.text)

        users = json.loads(r.text)["Users"]
        paginate = {}
        paginate["total"] = json.loads(r.text)["total"]
        paginate["pages"] = json.loads(r.text)["pages"]
        paginate["current_page"] = json.loads(r.text)["page"]
        title = "Users List"
        return render_template("users.html", title=title, users=users, pagination=paginate)


@user.route("/view/<int:id>")
@login_required
#@admin_required
@register_breadcrumb(user,".view","View")
def view(id):
    r = sendRequest(method="get", url="/user/"+str(id), auth=True)

    if (r.status_code == 404):
        flash("User not found","danger")
        return redirect(url_for("user.index"))
    user = json.loads(r.text)
    title = "User View"

    return render_template("user.html", title=title, user=user)

@user.route("/create", methods=["GET", "POST"])
@login_required
#@admin_required
@register_breadcrumb(user, ".create", "Create User")
def create():
    form = UserCreateForm()

    if form.validate_on_submit():
        user = {"email": form.email.data,"password": form.password.data, "admin": form.admin.data}
        data = json.dumps(user)
        r = sendRequest(method="post", url="/users", data=data, auth=True)
        return redirect(url_for("user.index"))

    return render_template("frmNewUser.html", form=form)

@user.route("/edit/<int:id>", methods=["GET","POST"])
@login_required
#@admin_required
@register_breadcrumb(user, ".edit", "Edit User")
def edit(id):
    form = UserEditForm()


    if not form.is_submitted():
        r = sendRequest(method="get", url="/user/"+str(id), auth=True)

        if (r.status_code == 404):
            flash("User not found","danger")
            return redirect(url_for("user.index"))

        user = json.loads(r.text)
        form.email.data = user["email"]
        form.admin.data = user["admin"]

    if form.validate_on_submit():
        user = {"email": form.email.data, "admin": form.admin.data}
        data = json.dumps(user)


        r = sendRequest(method="put", url="/user/"+str(id), data=data, auth=True)
        flash("User edited","success")
        return redirect(url_for("user.index"))

    return render_template("frmEditUser.html", form=form, id=id)

@user.route("/delete/<int:id>")
@login_required
#@admin_required
def delete(id):
    r = sendRequest(method="delete", url="/user/"+str(id), auth=True)
    flash("User deleted","danger")
    return redirect(url_for("user.index"))
