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
    resultado = re.sub(r'\b(\w)(\w+)(\w)\b', lambda match: match.group(1) + 'X' * len(match.group(2)) + match.group(3), cadena)
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
    
    #if len(cadena) >= 9:
    #    nueva_cadena = cadena[:-6] + "X" * 4 + cadena[-2:]
    #elif len(cadena) >= 8:
    #    nueva_cadena = cadena[:-6] + "X" * (len(cadena) - 4) + cadena[-1:]
    #else:
    #    nueva_cadena = cadena
    #return nueva_cadena

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
        #codigoseguridad  = ticket_obj.codigoseguridad
        #codigoseguridad_encriptador = encriptador(entrada_id, codigoseguridad)
        #qr_buffer = generar_qr_code_url(codigoseguridad_encriptador)
        #qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')
        #qr_url = "data:image/png;base64," + qr_base64
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

    # Generar el PDF en un buffer de memoria
    # pdf_data = generar_pdf_desde_html(html_content)

    # Crear una respuesta de Django con el archivo PDF
    # response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="archivo.pdf"'
    # response.write(pdf_data)

    return HttpResponse(html_content)  # response

'''
def descargar_boleto(request, entrada_id):
#def obtener_boleto_pdf(entrada_id):
    # Obtener la entrada correspondiente al entrada_id (tú debes implementar esta lógica)
    print("Ingreso obtener boleto pdf")
    entrada = obtener_entrada(entrada_id)
    #print(entrada)
    #print(entrada[id])
    # Crear un objeto BytesIO para almacenar el PDF
    buffer = io.BytesIO()

    # Crear el documento PDF con tamaño carta/letter y centrado
    p = canvas.Canvas(buffer, pagesize=letter)
    p.translate(p._pagesize[0] / 2, p._pagesize[1] / 2)  # Centrar el contenido en el lienzo

    # Calcular las coordenadas del código QR centrado en el lienzo
    qr_size = 200  # Tamaño del código QR
    qr_x = -qr_size / 2  # Coordenada X del punto de referencia del código QR
    qr_y = -qr_size / 2  # Coordenada Y del punto de referencia del código QR

    # Agregar el código QR al documento PDF
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(entrada[id])  # Puedes ajustar qué información se codificará en el QR
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    img.save("qr_code.png")  # Guardar el código QR como imagen (opcional)
    p.drawInlineImage("qr_code.png", qr_x, qr_y, qr_size, qr_size)  # Agregar el código QR al documento

    # Agregar otros elementos al documento PDF, como información de la entrada
    entry_info_x = -100  # Coordenada X del texto de información de la entrada
    entry_info_y = qr_y - 20  # Coordenada Y del texto de información de la entrada
    p.drawString(entry_info_x, entry_info_y, f"Número de Entrada: {entrada[id]}")
    # Agregar más elementos según tus necesidades

    # Finalizar el documento PDF
    p.showPage()
    p.save()

    # Reiniciar el cursor del buffer
    buffer.seek(0)

    # Crear una respuesta de Django con el archivo PDF
    nombre_archivo="boleto_"+str(entrada[id])+".pdf"
    return FileResponse(buffer, as_attachment=True, filename=nombre_archivo)#filename=f'boleto_{entrada[id]}.pdf')
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = f'attachment; filename=boleto_{entrada[id]}.pdf'
    #response.write(buffer.getvalue())

    # Cerrar el buffer
    buffer.close()

    return buffer#response
'''


def homePage(request):
    return render(request, "homePage/homePage.html")

