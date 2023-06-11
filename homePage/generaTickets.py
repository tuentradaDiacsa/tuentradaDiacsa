from .models import Tickets

def generaNumeroTicket():
    cadenaCiudad = "001"
    cadenaEvento = "001"
    separador    = "-"
    num          = Tickets.objects.count()+1
    correlativo  = str(num).zfill(5)
    IDEntrada    = cadenaCiudad+cadenaEvento+separador+correlativo
    return IDEntrada