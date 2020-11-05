import os
from flask import Flask, flash, redirect, url_for
from dotenv import load_dotenv
from flask_breadcrumbs import Breadcrumbs
from flask_login import LoginManager
from .routes import main, verifseism, unverifseism, user, sensor


login_manager = LoginManager()

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("You need to login for continue.","warning")
    return redirect(url_for("main.index"))

def create_app():
    app = Flask(__name__)
    load_dotenv()

    # Configuraciones
    app.config["API_URL"] = os.getenv("API_URL")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    Breadcrumbs(app=app)
    login_manager.init_app(app)

    # Blueprints
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.verifseism.verifseism)
    #app.register_blueprint(routes.unverifseism.unverifseism)
    app.register_blueprint(routes.user.user)
    app.register_blueprint(routes.sensor.sensor)

    return app