from flask import request, flash, redirect, url_for
from flask_login import UserMixin, current_user
from functools import wraps
import jwt
from .. import login_manager

# Creamos esta clase para almacenar los datos del usuario previamente logueado.
class User(UserMixin):
    def __init__(self, id, email, admin):
        self.id = id; self.email = email; self.admin = admin

@login_manager.request_loader
def load_user(request):
    # Verificamos si hay cockies almacenadas.
    if "access_token" in request.cookies:
        try:
            # Decode token, cargamos los datos del usuario y devolvemos el user logueado..
            decoded = jwt.decode(request.cookies["access_token"], verify=False)
            user_data = decoded["user_claims"]
            user = User(user_data["id"], user_data["email"], user_data["admin"])
            return user
        except jwt.exceptions.InvalidTokenError:
            print("token invalid")
        except jwt.exceptions.DecodeError:
            print("DecodeError")
    return None

# Redireccionamos a la pagina main.index, la cual contiene el formulario de logueo, en caso de no haberse logueado.
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You must log in to continue','warning')
    return redirect(url_for('main.index'))

# Definimos admin_required para verificar si el usuario es admin, para poder aplicar las restricciones correspondientes.
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kws):
        print(current_user.admin)
        if not current_user.admin:
            flash('Access restricted to administrators.','warning')
            return redirect(url_for('main.index'))
        return fn(*args, **kws)
    return wrapper
