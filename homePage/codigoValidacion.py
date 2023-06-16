import random
from django.utils import timezone
from django.utils.timezone import activate
import string
from .models import smsValidacionCelular


def generaCodigoValidacion(longitud):
    existe = True
    intentos = 0
    while (existe == True and intentos < 10):
        intentos = intentos + 1
        caracteres = string.ascii_uppercase + string.digits  # Letras mayúsculas y dígitos
        codigo = ''.join(random.choice(caracteres) for _ in range(longitud))
        if smsValidacionCelular.objects.filter(codigoValidacion=codigo).exists():
            existe = True
        else:
            existe = False
    if existe == True:
        codigo = ""
    return codigo


def almacenaCelularValidador(celular, codigoValidacion):
    registro = smsValidacionCelular()
    registro.celular = celular
    registro.codigoValidacion = codigoValidacion
    registro.fechaSolicitud = timezone.now()
    registro.estado = 1 #Default 0
    registro.save()
    return


def buscarCodigoEnBaseDatos(celularIngresado, codigoValidacionIngresado):
    ultimo_registro = smsValidacionCelular.objects.filter(
        celular=celularIngresado).latest('correlativo')

    if ultimo_registro.codigoValidacion == codigoValidacionIngresado and ultimo_registro.estado == 1:
        ultimo_registro.estado = 21
        ultimo_registro.save()
        return True

    else:
        return False
