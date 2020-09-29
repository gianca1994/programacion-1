from flask import Blueprint, render_template, current_app, redirect, url_for
from flask_breadcrumbs import register_breadcrumb
import requests, json
from flask_login import login_required, LoginManager
from ..utilities.functions import sendRequest
from .auth import admin_required
from ..forms.sensor_form import SensorCreateForm, SensorEditForm, SensorFilterForm


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
    data = {}

    if filter.validate():
        if filter.name.data != None:
            data['name'] = filter.name.data
        if filter.status.data != None:
            data['status'] = filter.status.data
        if filter.active.data != None:
            data['active'] = filter.active.data
        if filter.userId.data != None and filter.userId.data != 0:
            data['userId'] = filter.userId.data
    if 'page' in request.args:
        data['page'] = request.args.get('page', '')
    if 'sort_by' in request.args:
        data['sort_by'] = request.args.get('sort_by', '')

    r = sendRequest(method="get", url="/sensors", data=json.dumps(data), auth=True)

    if (r.status_code == 200):
        sensors = json.loads(r.text)["sensors"]
        pagination = {}
        pagination['total'] = json.loads(r.text)['total']
        pagination['pages'] = json.loads(r.text)['pages']
        pagination['current_page'] = json.loads(r.text)['page']
        title = "Sensors"

        return render_template("sensors.html", title=title, sensors=sensors, filter=filter, pagination=pagination)
    else:
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
        data = json.dumps(sensor)
        r = sendRequest(method="post", url="/sensors", data=data, auth=True)

        return redirect(url_for("sensor.index"))
    return render_template("sensorEdit_form.html", form=form)


@sensor.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
@register_breadcrumb(sensor, ".edit", "Edit Sensor")
def edit(id):

    form = SensorEditForm()
    req = sendRequest(method="get", url="/users", auth=True)
    users = [(item['id'], item['email'])

             for item in json.loads(req.text)["Users"]]
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

        try:
            user = sensor["user"]
            form.userId.data = [int(user_id)
                                for user_id in users if user_id == int(user["id"])]
        except KeyError:
            pass

    if form.validate_on_submit():
        sensor = {"name": form.name.data, "ip": form.ip.data, "port": form.port.data, "status": form.status.data, "active": form.active.data, "userId": form.userId.data}
        data = json.dumps(sensor)
        r = sendRequest(method="put", url="/sensor/" + str(id), data=data, auth=True)
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