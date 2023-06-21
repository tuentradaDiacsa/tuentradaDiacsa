from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

# ENTRADA:
# key   ->  debe ser string de 16 caracteres.
#           es la llave secret para encriptar y desencriptar.
# entrada_id        -> 12 caracateres. Ejemplo: "001001-00001"
# codigoseguridad   ->   8 caracteres. Ejemplo: "XBCD1234"
#
# SALIDA:
# cifrado -> 64 caracteres (hex text)
def encriptador(key,entrada_id, codigoseguridad):    
    if len(key)!=16: return "No valido"
    if len(entrada_id)!=12: return "No valido"
    if entrada_id[6:7]!="-": return "No valido"
    if len(codigoseguridad)!=8: return "No valido"

    keyb =  bytes(key, 'utf-8')
    temp=entrada_id[0:6]+"0"+entrada_id[7:12]
    llano = bytes.fromhex(temp)+ bytes(codigoseguridad,'utf-8')+get_random_bytes(2)

    cipher = AES.new(keyb, AES.MODE_CBC)
    cifrado = cipher.encrypt(llano)
    iv = cipher.iv
    return iv.hex()+cifrado.hex()


def desencriptador(key,cadena_encriptada):
    if len(key)!=16: return "No valido"
    if len(cadena_encriptada)!=64: return "No valido"

    keyb =  bytes(key, 'utf-8')
    iv=bytes.fromhex(cadena_encriptada[0:32])

    decrypt_cipher = AES.new(keyb, AES.MODE_CBC, iv)
    llano = decrypt_cipher.decrypt(bytes.fromhex(cadena_encriptada[32:64]))

    temp = llano[0:6].hex()
    entrada_id=temp[0:6]+"-"+temp[7:12]
    codigoseguridad = bytes.decode(llano[6:14], 'utf-8')
    return entrada_id,codigoseguridad