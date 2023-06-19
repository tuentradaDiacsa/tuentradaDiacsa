from django.shortcuts import render, redirect
from homePage.models import Preguntas, Tipos, Tickets, Pagos, boxesRestante1, boxesRestante2, boxesRestante3
from .codigoValidacion import generaCodigoValidacion
from .codigoValidacion import almacenaCelularValidador, buscarCodigoEnBaseDatos
from .generaTickets import generaNumeroTicket
from .generaCIP import generaCIP
from django.http import JsonResponse

from .models import Pagos
from django.http import FileResponse

from django.http import HttpResponse
import io
import qrcode
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pdfkit
from django.template.loader import render_to_string

from django.utils import timezone
from django.utils.timezone import activate
import pytz

import base64
from django.conf import settings
from io import BytesIO
from xhtml2pdf import pisa
import os
from django.contrib.sites.shortcuts import get_current_site
from django.views import View

from .encripdecripEntradas import encriptador
from .generaCodigoSeguridad import generacodigoseguridad

import re

def reemplazar_letras(cadena):
    # Utilizar expresiones regulares para buscar palabras y reemplazar letras
    resultado = re.sub(r'\b(\w)(\w+)(\w)\b', lambda match: match.group(1) + 'x' * len(match.group(2)) + match.group(3), cadena)
    return resultado

def reemplazar_ultimos_caracteres(cadena):
    longitud = len(cadena)
    if(longitud==1):
        return "X"
    if(longitud==2):
        return cadena[0]+"X"
    if(longitud==3):
        return cadena[0]+"X"+cadena[2]
    if(longitud==4):
        return cadena[0]+"XX"+cadena[3]
    if(longitud==5):
        return cadena[0]+"XXX"+cadena[4]
    if(longitud==6):
        return cadena[0]+"XXXX"+cadena[5]
    if(longitud>=7):
        return cadena[:-6]+"XXXX"+cadena[-2:]
    return cadena

def generar_qr_code_url(datoencriptado):
    data = datoencriptado#"Ticket: {}, CIP: {}".format(ticket, cip)
    qr   = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image  = qr.make_image(fill="black", back_color="white")
    qr_buffer = io.BytesIO()
    qr_image.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    return qr_buffer

def descargar_boleto(request, entrada_id):
    try:
        ticket_obj = Tickets.objects.get(ticket=entrada_id)

        if(getattr(ticket_obj, 'numeroBox', '0') !='0'): numeroBox = " - Box "+getattr(ticket_obj, 'numeroBox', '0')
        else: numeroBox = ""

        if(getattr(ticket_obj, 'nombre', 'No completado')!="No completado"): campoNombreApellido = reemplazar_letras(getattr(ticket_obj, 'nombre', 'No completado'))
        else: campoNombreApellido = "No completado"

        if(getattr(ticket_obj, 'dni', 'No completado')!="No completado"): campodni = reemplazar_ultimos_caracteres(getattr(ticket_obj, 'dni', 'No completado'))
        else: campodni = "No completado"
        
        if(getattr(ticket_obj, 'celular', 'No completado')!="No completado"): campocelular = reemplazar_ultimos_caracteres(getattr(ticket_obj, 'celular', 'No completado'))
        else: campocelular = "No completado"

        context = {
            'ID_Ticket': entrada_id,
            'nombre_y_apellido': campoNombreApellido,
            'dni': campodni,
            'telefono': campocelular,
            'whatsapp': campocelular,
            'Lugar': "Centro Convenciones del Pardo",
            'Ubicacion': "Calle Alzamora / Av. Mariscal Cáceres",
            'fecha': "Domingo 25 de Junio 2023",
            'hora': "3:00 pm",
            'Zona': getattr(ticket_obj, 'tipo', 'No completado')+numeroBox,
            #'qr_image': qr_url,
        }

    except Tickets.DoesNotExist:
        return HttpResponse("No se crearon los tickets correctamente o hubo problemas en la búsqueda")

    html_content = render_to_string('entradas/plantillaentrada1.html', context)

    return HttpResponse(html_content)  # response

