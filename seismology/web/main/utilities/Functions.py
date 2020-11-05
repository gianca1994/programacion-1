from flask import request, current_app, url_for, flash
from werkzeug.routing import RequestRedirect
import requests

def sendRequest(method, url, auth=False, data=None):

    headers = {"content-type": "application/json"}
   # if auth == True:
   #     token = request.cookies['access_token']
   #     headers["authorization"] = "Bearer " + token

    if method.lower() == "get":
        data = requests.get(current_app.config["API_URL"] + url, headers=headers,data=data)

    if method.lower() == "post":
        data = requests.post(current_app.config["API_URL"] + url, headers=headers, data=data)

    if method.lower() == "put":
        data = requests.put(current_app.config["API_URL"] + url, headers=headers, data=data)

    if method.lower() == "delete":
        data = requests.delete(current_app.config["API_URL"] + url, headers=headers)

    if data.status_code == 401 or data.status_code == 422:
        flash("Authorization token not valid. Please log in again", "warning")
        raise RequestRedirect(url_for("main.logout"))

    return data
