from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import SeismModel, SensorModel
from random import randint, uniform
import time
from flask_jwt_extended import jwt_required, get_jwt_identity


# -------------------------------------------------------------------------------------#
# Creamos la clase para verificar el recurso "Seism".
# -------------------------------------------------------------------------------------#

class VerifSeism(Resource):

    # Definimos "GET" para obtener un recurso de una coleccion y su "ID".
    def get(self, id):
        # Asignamos a la variable "verifseism" un seism traido de la db, si no existe, error 404.
        seism = db.session.query(SeismModel).get_or_404(id)

        if seism.verified:
            # Si el recurso existe, nos devolvera:
            return seism.to_json()

        # Sino, nos devuelve el error 403, Acceso denegado o Prohibido.
        else:
            return 'Access Denied', 403


# -------------------------------------------------------------------------------------#
# Creamos la clase para verificar la COLECCION de recursos "Seisms".
# -------------------------------------------------------------------------------------#

class VerifSeisms(Resource):

    # Luego definimos un "GET" para obtener la coleccion de seisms verificados.
   # @property
    def get(self):

        # Definimos la variable "page" para decir cuantas paginas tendremos.
        page = 1
        # Definimos "perpage" para decir cuantos sensores mostrara cada pagina.
        perpage = 3
        # Aca analizamos los datos y filtramos los Seisms verificados de la coleccion,"verified == True".
        seisms = db.session.query(SeismModel).filter(
            SeismModel.verified == True)

        if request.get_json():
            filter = request.get_json().items()

            # Definimos "for" para los filtros en las consultas...
            for key, value in filter:

                if key == "datetime":
                    seisms = seisms.filter(SeismModel.datetime == value)
                if key == "datetimeFrom":
                    seisms = seisms.filter(SeismModel.datetime >= value)
                if key == "datetimeTo":
                    seisms = seisms.filter(SeismModel.datetime <= value)

                if key == "sensorId":
                    seisms = seisms.filter(SeismModel.sensorId == value)
                if key == "magnitudeMax":
                    seisms = seisms.filter(SeismModel.magnitude <= value)
                if key == "magnitudeMin":
                    seisms = seisms.filter(SeismModel.magnitude == value)
                if key == "sensor.name":
                    seisms = seisms.join(SeismModel.sensor).filter(
                        SensorModel.name.like('%' + value + '%'))

                # ORDENAMIENTO
                # Utilizamos sort_by para ordenar todo de mayor a menor.
                if key == "shortby":
                    if value == "datetime":
                        seisms = seisms.order_by(SeismModel.dt)
                    if value == "datime.desc":
                        seisms = seisms.order_by(SeismModel.dt.desc())
                    if value == "sensor.name":
                        seisms = seisms.join(
                            SeismModel.sensor).orderby(SensorModel.name)
                    if value == "sensor.namedesc":
                        seisms = seisms.join(SeismModel.sensor).orderby(
                            SensorModel.name.desc())

                # Definimos los if dentro de for para paginas y cantidad de sismos mostrados por pagina.
                if key == "page":
                    page = value
                if key == "perpage":
                    perpage = value

        # Alojamos en la variable seisms, todos los sismos verificados obtenidos de las paginas.
        seisms = seisms.paginate(page, perpage, True, 500)

        # Con el return nos devolvera la coleccion de Seisms.
        return jsonify(
            {
                'Verif-seisms': [seism.to_json() for seism in seisms.items],
                'total': seisms.total,
                'pages': seisms.pages,
                'page': page,
            }
        )


# -------------------------------------------------------------------------------------#
# Creamos la clase para trabajar sobre algun recurso "UnverifSeism" de la coleccion.
# -------------------------------------------------------------------------------------#

class UnverifSeism(Resource):

    @jwt_required
    # Definimos "GET" para obtener un "UnverifSeism" con su id de la coleccion.
    def get(self, id):
        # Asignamos a la variable "seism" un seism traido de la db, si no existe, error 404.
        seism = db.session.query(SeismModel).get_or_404(id)

        # Si el seism no esta verificado entonces:
        if not seism.verified:

            # Nos devuelve los datos del "seism".
            return seism.to_json()

        else:
            # En caso de no existir, nos devuelve un error 403 "Prohibido (el servidor se niega a devolver el contenido)".
            return "Denied Access", 403

   # @jwt_required
    # Ahora para modifcar un recurso de la coleccion definimos un "PUT".
    def put(self, id):

        # Trae la coleccion de seism y la almacena en la variable seism.
        seism = db.session.query(SeismModel).get_or_404(id)
        # Extraemos los seism no verif a modificar de la info consultada, en formato json y guarda en "data".
        data = request.get_json().items()

        # si seism no esta verificado.
        if not seism.verified:
            # Utilizamos un FOR para recorrer el diccionario y evalua el contenido alojado en data.
            for key, value in data:
                setattr(seism, key, value)

            # Realiza la operacion
            try:
                # Agregamos un nuevo seism
                db.session.add(seism)
                # Actualiza la db.
                db.session.commit()
                # Nos devuelve el seism modificado con un codigo "201" (EXITO!).
                return seism.to_json(), 201

            # Si algo pasa o ocurre mal...
            except Exception as error:
                # Nos retorna el error "400 (Solicitud incorrecta)"
                return str(error), 400
        else:
            # Si no, nos devuelve el error "403 (Acceso denegado o Prohibido)"
            return "Denied Access", 403

   # @jwt_required
    # Por ultimo definimos un "delete" para borrar un seism no verificado de la coleccion.
    def delete(self, id):
        # Traemos de la coleccion de seisms un seism y lo alojamos en la variable, si no existe, error 404.
        seism = db.session.query(SeismModel).get_or_404(id)

        # Si el seism no esta verificado.
        if not seism.verified:
            # Deleteamos el seism y actualizamos la db.
            db.session.delete(seism)
            db.session.commit()

            # Y nos devuelve el cod. 204 con el mensaje:
            return "Unverif seism delete", 204
        # Si no.
        else:
            # Si no, nos devuelve el error "403 (Acceso denegado o Prohibido)"
            return "Denied Access", 403


