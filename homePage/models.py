from django.db import models


class Pagos(models.Model):
    # key = models.ForeignKey()

    estado = models.IntegerField(blank=True, null=True, default="0")
    fechaHoraPREP = models.DateTimeField(
        blank=True, null=True
    )  # Boton de Comprar en pagina de seleccion tickets #Comprador en Web+Server
    fechaHoraCONF = models.DateTimeField(
        blank=True, null=True
    )  # Boton de Confirmar en pagina resumen #Comprador en Web+Server
    fechaHoraPAGO = models.DateTimeField(
        blank=True, null=True
    )  # Verificacion de Pago con resumen de transferencias o compras #Script PC
    fechaHoraSmsTicketsPagados = models.DateTimeField(
        blank=True, null=True
    )  # Envio de URL con tickets de QR oficial #Script PC

    celular = models.TextField()

    cip = models.TextField()  # Aleatorio 6 digitos
    pin = models.TextField(blank=True, null=True)
    monto = models.TextField()

    whatsapp = models.TextField(blank=True, null=True)
    nombre = models.TextField(max_length=40, blank=True, null=True)
    correo = models.TextField(max_length=20, blank=True, null=True)
    dni = models.TextField(blank=True, null=True)
    pregunta1 = models.TextField(max_length=50, blank=True, null=True)
    pregunta2 = models.TextField(max_length=50, blank=True, null=True)
    pregunta3 = models.TextField(max_length=50, blank=True, null=True)
    respuesta1 = models.TextField(max_length=50, blank=True, null=True)
    respuesta2 = models.TextField(max_length=50, blank=True, null=True)
    respuesta3 = models.TextField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.cip) + " " + str(self.celular) + " " + str(self.monto)


class Tickets(models.Model):
    estado = models.IntegerField(blank=True, null=True)
    ticket = models.TextField()  # XYZ(CIUDAD)XYZ(EVENTO)-ABCDE
    codigoseguridad = models.TextField()  # Aleatorio 8 alfanumericos

    fechaHoraCambio = models.DateTimeField(
        blank=True, null=True
    )  # Fecha generacion cada vez cambia pin
    # cambio igual a generacion pero con reinicio si se transfiere
    fechaHoraConfirmado = models.DateTimeField(
        blank=True, null=True
    )  # Hora en que se da click a boton Confirmar
    fechaHoraPago = models.DateTimeField(
        blank=True, null=True
    )  # Hora en que se corrobora el pago con resumenes de banco

    pin = models.TextField(blank=True, null=True)  # pin cambia codigo de seguridad
    pinIntentos = models.PositiveIntegerField(
        default=0
    )  # intento de cambio de pin #cuando se cambia o accede se reinicia
    # si llega a 10 se bloquea
    fechaHoraIntentoFallido = models.DateTimeField(
        blank=True, null=True
    )  # Fecha del ultimo intento fallido

    celular = models.TextField()

    codigoTransferencia = models.TextField(blank=True, null=True)
    tipo = models.TextField()
    numeroBox = models.TextField(max_length=5, default="0")
    cip = models.TextField()  # Usado para pagos

    whatsapp = models.TextField(blank=True, null=True)
    nombre = models.TextField(max_length=40, blank=True, null=True)
    correo = models.TextField(max_length=50, blank=True, null=True)
    dni = models.TextField(blank=True, null=True)
    pregunta1 = models.TextField(max_length=50, blank=True, null=True)
    pregunta2 = models.TextField(max_length=50, blank=True, null=True)
    pregunta3 = models.TextField(max_length=50, blank=True, null=True)
    respuesta1 = models.TextField(max_length=50, blank=True, null=True)
    respuesta2 = models.TextField(max_length=50, blank=True, null=True)
    respuesta3 = models.TextField(max_length=50, blank=True, null=True)

    intentosIngresoFallido = models.PositiveIntegerField(
        blank=True, null=True, default=0
    )
    fechaHoraIngresoExitoso = models.DateTimeField(blank=True, null=True)
    intentosIngresoOK = models.PositiveIntegerField(blank=True, null=True, default=0)

    codigoDescarga = models.TextField(
        blank=True, null=True, default=""
    )  # codigo Descarga

    def __str__(self):
        return str(self.cip) + " " + str(self.tipo) + " " + str(self.ticket)


class Tipos(models.Model):
    tipo = models.PositiveIntegerField()
    descripcion = models.TextField()
    cantidad = models.PositiveBigIntegerField(default=100)
    precio = models.PositiveIntegerField()

    def __str__(self):
        return self.descripcion + " " + str(self.cantidad)


class Preguntas(models.Model):
    tipo = models.PositiveIntegerField()
    pregunta = models.CharField(max_length=100)

    def __str__(self):
        return self.pregunta


class smsValidacionCelular(models.Model):
    correlativo = models.AutoField(primary_key=True)
    celular = models.CharField(max_length=9)
    codigoValidacion = models.CharField(max_length=8, default="12345678")
    # Lo llena el script en la computadora
    fechaSolicitud = models.DateTimeField(blank=True, null=True)
    fechaEnvio = models.DateTimeField(blank=True, null=True)
    # Lo llena el script de la computadora
    estado = models.PositiveIntegerField(default=0)

    class Meta:
        # Reemplaza 'nombre_de_la_tabla' por el nombre que desees para tu tabla
        db_table = "SMSCelularesyCodigosValidacion"

    def __str__(self):
        return (
            str(self.correlativo)
            + " "
            + str(self.celular)
            + " "
            + str(self.codigoValidacion)
            + " "
            + str(self.estado)
        )


class boxesRestante1(models.Model):
    box = models.IntegerField()
    ocupado = models.BooleanField(default=False)

    def __str__(self):
        return "box" + str(self.box) + " " + str("Ocupado" if self.ocupado else "Libre")


class boxesRestante2(models.Model):
    box = models.IntegerField()
    ocupado = models.BooleanField(default=False)

    def __str__(self):
        return "box" + str(self.box) + " " + str("Ocupado" if self.ocupado else "Libre")


class boxesRestante3(models.Model):
    box = models.IntegerField()
    ocupado = models.BooleanField(default=False)

    def __str__(self):
        return "box" + str(self.box) + " " + str("Ocupado" if self.ocupado else "Libre")
