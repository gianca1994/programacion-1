from flask import current_app, render_template
from flask_mail import Message
from .. import sendmail
from smtplib import SMTPException

# Definimos sendMail con las variables: to (destinatario), subject (asunto), template (ubicacion y nombre del
# template del mail) y **kwargs (serie de argumentos).
def sendMail(to,subject, template, adj, **kwargs):
    # Definimos un mensaje con el objeto "Message" del flask_mail, le pasamos el asunto, quien lo envia y receptores
    msg = Message(subject, sender=current_app.config["FLASKY_MAIL_SENDER"], recipients=[to])
    try:
        # Definimos body (texto plano) y html (estilo con css) dependiendo del soporte del cliente de correo usa uno u otro.
        msg.body = render_template(template + ".txt", **kwargs)
        msg.html = render_template(template + ".html", **kwargs)

        # Envia el mensaje
        result = sendmail.send(msg)

    # En caso de salir un error SMTP (error de autenticacion o fallo al conectar al servidor)
    except SMTPException as error:
        print(str(error))
        return "Mail deliver failed" + str(error)
    return True