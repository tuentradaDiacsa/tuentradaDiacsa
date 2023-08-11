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

def generaCodigoValidacionNumeros(longitud):
    existe = True
    intentos = 0
    while (existe == True and intentos < 10):
        intentos = intentos + 1
        caracteres = string.digits  # Letras mayúsculas y dígitos
        codigo = ''.join(random.choice(caracteres) for _ in range(longitud))
        if smsValidacionCelular.objects.filter(codigoValidacion=codigo).exists():
            existe = True
        else:
            existe = False
    if existe == True:
        codigo = ""
    return codigo


def almacenaCelularValidador(celular, codigoValidacion, estado):
    registro = smsValidacionCelular()
    registro.celular = celular
    registro.codigoValidacion = codigoValidacion
    registro.fechaSolicitud = timezone.now()
    registro.estado = estado #Default 0
    registro.save()
    return


def buscarCodigoEnBaseDatos(celularIngresado, codigoValidacionIngresado, estado):
    ultimo_registro = smsValidacionCelular.objects.filter(
        celular=celularIngresado, estado=estado).latest('correlativo')

    if ultimo_registro.codigoValidacion == codigoValidacionIngresado and ultimo_registro.estado == 1:
        ultimo_registro.estado = 21
        ultimo_registro.save()
        return True
    
    elif ultimo_registro.codigoValidacion == codigoValidacionIngresado and ultimo_registro.estado == 2:
        ultimo_registro.estado = 22
        ultimo_registro.save()
        return True

    elif ultimo_registro.codigoValidacion == codigoValidacionIngresado and ultimo_registro.estado == 3:
        ultimo_registro.estado = 23
        ultimo_registro.save()
        return True

    else:
        return False