def homePage(request):
    return render(request, "homePage/homePage.html")

def armaEntradas(cipBuscaTickets):
    ticketSxCIP = Tickets.objects.filter(cip=cipBuscaTickets)
    entradasArgumento = []
    for ticketCIP in ticketSxCIP:
        auxiliar = {}
        auxiliar["tipo_ticket"]   = ticketCIP.tipo #Tiene la descripcion
        auxiliar["numero_ticket"] = ticketCIP.ticket
        entradasArgumento.append(auxiliar)
    return entradasArgumento

class comprarPage(View):
    def get(self, request):
        preguntas = Preguntas.objects.all()
        entradas  = Tipos.objects.all().order_by('tipo')

        boxes1    = boxesRestante1.objects.all().order_by('box')
        boxes2    = boxesRestante2.objects.all().order_by('box')
        boxes3    = boxesRestante3.objects.all().order_by('box')
        datos = {
            'preguntas': preguntas,
            'entradas' : entradas,
            'boxes1'   : boxes1,
            'boxes2'   : boxes2,
            'boxes3'   : boxes3
        }
        identifica_compra = request.session.get('compra_redirect', False)
        if (identifica_compra):
            # print(request.session['compra_redirect'])
            del (request.session['compra_redirect'])
            contexto = request.session['contexto']
            del (request.session['contexto'])
            #ticketsGenerados = request.session['ticketsGenerados']
            #del (request.session['ticketsGenerados'])
            return render(request, "resumenPage/resumenPage.html", contexto)
        identifica_tickets = request.session.get('tickets_redirect', False)
        if (identifica_tickets):
            del (request.session['tickets_redirect'])
            contexto = request.session['contexto']
            del (request.session['contexto'])
            return render(request, "ticketsCompradosPage/ticketsCompradosPage.html", contexto)
        return render(request, "comprarPage/comprarPage.html", datos)

    def post(self, request):
        if request.method == 'POST':
            preguntas = Preguntas.objects.all()
            entradas  = Tipos.objects.all().order_by('tipo')
            boxes1    = boxesRestante1.objects.filter(ocupado=False)
            boxes2    = boxesRestante2.objects.filter(ocupado=False)
            boxes3    = boxesRestante3.objects.filter(ocupado=False)
            datos = {
                'preguntas': preguntas,
                'entradas' : entradas,
                'boxes1'   : boxes1,
                'boxes2'   : boxes2,
                'boxes3'   : boxes3
            }
            print("POST ")
            if request.POST.get('boton') == 'sms':
                print("Boton SMS presionado")
                celular = request.POST.get('celular')
                datos['celular'] = celular
                codigoValidacion = generaCodigoValidacion(6)
                if codigoValidacion == "":
                    print(
                        "Error!!! No se pudo generar codigo de validacion NO REPETIDO")
                else:
                    print("Boton SMS presionado", "Celular:",
                          celular, "Codigo:", codigoValidacion)
                    almacenaCelularValidador(celular, codigoValidacion)
                
                return render(request, "comprarPage/comprarPage.html", datos)

            elif request.POST.get('comando') == 'leerCantidadEntradas':
                entradas  = Tipos.objects.all().order_by('tipo')
                boxes1    = boxesRestante1.objects.filter(ocupado=False).order_by('box')
                boxes2    = boxesRestante2.objects.filter(ocupado=False).order_by('box')
                boxes3    = boxesRestante3.objects.filter(ocupado=False).order_by('box')
                boxes1N    = boxesRestante1.objects.filter(ocupado=True).order_by('box')
                boxes2N    = boxesRestante2.objects.filter(ocupado=True).order_by('box')
                boxes3N    = boxesRestante3.objects.filter(ocupado=True).order_by('box')
                
                entradasRestantes   = []
                entradasDescripcion = []

                for entrada in entradas:
                    entradasRestantes.append(entrada.cantidad)
                    entradasDescripcion.append(entrada.descripcion)
                
                boxes1Restantes   = []
                for box in boxes1:
                    boxes1Restantes.append(box.box)
                boxes2Restantes   = []
                for box in boxes2:
                    boxes2Restantes.append(box.box)
                boxes3Restantes   = []
                for box in boxes3:
                    boxes3Restantes.append(box.box)    


                boxes1Ocupados   = []
                for box in boxes1N:
                    boxes1Ocupados.append(box.box)
                boxes2Ocupados   = []
                for box in boxes2N:
                    boxes2Ocupados.append(box.box)
                boxes3Ocupados   = []
                for box in boxes3N:
                    boxes3Ocupados.append(box.box)   
                responseData = {
                    'entradasDescripcion' : entradasDescripcion,
                    'entradasRestantes'   : entradasRestantes,
                    'boxes1Restantes'     : boxes1Restantes,
                    'boxes2Restantes'     : boxes2Restantes,
                    'boxes3Restantes'     : boxes3Restantes,
                    'boxes1Ocupados'     : boxes1Ocupados,
                    'boxes2Ocupados'     : boxes2Ocupados,
                    'boxes3Ocupados'     : boxes3Ocupados,
                }
                return JsonResponse(responseData)

            elif request.POST.get('boton') == 'verificar':
                print("Boton verificar presionado")
                celular = request.POST.get('celular')
                datos['celular'] = celular
                codigoValidacionIngresado = request.POST.get('codigo')
                datos['codigo'] = codigoValidacionIngresado
                responseData = {'data': 'Codigo incorrecto'}
                if (buscarCodigoEnBaseDatos(celular, codigoValidacionIngresado)):
                    print("Codigo Correcto!!!")
                    responseData = {'data': 'Codigo correcto'}
                return JsonResponse(responseData)
            
