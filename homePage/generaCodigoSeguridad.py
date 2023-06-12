import random
import string
from .models import Tickets

def generacodigoseguridad():
    existe   = True
    intentos = 0 
    while (existe == True and intentos<10):
        intentos   = intentos + 1
        caracteres = string.ascii_uppercase + string.digits  # Letras mayúsculas y dígitos
        codigo     = ''.join(random.choice(caracteres) for _ in range(8))

        if Tickets.objects.filter(codigoseguridad=codigo).exists():
            existe = True
            #print("Paso por True en generaCodigoValidacion. Intento:"+str(intentos))
        else:
            existe = False
    if existe == True:
        codigo=""
    return codigo