from main import create_app
from dotenv import load_dotenv
from main import db
import os

load_dotenv()
app = create_app()
app.app_context().push()

if __name__ == '__main__':
    # Toma los modelos y crea las tablas en el archivo.
    db.create_all()

    app.run(debug=True, port=os.getenv('PORT'))