##########################################################
            elif request.POST.get('boton') == 'comprar':
                print("POST COMPRAR ENTRADA")
                
                celular    = request.POST.get('celular')
                codigo     = request.POST.get('codigo')
                pin        = request.POST.get('pin')
                nombre     = request.POST.get('nombre')
                dni        = request.POST.get('dni')
                correo     = request.POST.get('correo')
                pregunta1  = request.POST.get('pregunta1')
                respuesta1 = request.POST.get('respuesta1')
                pregunta2  = request.POST.get('pregunta2')
                respuesta2 = request.POST.get('respuesta2')
                pregunta3  = request.POST.get('pregunta3')
                respuesta3 = request.POST.get('respuesta3')
                box1       = request.POST.get('boxes1') #Box Izquierdo 4
                box2       = request.POST.get('boxes2') #Box Derecho Tipo 5
                box3       = request.POST.get('boxes3') #Box Alimanha Tipo 6
                cip        = generaCIP(6)
                arregloEntradas1 = request.POST.get('cantidadEntradas1')
                arregloEntradas2 = request.POST.get('cantidadEntradas2')
                arregloEntradas3 = request.POST.get('cantidadEntradas3')
                print(arregloEntradas1)
                print(arregloEntradas2)
                print(arregloEntradas3)
                print(box1)
                print(box2)
                print(box3)
                cantTiposEntradas =  Tipos.objects.count()
                entradasCantidad = []
                for i in range(cantTiposEntradas):
                    entradasCantidad.append(request.POST.get('cantidadEntradas'+str(i+1)))
                print(entradasCantidad)
                error               = "ninguno"
                montoPagar          = 0
                entradasElegidas    = {}
                idxEntradasElegidas = 0 #Se usa para el key a mostrar
                for idxTiposEntradas in range(cantTiposEntradas):
                    descripcionTipo = Tipos.objects.get(tipo=(idxTiposEntradas+1)).descripcion
                    if entradasCantidad[idxTiposEntradas] == str(0):
                        continue
                    idxEntradasElegidas = idxEntradasElegidas+1
                    #print(idxEntradasElegidas)
                    key = f"entrada{idxEntradasElegidas}"
                    value = {
                        "id": descripcionTipo,
                        "cantidad": entradasCantidad[idxTiposEntradas],
                        "tipo": str(idxTiposEntradas+1)
                    }
                    entradasElegidas[key] = value
                    montoPagar = montoPagar + int(entradasCantidad[idxTiposEntradas])*int(Tipos.objects.get(tipo=(idxTiposEntradas+1)).precio)

                    ##############################
                    auxiliarDisminuyeEntradas          = Tipos.objects.get(tipo=(idxTiposEntradas+1))
                    auxiliarDisminuyeEntradas.cantidad = auxiliarDisminuyeEntradas.cantidad
                    if((auxiliarDisminuyeEntradas.cantidad-int(entradasCantidad[idxTiposEntradas]))<0):
                        error += "No quedan entradas del tipo: "+descripcionTipo
                        break
                    if idxTiposEntradas+1 == 4:
                        print(box1)
                        auxiliarDisminuyeBox1 = boxesRestante1.objects.get(box=int(box1))
                        if(auxiliarDisminuyeBox1.ocupado):
                            error = "El box: "+str(box1)+" ya fue comprado."    
                            break
                    if idxTiposEntradas+1 == 5:
                        print(box2)
                        auxiliarDisminuyeBox2 = boxesRestante2.objects.get(box=int(box2))
                        if(auxiliarDisminuyeBox2.ocupado):
                            error = "No queda el box: "+str(box2)+" ya fue comprado."
                            break
                    if idxTiposEntradas+1 == 6:
                        print(box3)
                        auxiliarDisminuyeBox3 = boxesRestante3.objects.get(box=int(box3))
                        if(auxiliarDisminuyeBox3.ocupado):
                            error = "No queda el box: "+str(box3)+" ya fue comprado."
                            break    

                if(error != "ninguno"):
                    responseData = {
                        'error': error,
                    }
                    request.session['compra_redirect'] = "compra"
                    request.session['contexto'] = {
                        'response': responseData
                    }
                    return redirect(request.path)


            #########################################################
                # PAGO
                nuevaCompra               = Pagos()
                nuevaCompra.estado        = 1             #Generado en pagina de compra
                nuevaCompra.fechaHoraPREP = timezone.now()
                #Nulo fechaHoraCONF
                #Nulo fechaHoraPAGO
                #Nulo fechaHoraSmsTicketsPagados

                nuevaCompra.celular   = celular

                nuevaCompra.cip       = cip
                nuevaCompra.pin       = pin
                nuevaCompra.monto     = montoPagar
                # confirmado
                # sms tickets pagados
                nuevaCompra.nombre    = nombre
                nuevaCompra.correo    = correo
                nuevaCompra.dni       = dni
                nuevaCompra.pregunta1 = pregunta1
                nuevaCompra.pregunta2 = pregunta2
                nuevaCompra.pregunta3 = pregunta3
                respuesta1            = respuesta1
                respuesta2            = respuesta2
                respuesta3            = respuesta3
                nuevaCompra.save() 
            #########################################################
                #TICKETS
                error = "ninguno"
                for numTipo in range(cantTiposEntradas):
                    #print(request.POST.get('tipoentrada'+str(i+1)))
                    if (int(entradasCantidad[numTipo]) == 0):
                        continue
                    
                    auxiliarDisminuyeEntradas          = Tipos.objects.get(tipo=(numTipo+1))
                    auxiliarDisminuyeEntradas.cantidad = auxiliarDisminuyeEntradas.cantidad
                    descripcionTipoEntrada             = Tipos.objects.get(tipo=(numTipo+1)).descripcion
                    if((auxiliarDisminuyeEntradas.cantidad-int(entradasCantidad[numTipo]))<0):
                        error = "No quedan entradas del tipo: "+Tipos.objects.get(tipo=(numTipo+1)).descripcion
                        break
                    auxiliarDisminuyeEntradas.cantidad = auxiliarDisminuyeEntradas.cantidad-int(entradasCantidad[numTipo])
                    auxiliarDisminuyeEntradas.save()
                    if numTipo+1 == 4:
                            ticket.numeroBox = box1
                            auxiliarDisminuyeBox1 = boxesRestante1.objects.get(box=int(box1))
                            if(auxiliarDisminuyeBox1.ocupado):
                                error = "El box: "+box1+" ya fue comprado."
                                break    
                            auxiliarDisminuyeBox1.ocupado = True
                            auxiliarDisminuyeBox1.save()
                            for _ in range(10):
                                ticket = Tickets()
                                ticket.ticket          = generaNumeroTicket()
                                ticket.codigoseguridad = generacodigoseguridad()
                                ticket.pin             = pin
                                ticket.fechaHoraCambio = timezone.now()
                                ticket.celular         = celular
                                ticket.tipo            = descripcionTipoEntrada
                                ticket.numeroBox       = box1
                                ticket.cip             = cip
                                ticket.nombre          = nombre
                                ticket.correo          = correo
                                ticket.dni             = dni
                                ticket.pregunta1       = pregunta1
                                ticket.pregunta2       = pregunta2
                                ticket.pregunta3       = pregunta3
                                ticket.respuesta1      = respuesta1
                                ticket.respuesta2      = respuesta2
                                ticket.respuesta3      = respuesta3
                                ticket.save()
                                

                    if numTipo+1 == 5:
                        ticket.numeroBox = box2
                        auxiliarDisminuyeBox2 = boxesRestante2.objects.get(box=int(box2))
                        if(auxiliarDisminuyeBox2.ocupado):
                                error = "No queda el box: "+box2+" ya fue comprado."
                                break    
                        auxiliarDisminuyeBox2.ocupado = True
                        auxiliarDisminuyeBox2.save()
                        for _ in range(10):
                                ticket = Tickets()
                                ticket.ticket          = generaNumeroTicket()
                                ticket.codigoseguridad = generacodigoseguridad()
                                ticket.pin             = pin
                                ticket.fechaHoraCambio = timezone.now()
                                ticket.celular         = celular
                                ticket.tipo            = descripcionTipoEntrada
                                ticket.numeroBox       = box2
                                ticket.cip             = cip
                                ticket.nombre          = nombre
                                ticket.correo          = correo
                                ticket.dni             = dni
                                ticket.pregunta1       = pregunta1
                                ticket.pregunta2       = pregunta2
                                ticket.pregunta3       = pregunta3
                                ticket.respuesta1      = respuesta1
                                ticket.respuesta2      = respuesta2
                                ticket.respuesta3      = respuesta3
                                ticket.save()
                                
                    if numTipo+1 == 6:
                        ticket.numeroBox = box3
                        auxiliarDisminuyeBox3 = boxesRestante3.objects.get(box=int(box3))
                        if(auxiliarDisminuyeBox3.ocupado):
                                error = "No queda el box: "+box3+" ya fue comprado."
                                break    
                        auxiliarDisminuyeBox3.ocupado = True
                        auxiliarDisminuyeBox3.save()
                        for _ in range(10):
                                ticket = Tickets()
                                ticket.ticket          = generaNumeroTicket()
                                ticket.codigoseguridad = generacodigoseguridad()
                                ticket.pin             = pin
                                ticket.fechaHoraCambio = timezone.now()
                                ticket.celular         = celular
                                ticket.tipo            = descripcionTipoEntrada
                                ticket.numeroBox       = box3
                                ticket.cip             = cip
                                ticket.nombre          = nombre
                                ticket.correo          = correo
                                ticket.dni             = dni
                                ticket.pregunta1       = pregunta1
                                ticket.pregunta2       = pregunta2
                                ticket.pregunta3       = pregunta3
                                ticket.respuesta1      = respuesta1
                                ticket.respuesta2      = respuesta2
                                ticket.respuesta3      = respuesta3
                                ticket.save()
                                                        
               
                    for _ in range(int(entradasCantidad[numTipo])): 
                        if numTipo+1 == 4:
                            ticket.numeroBox = box1
                            continue
                        if numTipo+1 == 5:
                            ticket.numeroBox = box2
                            continue
                        if numTipo+1 == 6:
                            ticket.numeroBox = box3
                            continue
                        ticket = Tickets()
                        ticket.ticket          = generaNumeroTicket()
                        ticket.codigoseguridad = generacodigoseguridad()
                        ticket.pin             = pin
                        ticket.fechaHoraCambio = timezone.now()
                        ticket.celular         = celular
                        ticket.tipo            = descripcionTipoEntrada
                        ticket.numeroBox       = "0"

                        ticket.cip         = cip
                        ticket.nombre      = nombre
                        ticket.correo      = correo
                        ticket.dni         = dni
                        ticket.pregunta1   = pregunta1
                        ticket.pregunta2   = pregunta2
                        ticket.pregunta3   = pregunta3
                        ticket.respuesta1  = respuesta1
                        ticket.respuesta2  = respuesta2
                        ticket.respuesta3  = respuesta3
                        ticket.save()
                    
                if(error!="ninguno"):
                    responseData = {
                        'error': error,
                    }
                    request.session['compra_redirect'] = "compra"
                    request.session['contexto'] = {
                        'response': responseData
                    }
                    return redirect(request.path)
                
                responseData = {
                                'cip': cip,
                                }
                print(responseData)

                request.session['compra_redirect'] = "compra"
                request.session['contexto'] = {
                    'response': responseData, 'entradas': entradasElegidas, 'precioTotal': str(montoPagar)}
                return redirect(request.path)

