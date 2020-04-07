from flask_restful import Resource
from flask import request

VERIFIED_SEISMS = {
    1: {'datatime': '25/11/2019', 'magnitude': '3.3'},
    2: {'datatime': '10/12/2019', 'magnitude': '1.6'},
}

UNVERIFIED_SEISMS = {
    1: {'datetime': '08/02/2020', 'magnitude': '2.5'},
    2: {'datatime': '12/03/2020', 'magnitude': '5.0'},
}

#RECURSO VERIFIEDSEISM
class VerifiedSeism(Resource):
    #OBTENER RECURSO
        def get(self, id):
            if int(id) in VERIFIED_SEISMS:
                return VERIFIED_SEISMS[int(id)]
            return 'Seism not found', 404

#RECURSO VERIFIEDSEIMS
class VerifiedSeisms(Resource):
    #OBTENER LISTA DE RECURSOS
        def get(self):
            return VERIFIED_SEISMS

class UnverifiedSeism(Resource):
    #OBTENER RECURSO
        def get(self, id):
            if int(id) in UNVERIFIED_SEISMS:
                return UNVERIFIED_SEISMS[int(id)]
            return 'Seism not found', 404

#MODIFICAR RECURSO
    def put(self, id):
        if int(id) in UNVERIFIED_SEISMS:
            seism = UNVERIFIED_SEISMS[int(id)]
            data = request.get_json()
            seism.update(data)
            return seism, 201
        return 'Seism not found', 404

#ELIMINAR RECURSO
    def delete(self, id):
        if int(id) in UNVERIFIED_SEISMS:
            del UNVERIFIED_SEISMS[int(id)]
                return 'Successful deletion', 204
        return 'Seism not found', 404

class UnverifiedSeisms(Resource):
#OBTENER LISTA DE RECURSOS
    def get(self):
        return UNVERIFIED_SEISMS