# -------------------------------------------------------------------------------------#
# Creamos la clase para VER la COLECCION de recursos "Seism UnVerified" osea no verificados.
# -------------------------------------------------------------------------------------#

class UnverifSeisms(Resource):

   # @jwt_required
    # Aca definimos un "GET" para obtener la coleccion de UnverifSeisms.
    def get(self):

        # Definimos la variable "page" para decir cuantas paginas tendremos.
        page = 1
        # Definimos "perpage" para decir cuantos sismos mostrara cada pagina.
        perpage = 3

        # Traemos la coleccion de seisms, pero filtramos los seism verificados.

        seisms = db.session.query(SeismModel).filter(
            SeismModel.verified == False)

        if request.get_json():
            filters = request.get_json().items()

            # Utilizamos un FOR para recorrer el diccionario y evalua el contenido alojado en filters.
            for key, value in filters:
                # Utilizamos condicionales para filtrar por partes...
                if "datetime" in filters:
                    seisms = seisms.filter(SeismModel.datetime == value)
                if key == "datetimeFrom":
                    seisms = seisms.filter(SeismModel.datetime >= value)
                if key == "datetimeTo":
                    seisms = seisms.filter(SeismModel.datetime <= value)
                if key == "sensorId":
                    seisms = seisms.filter(SeismModel.sensorId == value)
                if key == "magnitude":
                    seisms = seisms.filter(SeismModel.magnitude == value)
                if key == "depth":
                    seisms = seisms.filter(SeismModel.depth == value)

                # ORDENAMIENTO
                # Utilizamos sort_by para ordenar todo de mayor a menor.
                if key == "sort_by":
                    if value == "datetime":
                        seisms = seisms.order_by(SeismModel.datetime)
                    # Se agrega datetime.desc para realizar el ordenamiento y se almacena en la variable.
                    if value == "datetime.desc":
                        seisms = seisms.order_by(SeismModel.datetime.desc())
                    if value == "sensorname":
                        seisms = seisms.join(SeismModel.sensor).order_by(
                            SensorModel.name.asc())
                    if value == "sensorname.desc":
                        seisms = seisms.join(SeismModel.sensor).order_by(
                            SensorModel.name.desc())

                    if value == "magnitude":
                        seisms = seisms.order_by(SeismModel.magnitude.asc())
                    if value == "magnitude.desc":
                        seisms = seisms.order_by(SeismModel.magnitude.desc())
                    if value == "depth":
                        seisms = seisms.order_by(SeismModel.depth.asc())
                    if value == "depth.desc":
                        seisms = seisms.order_by(SeismModel.depth.desc())

                    # Definimos los if dentro de for para la paginacion de sismos no verificados mostrados por pagina.
                    if key == "page":
                        page = int(value)
                    if key == "per_page":
                        perpage = int(value)

        # Alojamos en la variable seisms, todos los sismos obtenidos de las paginas.
        seisms = seisms.paginate(page, perpage, True, 100)

        # Nos devuelve la coleccion con los seisms no verificados filtrados.
        return jsonify(
            {
                "Unverif-seisms": [seism.to_json() for seism in seisms.items],
                "total": seisms.total,
                "pages": seisms.pages,
                "page": page
            }
        )

  #  @jwt_required
    # Definimos "POST" para agregar un seisms no verificado a la coleccion.
    def post(self):

        # Traemos la coleccion de seisms completa y la alojamos en la variable, si no existe, error 404.
        sensors = db.session.query(SensorModel).all()
        sensorlist = [(int(sensor.id)) for sensor in sensors]

        if sensorlist:
            value_sensor = {
                'datetime': time.strftime(r'%Y-%m-%d %H:%M:%S', time.localtime()),
                'depth': randint(5, 250),
                'magnitude': round(uniform(2.0, 5.5), 1),
                'latitude': uniform(-180, 180),
                'longitude': uniform(-90, 90),
                'verified': False,
                'sensorId': sensorlist[randint(0, len(sensorlist) - 1)]
            }

            seism = SeismModel.from_json(value_sensor)
            # Agregamos el seism a la db.
            db.session.add(seism)
            # Actualizamos la db.
            db.session.commit()

        else:
            # Sino nos devuelve el error "400 (Solicitud incorrecta)"
            return 'Sensors not found, cant create seism', 400

        # Retornamos el seism en formato json con el codigo "201 (Nuevo recurso Creado)"
        return seism.to_json(), 201