##########################################################
            elif request.POST.get('boton') == 'confirmarCompra':
                print("POST confirmarCompra")
                cipRecibo = request.POST.get('cip')
                #disminuyeEntradas(cipRecibo)
                entradasArgumento = armaEntradas(cipRecibo) #Esperado tipo (Arreglo)[] con diccionarios como elementos {} de campos ["tipo_ticket"] y ["numero_ticket"] 
                datosConfirmar = {
                    'entradas': entradasArgumento,
                }

                request.session['tickets_redirect'] = "tickets"
                request.session['contexto']         = datosConfirmar
                print("Llega hasta redirect confirmar Ticket")
                return redirect(request.path)

        return render(request, "comprarPage/comprarPage.html", datos)


def administrarPage(request):
    if request.POST.get('submit') == "validar":
        return render(request, "validarPage/validarPage.html")
    elif request.POST.get('submit') == "transferir":
        return render(request, "transferirPage/transferirPage.html")
    elif request.POST.get('submit') == "vender":
        None
    elif request.POST.get('submit') == "comprar":
        None

    # ValidarPage
    if request.method == 'POST' and request.POST.get('comando') == 'verificarBotonValidarTemplate':
        numero = request.POST.get('ticket')
        apellido = request.POST.get('cip')
        
        try:
            ticket = Tickets.objects.get(ticket=numero, nombre__icontains=apellido)
            if ticket.confirmado2 is not None:
                responseData = {'estado': 'Ticket valido'}
            else:
                responseData = {'estado': 'Ticket en validacion'}
        except Tickets.DoesNotExist or Tickets.MultipleObjectsReturned:
            responseData = {'estado': 'Ticket no valido'}
        return JsonResponse(responseData)
    return render(request, "administrarPage.html")

def escanerPage(request):
    return render(request, "escanerPage/escanerPage.html")

def apiPage(request):
    return render(request, "apiDNI/index.html")
