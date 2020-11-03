from main import create_app
from main import db
import os, threading
#from .main.Utilities.SensorSockets import callSensors


app = create_app()
app.app_context().push()

if __name__ == '__main__':
    # Crea el esquema de la base de datos...
    db.create_all()
 #   threading.Thread(target=callSensors, args=(app,)).start()
    # Inicia la aplicacion.
    app.run(debug=True, port=os.getenv('PORT'))