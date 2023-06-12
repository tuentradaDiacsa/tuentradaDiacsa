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

def get_dynamic_base_url(request):
    current_site = get_current_site(request)
    scheme = 'https' if request.is_secure() else 'http'

    # Combinar con la ruta base de los archivos estáticos
    static_url = '/static/'  # Esto debería coincidir con tu configuración STATIC_URL

    return f'{scheme}://{current_site.domain}{static_url}'


def generar_qr_code_url(datoencriptado):
    data = datoencriptado#"Ticket: {}, CIP: {}".format(ticket, cip)
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    qr_image = qr.make_image(fill="black", back_color="white")
    qr_buffer = io.BytesIO()
    qr_image.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)
    return qr_buffer


def descargar_boleto(request, entrada_id):
    try:
        ticket_obj = Tickets.objects.get(ticket=entrada_id)
        codigoseguridad  = ticket_obj.codigoseguridad
        codigoseguridad_encriptador = encriptador(entrada_id, codigoseguridad)
        qr_buffer = generar_qr_code_url(codigoseguridad_encriptador)
        qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode('utf-8')
        qr_url = "data:image/png;base64," + qr_base64
        context = {
            'ID_Ticket': entrada_id,
            'nombre_y_apellido': getattr(ticket_obj, 'nombre', 'No completado'),
            'dni': getattr(ticket_obj, 'dni', 'No completado'),
            'telefono': getattr(ticket_obj, 'celular', 'No completado'),
            'whatsapp': getattr(ticket_obj, 'celular', 'No completado'),
            'Lugar': "Hangar de Iquitos",
            'Ubicacion': "Calle Muy Bonita 234 Iquitos Peru",
            'fecha': "21-06-2023",
            'hora': "3:00 pm",
            'Zona': getattr(ticket_obj, 'tipo', 'No completado'),
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


def generar_pdf_desde_html(html_content):
    pdf_data = pdfkit.from_string(html_content, False)
    return pdf_data


def obtener_entrada(entrada_id):
    datosentrada = {}
    datosentrada[id] = entrada_id
    return datosentrada


def descargar_boleto2(request, entrada_id):
    datosEntrada = {
        'ID_Ticket': 2,
        'nombre_y_apellido': "Andre Bolaños",
        'dni': 44036805,
        'telefono': 975976333,
        'whatsapp': 975976333,
        'Lugar': "Hangar de Iquitos",
        'Ubicacion': "Calle Muy Bonita 234 Iquitos Peru",
        'fecha': "21-06-2023",
        'hora': "7:00 pm",
        'Zona': "Box 1",

    }
    return render(request, "entradas/plantillaentrada1.html", datosEntrada)


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


TipoEntradas = ["Platinum", "Box", "Motor y Motivo",
                "General", "Alimaña", "Palco"]


def armaEntradas(entradasArreglo):
    '''
    ticket1 = {}
    ticket1["tipo_ticket"]="Platinum"
    ticket1["numero_ticket"]=1
    ticket1["cip"]="ABC123"

    ticket2 = {}
    ticket2["tipo_ticket"]="VIP"
    ticket2["numero_ticket"]=2
    ticket2["cip"]="456XYZ"
    '''
    arregloAenviar = []
    auxiliar = {}
    print(entradasArreglo)
    for indice, entrada in enumerate(entradasArreglo):

        print(entrada)
        print(entrada[0])
        print("Paso cantidad")
        for i in range(int(entrada)):
            auxiliar = {}
            auxiliar["tipo_ticket"] = TipoEntradas[indice]
            auxiliar["numero_ticket"] = generaNumeroTicket(indice)
            auxiliar["cip"] = generaCIP()
            arregloAenviar.append()

    return arregloAenviar  # [ticket1,ticket2]


def homePage(request):
    return render(request, "homePage/homePage.html")


def calculamonto(request):
    print("entradaID: ", request.POST.get("entradaID"+str(i+1)),
          "cantidad: ", request.POST.get("entradasFilaID"+str(i+1)))

# def descargar_boleto(request, entrada_id):
    # Lógica para obtener el archivo PDF del boleto basado en entrada_id
    # boleto = obtener_boleto_pdf(entrada_id)
    # obtener_boleto_pdf(entrada_id)
    # Devuelve el archivo PDF como una respuesta de archivo
    # return #FileResponse(boleto, as_attachment=True, filename='boleto.pdf')


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
                nuevaCompra.celular = request.POST.get('celular')
                nuevaCompra.cip = request.POST.get('cip')
                nuevaCompra.pin = request.POST.get('pin')
                nuevaCompra.monto = request.POST.get('montoaPagar')
                # confirmado
                # sms tickets pagados
                nuevaCompra.nombre = request.POST.get('nombre')
                nuevaCompra.correo = request.POST.get('correo')
                nuevaCompra.dni = request.POST.get('dni')
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
                    if (request.POST.get('tipoentrada'+str(i+1)) == None):
                        continue
                    ticketsCantidad = ticketsCantidad + 1
                    ultimoTicket = ultimoTicket + 1                  
                    for j in range(int(request.POST.get("cantidadentrada"+str(i+1)))):
                        auxiliarDisminuyeEntradas = Tipos.objects.get(tipo=int(request.POST.get('tipoentrada'+str(i+1))))
                        auxiliarDisminuyeEntradas.cantidad = auxiliarDisminuyeEntradas.cantidad-1
                        auxiliarDisminuyeEntradas.save()
                        
                        Tipos.objects.get(tipo=k+1).descripcion
                        #print(j)
                        # montoPagar = montoPagar + int(entradasCantidad[i])*int(Tipos.objects.get(tipo = auxiliarDisminuyeEntradas).precio)
                        ticket = Tickets()
                        ticket.ticket = generaNumeroTicket()
                        ticket.codigoseguridad = generacodigoseguridad()
                        ticket.pin = request.POST.get('pin')
                        ticket.fechaHoraCambio = timezone.now()
                        ticket.celular = request.POST.get('celular')
                        ticket.tipo = Tipos.objects.get(tipo=auxiliarDisminuyeEntradas).descripcion
                        ticket.numeroBox = "0"
                        if int(request.POST.get('tipoentrada'+str(auxiliarDisminuyeEntradas))) == 4:
                            ticket.numeroBox = box1
                        if int(request.POST.get('tipoentrada'+str(auxiliarDisminuyeEntradas))) == 5:
                            ticket.numeroBox = box2
                        if int(request.POST.get('tipoentrada'+str(auxiliarDisminuyeEntradas))) == 6:
                            ticket.numeroBox = box3
                        ticket.cip = request.POST.get('cip')
                        ticket.nombre = request.POST.get('nombre')
                        ticket.correo = request.POST.get('correo')
                        ticket.dni = request.POST.get('dni')
                        ticket.pregunta1 = request.POST.get('pregunta1')
                        ticket.pregunta2 = request.POST.get('pregunta2')
                        # "id": Tipos.objects.get(tipo = auxiliarDisminuyeEntradas).descripcion,
                        ticket.save()
                        auxiliar = {}
                        auxiliar["tipo_ticket"] = Tipos.objects.get(
                            id=int(request.POST.get('tipoentrada'+str(auxiliarDisminuyeEntradas)))).descripcion
                        auxiliar["numero_ticket"] = ticket.ticket
                        entradasArgumento.append(auxiliar)

                # return render(request, "ticketsCompradosPage/ticketsCompradosPage.html", {'response': responseData, 'entradas': entradasElegidas, 'precioTotal': str(montoPagar)})
                # entradasArgumento = armaEntradas(entradasArreglo)
                datosConfirmar = {
                    'entradas': entradasArgumento,
                }

                # entradas = {}
                # for i in range (4):
                #    key = f"entrada{str(i)}"
                #    value = {
                #        "id": Tipos.objects.get(id = i + 1).descripcion, #nombre de la entrada
                # mas cosas
                # mas
                #
                #
                #    }
                #    entradas[key] = value
                # return render(request, "ticketsCompradosPage/ticketsCompradosPage.html", {"entradas" : entradas})
                request.session['tickets_redirect'] = "tickets"
                request.session['contexto'] = datosConfirmar
                print("Llega hasta redirect")
                return redirect(request.path)
                return render(request, "ticketsCompradosPage/ticketsCompradosPage.html", datosConfirmar)
                # entradas = Tipos.objects.all()
                # monto = 0

                # #cantidadEntradasTipo1 = request.POST.get("cantidadEntradasTipo1")
                # #cantidadEntradasTipo2 = request.POST.get("cantidadEntradasTipo2")
                # #cantidadEntradasTipo3 = request.POST.get("cantidadEntradasTipo3")
                # #cantidadEntradasTipo4 = request.POST.get("cantidadEntradasTipo4")
                # entradasArreglo = {}
                # for i in range (4):
                #     campo = "cantidadEntradasTipo"+str(i)
                #     cantidad = int(request.POST.get("cantidadEntradasTipo"+str(i+1)))
                #     entradasArreglo[campo] = cantidad
                #     monto += (entradas[i].precio)*cantidad

                # celular = request.POST.get('celular')
                # print(celular)
                # codigo = request.POST.get('codigo')
                # print(codigo)
                # pin = request.POST.get('pin')
                # print(pin)
                # medioPago = request.POST.get('medioPago')
                # print(medioPago)
                # nombre = request.POST.get('nombre')
                # print(nombre)
                # correo = request.POST.get('correo')
                # print(correo)
                # dni = request.POST.get('dni')
                # print(dni)
                # pregunta1 = request.POST.get('pregunta1')
                # print(pregunta1)
                # pregunta2 = request.POST.get('pregunta2')
                # print(pregunta2)
                # monto = request.POST.get('monto')
                # print(monto)
                # print("Pasa por POST Confirmar")

                # pagoAguardar = Pagos()
                # #pagoAguardar.fechaHora =         #Actual
                # pagoAguardar.celular = celular
                # #pagoAguardar.recibo =
                # pagoAguardar.pin = pin
                # pagoAguardar.monto = monto
                # #pagoAguardar.confirmado =
                # #pagoAguardar.sms =
                # pagoAguardar.nombre = nombre
                # pagoAguardar.correo = correo
                # pagoAguardar.dni = dni
                # pagoAguardar.pregunta1 = pregunta1
                # pagoAguardar.pregunta2 = pregunta2

                # entradasArgumento = armaEntradas(entradasArreglo)
                # print(entradasArgumento)
                # datosConfirmar = {
                #     'entradas': entradasArgumento,
                # }
                # return render(request, "ticketsCompradosPage/ticketsCompradosPage.html",datosConfirmar)
        return render(request, "comprarPage/comprarPage.html", datos)


def administrarPage(request):
    if request.POST.get('submit') == "validar":
        return render(request, "validarPage/validarPage.html")
    elif request.POST.get('submit') == "actualizar":
        None
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
