import os
from flask import Flask
from dotenv import load_dotenv
from flask_restful import Api

import main.resources as resources

api = Api()

def create_app():
    app = Flask(__name__)
    load_dotenv()
    api.add_resource(resources.VerifiedSeismsResource, '/verified-seisms')
    api.add_resource(resources.UnverifiedSeismsResource, '/unverified-seisms')
    api.add_resource(resources.SensorsResource, '/sensors')
    api.add_resource(resources.VerifiedSeismResource, '/verified-seisms/<id>')
    api.add_resource(resources.UnverifiedSeismResource, '/unverified-seisms/<id>')
    api.add_resource(resources.SensorResource, '/sensors/<id>')
    api.init_app(app)
    return app
