import random
import string

def encriptador(entrada_id, codigoseguridad):
    #entrada_id: 001001-00001
    #codigoseguridad: ABCD1234
    #validar longitudes 12 y 8
    if(len(entrada_id)!=12): return "No valido"
    if(len(codigoseguridad)!=8): return "No valido"

    return entrada_id+codigoseguridad

def desencriptador(cadena_encriptada):

    return [cadena_encriptada[:11],cadena_encriptada[11:]]