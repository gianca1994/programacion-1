from flask_jwt_extended import verify_jwt_in_request, get_jwt_claims
from .. import jwt
from functools import wraps

# Definimos admin_required para otorgarle a un usuario accesos a ciertos lugares que requieren privilegios


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Verificamos la solicitud de jwt y la almacenamos en la variable "claims".
        verify_jwt_in_request()
        claims = get_jwt_claims()

        # Si el usuario es "admin"
        if claims["admin"]:
            # recibimos el acceso
            return fn(*args, **kwargs)
        # Si no...
        else:
            # Nos retorna un error 403 y nos dice que solo los administradores pueden acceder.
            return "Admins can access", 403
    return wrapper


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {
        "id": user.id,
        "email": user.email,
        "admin": user.admin
    }
