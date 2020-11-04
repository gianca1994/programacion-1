from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_breadcrumbs import register_breadcrumb
import requests, json
from flask_login import login_required, LoginManager
from ..utilities.Functions import sendRequest
from .auth import admin_required
from ..forms.frmSensor import SensorCreateForm, SensorEditForm, SensorFilterForm

sensor = Blueprint("sensor", __name__, url_prefix="/sensor")

@sensor.route("/")
@login_required
@admin_required
@register_breadcrumb(sensor,".","Sensors")
def index():

    filter = SensorFilterForm(request.args, meta={'crsf': False})
    r = sendRequest(method="get", url="/users", auth=True)
    filter.userId.choices = [(item['id'], item['email']) for item in json.loads(r.text)["Users"]]
    filter.userId.choices.insert(0, [0, 'All'])
    fact = {}

    if filter.validate():
        if filter.name.data != None:
            fact['name'] = filter.name.data
        if filter.status.data != None:
            fact['status'] = filter.status.data
        if filter.active.data != None:
            fact['active'] = filter.active.data
        if filter.userId.data != None and filter.userId.data != 0:
            fact['userId'] = filter.userId.data

    if "page" in request.args:
        fact["page"] = request.args.get("page", "")
    else:
        if "page" in fact:
            del fact["page"]

    if 'sort_by' in request.args:
        fact['sort_by'] = request.args.get('sort_by', '')

    r = sendRequest(method="get", url="/sensors", data=json.dumps(fact), auth=True)

    if (r.status_code == 200):
        sensors = json.loads(r.text)["sensors"]
        paginate = {}
        paginate['total'] = json.loads(r.text)['total']
        paginate['pages'] = json.loads(r.text)['pages']
        paginate['current_page'] = json.loads(r.text)['page']
        title = "Sensors"

        return render_template("sensors.html", title=title, sensors=sensors, filter=filter, pagination=paginate)
    else:
        flash("filtering error", "danger")
        redirect(url_for('main.logout'))


@sensor.route("/view/<int:id>")
@login_required
@admin_required
@register_breadcrumb(sensor, ".view", "Sensor")
def view(id):

    r = sendRequest(method="get", url="/sensor/" + str(id), auth=True)

    if (r.status_code == 404):
        flash("Sensor not found", "danger")

        return redirect(url_for("sensor.index"))

    sensor = json.loads(r.text)
    title = "Sensor View"

    return render_template("sensor.html", title=title, sensor=sensor)


@sensor.route("/create", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(sensor, ".create", "Create Sensor")
def create():

    form = SensorCreateForm()
    if form.validate_on_submit():
        sensor = {"name": form.name.data, "ip": form.ip.data, "port": form.port.data, "status": form.status.data, "active": form.active.data, "userId": form.userId.data}
        fact = json.dumps(sensor)
        r = sendRequest(method="post", url="/sensors", data=fact, auth=True)

        return redirect(url_for("sensor.index"))
    return render_template("sensorEdit_form.html", form=form)


@sensor.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(sensor, ".edit", "Edit Sensor")
def edit(id):

    form = SensorEditForm()
    req = sendRequest(method="get", url="/users", auth=True)
    users = [(item['id'], item['email']) for item in json.loads(req.text)["Users"]]
    form.userId.choices = users
    form.userId.choices.insert(0, [0, 'Select one user'])

    if not form.is_submitted():
        r = sendRequest(method="get", url="/sensor/"+str(id), auth=True)

        if r.status_code == 404:
            flash("Sensor not found", "danger")
            return redirect(url_for("sensor.index"))

        sensor = json.loads(r.text)

        form.name.data = sensor["name"]
        form.ip.data = sensor["ip"]
        form.port.data = sensor["port"]
        form.status.data = sensor["status"]
        form.active.data = sensor["active"]

        for user_id, user_email in users:
            if sensor["user"]["id"] == user_id:
                form.userId.data = int(user_id)

    if form.validate_on_submit():
        sensor = {"name": form.name.data, "ip": form.ip.data, "port": form.port.data, "status": form.status.data, "active": form.active.data, "userId": form.userId.data}
        fact = json.dumps(sensor)
        r = sendRequest(method="put", url="/sensor/" + str(id), data=fact, auth=True)
        flash("Sensor edited", "success")

        return redirect(url_for("sensor.index"))
    return render_template("sensorEdit_form.html", id=id, form=form)


@sensor.route("/delete/<int:id>")
@login_required
@admin_required
def delete(id):

    r = sendRequest(method="delete", url="/sensor/"+str(id), auth=True)
    flash("Sensor deleted", "danger")

    return redirect(url_for("sensor.index"))
