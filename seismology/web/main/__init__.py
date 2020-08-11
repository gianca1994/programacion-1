import os
from flask import Flask
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['API_URL'] = os.getenv('API_URL')

    from .routes import main, verifseism
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.verifseism.verifseism)

    return app