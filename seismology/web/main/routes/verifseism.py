from flask import Blueprint, redirect, render_template, request, url_for, flash, make_response
from flask_breadcrumbs import register_breadcrumb
from ..forms.frmLogin import LoginForm
import requests, json, io, csv
from ..utilities.Functions import sendRequest
from ..forms.frmSeisms import SeismFilterForm

verifseism = Blueprint("verifseism", __name__, url_prefix="/verified-seism")

@verifseism.route("/")
def index():
    frmLogin = LoginForm()
    filter = SeismFilterForm(request.args, meta={"csrf": False})
    r = sendRequest(method="get", url="/sensors-info")
    filter.sensorId.choices = [
        (int(sensor["id"]), sensor["name"]) for sensor in json.loads(r.text)["sensors"]
    ]
    filter.sensorId.choices.insert(0, [0,"All"])
    fact = {}

    if filter.validate():
        if filter.datetimeFrom.data and filter.datetimeTo.data:
            if filter.datetimeFrom.data == filter.datetimeTo.data:
                fact["datetime"] = filter.datetimeTo.data.strftime("%Y-%m-%d %H:%M")
        if filter.datetimeFrom.data != None:
            fact["datetimeFrom"] = filter.datetimeFrom.data.strftime("%Y-%m-%d %H:%M")
        if filter.datetimeTo.data != None:
            fact["datetimeTo"] = filter.datetimeTo.data.strftime("%Y-%m-%d %H:%M")

        if filter.sensorId.data != None and filter.sensorId.data != 0:
            fact["sensorId"] = filter.sensorId.data
        if filter.depth_min.data != None:
            fact["depth_min"] = filter.depth_min.data
        if filter.depth_max.data != None:
            fact["depth_max"] = filter.depth_max.data
        if filter.magnitude_min.data != None:
            fact["magnitude_min"] = filter.magnitude_min.data
        if filter.magnitude_max.data != None:
            fact["magnitude_max"] = filter.magnitude_max.data

    if "sort_by" in request.args:
        data["sort_by"] = request.args.get("sort_by", "")

    if "download" in request.args:
        if request.args.get("download", "") == "Download":
            codeOK = 200
            page = 1
            SeismList = []

            while codeOK == 200:
                data["page"] = page
                r = sendRequest(method="get", url="/verified-seisms", data=json.dumps(data))
                codeOK = r.status_code

                if codeOK == 200:
                    for seism in json.loads(r.text)["Verified-seisms"]:
                        element = {"datetime": seism["datetime"], "depth": seism["depth"], "magnitude": seism["magnitude"],
                            "latitude": seism["latitude"], "longitude": seism["longitude"], "sensor.name": seism["sensor"]["name"]}
                        SeismList.append(element)
                page += 1

            si = io.StringIO()
            fc = csv.DictWriter(si, fieldnames=SeismList[0].keys())
            fc.writeheader()
            fc.writerows(SeismList)

            output = make_response(si.getvalue())
            output.headers["Content-Disposition"] = "attachment; filename=seisms.csv"
            output.headers["Content-type"] = "text/csv"
            return output

    if "page" in request.args:
        data["page"] = request.args.get("page", "")
    else:
        if "page" in data:
            del data["page"]

    r = sendRequest(method="get", url="/verified-seisms", data=json.dumps(data))

    if r.status_code == 200:
        verified_seisms = json.loads(r.text)["Verified-seisms"]
        paginate = {}
        paginate["total"] = json.loads(r.text)["total"]
        paginate["pages"] = json.loads(r.text)["pages"]
        paginate["current_page"] = json.loads(r.text)["page"]
        title = "Verified Seisms List"
        return render_template("verified-seisms.html", title=title, verified_seisms=verified_seisms, loginForm=loginForm, filter=filter, pagination=paginate)
    else:
        flash("Filtering Error", "danger")
        return redirect(url_for("verified_seism.index"))


@verifseism.route("/view/<int:id>")
@register_breadcrumb(verifseism, ".view", "View")
def view(id):
    r = sendRequest(method="get", url="/verified-seism/" + str(id))

    if (r.status_code == 404):
        return redirect(url_for("verified_seism.index"))

    verified_seism = json.loads(r.text)
    title = "Verified Seism View"
    loginForm = LoginForm()

    return render_template("verified-seism.html", title=title, verified_seism=verified_seism, loginForm=loginForm)