class comprarPage(View):
    def get(self, request):
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
        identifica_compra = request.session.get('compra_redirect', False)
        if (identifica_compra):
            # print(request.session['compra_redirect'])
            del (request.session['compra_redirect'])
            contexto = request.session['contexto']
            del (request.session['contexto'])
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
            print("POST COMPRAR ENTRADA")
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
                # return redirect(request.path)
                return render(request, "comprarPage/comprarPage.html", datos)

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

            elif request.POST.get('boton') == 'comprar':
                celular    = request.POST.get('celular2')
                codigo     = request.POST.get('codigo2')
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
                box1       = request.POST.get('boxes1')
                box2       = request.POST.get('boxes2')
                box3       = request.POST.get('boxes3')
                # print("antes de cip")
                cip        = generaCIP(6)
                # print(cip)
                entradasCantidad = []
                for i in range(Tipos.objects.count()):
                    # print(request.POST.get('cantidadHidden'+str(i+1)))
                    entradasCantidad.append(
                        request.POST.get('cantidadHidden'+str(i+1)))
                # print(entradasCantidad)
                responseData = {'celular'   : celular,
                                'codigo'    : codigo,
                                'pin'       : pin,
                                'nombre'    : nombre,
                                'dni'       : dni,
                                'correo'    : correo,
                                'respuesta1': respuesta1,
                                'respuesta2': respuesta2,
                                'respuesta3': respuesta3,
                                'cip'       : cip,
                                'box1'      : box1,
                                'box2'      : box2,
                                'box3'      : box3,
                                }
                print(responseData)
                entradasElegidas = {}
                montoPagar = 0
                j = 0
                for i in range(Tipos.objects.count()):
                    if entradasCantidad[i] == str(0):
                        continue
                    j = j+1
                    key = f"entrada{j}"
                    montoPagar = montoPagar + \
                        int(entradasCantidad[i]) * \
                        int(Tipos.objects.get(tipo=i + 1).precio)
                    value = {
                        "id": Tipos.objects.get(tipo=i + 1).descripcion,
                        "cantidad": entradasCantidad[i],
                        "tipo": str(i+1)
                    }
                    entradasElegidas[key] = value
                # print(entradasElegidas)

                request.session['compra_redirect'] = "compra"
                request.session['contexto'] = {
                    'response': responseData, 'entradas': entradasElegidas, 'precioTotal': str(montoPagar)}
                return redirect(request.path)

            elif request.POST.get('boton') == 'confirmarCompra':
                #print("Boton confirmar compra presionado")
                # boxes comprados
                box1 = request.POST.get('box1')
                box2 = request.POST.get('box2')
                box3 = request.POST.get('box3')
                # PAGO
                nuevaCompra = Pagos()
                nuevaCompra.fechaHora = timezone.now()
                nuevaCompra.celular   = request.POST.get('celular')
                nuevaCompra.cip       = request.POST.get('cip')
                nuevaCompra.pin       = request.POST.get('pin')
                nuevaCompra.monto     = request.POST.get('montoaPagar')
                # confirmado
                # sms tickets pagados
                nuevaCompra.nombre    = request.POST.get('nombre')
                nuevaCompra.correo    = request.POST.get('correo')
                nuevaCompra.dni       = request.POST.get('dni')
                nuevaCompra.pregunta1 = request.POST.get('pregunta1')
                nuevaCompra.pregunta2 = request.POST.get('pregunta2')
                nuevaCompra.save()
                #print("Termino de almacenar pago")
                # TICKET
                ticketsCantidad = 0
                ultimoTicket = Tickets.objects.count()
                # monto = 0
                entradasArgumento = []
                for i in range(Tipos.objects.count()):
                    print(request.POST.get('tipoentrada'+str(i+1)))
                    if (request.POST.get('tipoentrada'+str(i+1)) == None):
                        continue
                    ticketsCantidad = ticketsCantidad + 1
                    ultimoTicket = ultimoTicket + 1                  
                    for j in range(int(request.POST.get("cantidadentrada"+str(i+1)))):
                        tipoactualInt=int(request.POST.get('tipoentrada'+str(i+1)))
                        auxiliarDisminuyeEntradas = Tipos.objects.get(tipo=tipoactualInt)
                        auxiliarDisminuyeEntradas.cantidad = auxiliarDisminuyeEntradas.cantidad-1
                        auxiliarDisminuyeEntradas.save()
                        
                        #Tipos.objects.get(tipo=k+1).descripcion
                        #print(j)
                        # montoPagar = montoPagar + int(entradasCantidad[i])*int(Tipos.objects.get(tipo = tipoactualInt).precio)
                        ticket = Tickets()
                        ticket.ticket          = generaNumeroTicket()
                        ticket.codigoseguridad = generacodigoseguridad()
                        ticket.pin             = request.POST.get('pin')
                        ticket.fechaHoraCambio = timezone.now()
                        ticket.celular         = request.POST.get('celular')
                        ticket.tipo            = Tipos.objects.get(tipo=tipoactualInt).descripcion
                        ticket.numeroBox       = "0"
                        if tipoactualInt == 4:
                            ticket.numeroBox = box1
                            auxiliarDisminuyeBox1 = boxesRestante1.objects.get(box=box1)
                            auxiliarDisminuyeBox1.ocupado = True
                            auxiliarDisminuyeBox1.save()
                        if tipoactualInt == 5:
                            ticket.numeroBox = box2
                            auxiliarDisminuyeBox2 = boxesRestante2.objects.get(box=box2)
                            auxiliarDisminuyeBox2.ocupado = True
                            auxiliarDisminuyeBox2.save()
                        if tipoactualInt == 6:
                            ticket.numeroBox = box3
                            auxiliarDisminuyeBox3 = boxesRestante3.objects.get(box=box3)
                            auxiliarDisminuyeBox3.ocupado = True
                            auxiliarDisminuyeBox3.save()
                        ticket.cip       = request.POST.get('cip')
                        ticket.nombre    = request.POST.get('nombre')
                        ticket.correo    = request.POST.get('correo')
                        ticket.dni       = request.POST.get('dni')
                        ticket.pregunta1 = request.POST.get('pregunta1')
                        ticket.pregunta2 = request.POST.get('pregunta2')
                        # "id": Tipos.objects.get(tipo = tipoactualInt).descripcion,
                        ticket.save()
                        auxiliar = {}
                        auxiliar["tipo_ticket"] = Tipos.objects.get(
                            tipo=tipoactualInt).descripcion
                        auxiliar["numero_ticket"] = ticket.ticket
                        entradasArgumento.append(auxiliar)

                datosConfirmar = {
                    'entradas': entradasArgumento,
                }

                request.session['tickets_redirect'] = "tickets"
                request.session['contexto'] = datosConfirmar
                print("Llega hasta redirect")
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
