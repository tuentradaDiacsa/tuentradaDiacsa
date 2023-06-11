import random
import string
from .models import smsValidacionCelular

def generaCodigoValidacion(longitud):
    existe   = True
    intentos = 0 
    while (existe == True and intentos<10):
        intentos   = intentos + 1
        caracteres = string.ascii_uppercase + string.digits  # Letras mayúsculas y dígitos
        codigo     = ''.join(random.choice(caracteres) for _ in range(longitud))
        #print("Codigo generado = "+codigo)
        #codigo     = "963741"
        #print("Comparacion forzada con uno igual")
        if smsValidacionCelular.objects.filter(codigoValidacion=codigo).exists():
            existe = True
            #print("Paso por True en generaCodigoValidacion. Intento:"+str(intentos))
        else:
            existe = False
    if existe == True:
        codigo=""
    return codigo

def almacenaCelularValidador(celular,codigoValidacion):
    registro = smsValidacionCelular()
    
    registro.celular          = celular
    registro.codigoValidacion = codigoValidacion
    registro.save()
    return

def buscarCodigoEnBaseDatos(celularIngresado, codigoValidacionIngresado):
    if smsValidacionCelular.objects.filter(celular = celularIngresado, codigoValidacion=codigoValidacionIngresado, estado=0).exists():
        return True
    else:
        return False