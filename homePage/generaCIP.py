import random
import string
from .models import Pagos

def generaCIP(longitud):
    existe   = True
    intentos = 0 
    while (existe == True and intentos<10):
        intentos   = intentos + 1
        caracteres = string.digits  # Letras mayúsculas, minúsculas y dígitos
        codigo     = ''.join(random.choice(caracteres) for _ in range(longitud))
        if Pagos.objects.filter(cip=codigo).exists():
            existe = True
            #print("Paso por True en generaCodigoValidacion. Intento:"+str(intentos))
        else:
            existe = False

    return codigo