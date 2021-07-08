from .. import db
from main.models import UserModel, SensorModel
from flask import request, Blueprint
from flask_jwt_extended import create_access_token
from main.mail.functions import sendMail
from main.auth.decorators import admin_required

# pip install fpdf
#from fpdf import FPDF
# pip install reportlab
#from reportlab.pdfgen.canvas import Canvas


# Utilizamos Blueprint para generar rutas y lo almacenamos en la variable auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

# La función integrada nos permitirá definir la ruta para el login y el metodo POST, escritura...


@auth.route('/login', methods=['POST'])
# Definimos el login, para el inicio de sesion del usuario
def login():
    # Validamos si hay un email duplicado y alojamos en la variable user. Si hay un duplicado nos da error 404.
    user = db.session.query(UserModel).filter(
        UserModel.email == request.get_json().get('email')).first_or_404()

    # Definimos el "If" para verificar si la contraseña ingresada es correcta.
    if user.validate_pass(request.get_json().get('password')):

        # Utilizamos "create_access_token" para crear un token para que el usuario lo use cuando quiera hacer
        # acciones que requieran autenticaciony lo almacenamos en la variable...
        access_token = create_access_token(identity=user)

        # Alojamos el id, email y token de acceso en la variable data
        data = '{"id":"' + str(user.id) + '","email":"' + \
            str(user.email) + '","access_token":"' + access_token + '"}'

        # Nos devueve la variable con todos los datos dentro y el codigo 200.
        return data, 200
    # Si no
    else:
        # Nos devuelve error 401 "Contraseña incorrecta"
        return 'Incorrect password', 401

# Register eliminado, porque estabamos duplicando la misma accion...

    # La función integrada nos permitirá definir la ruta para el checkeo y el metodo GET, lectura.


@auth.route("/checksensors", methods=["GET"])
# La función integrada nos permitirá decir que solo los admins pueden ingresar a esta seccion.
#@admin_required
# Definimos checkStatus para...
def checkStatus():
    # Alojamos en sensors, todos los sensores de la db filtrados por active y status.
    sensors = (db.session.query(SensorModel).filter(
        SensorModel.active == True).filter(SensorModel.status == False).all())
    # Definimos los IF para el envio de emails.
    if sensors:
        # Alojamos en la variable admins, los usuarios traidos de la db, filtrados por "admin"
        admins = db.session.query(UserModel).filter(
            UserModel.admin == True).all()

        if admins:
            adminList = [admin.email for admin in admins]

            # Almacenar la lista de sensores desactivados en una variable..
            # Tengo que escribir un nuevo archivo .pdf en el cual, su contenido sera la variable definida...

            # OPCION 1
            # Pip install fpdf
            # Importamos FPDF de fpdf para crear el archivo.pdf
            #from fpdf import FPDF
            # Primero crearemos nuestro archivo PDF, usando la biblioteca FṔDF
            # Creamos la variable y guardamos la clase FPDF()
      #      SensorsListpdf = FPDF()
            # Agregamos una pagina al archivo pdf, para poder almacenar la lista de sensores
      #      SensorsListpdf.add_page()
            # Elegimos el tipo de letra y tamaño
      #      SensorsListpdf.set_font("Arial", size=12)
            # Me faltaria agregar la lista de los sensores fallando al archivo...
      #      SensorsDesactivated = jsonify({"sensors": [sensor.to_json() for sensor in sensors]})
      #      SensorsListpdf.cell(SensorsDesactivated)
            # Guardamos la informacion con output en el archivo.pdf
      #      SensorsListpdf.output('SensorList.pdf')
            # Adjuntar el archivo.PDF
      #      attach(filename=SensorList, content_type=application/pdf, data=SensorsList, disposition=None, headers=None)

            # OPCION 2
            # pip install reportlab
            # from reportlab.pdfgen.canvas import Canvas
            # Creamos el archivo PDF con canvas y lo almacenamos en la variable
      #      SensorsList=Canvas('SensorList.pdf')
            # Escribimos la variable con los datos de los sensores
      #      SensorsDesactivated=jsonify({"sensors": [sensor.to_json() for sensor in sensors]})
      #      SensorsList.drawString(0, 0,SensorsDesactivated)
            # Guardamos los datos de los sensores en el archivo..
      #      SensorsList.save()
            # Adjuntamos la variable al email
      #      msg.attach(filename=SensorsList, content_type=application/pdf, data=sensors, disposition=None, headers=None)

            # Enviamos el email con el archivo adjunto
            sendMail(adminList, "Deactivated sensors",
                     "mail/sensor", sensorList=sensors)

        # Nos retorna los datos del sensor
        return "There're no sensors", 200
    else:
        return "There're no deactivated sensors", 200
