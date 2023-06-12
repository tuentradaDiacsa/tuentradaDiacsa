from django.db import models


class Pagos(models.Model):
    # key = models.ForeignKey()
    fechaHora = models.DateTimeField()  # Actual
    celular   = models.TextField()
    whatsapp  = models.TextField(blank=True, null=True)
    cip = models.TextField()  # Aleatorio 6 digitos
    pin = models.TextField(blank=True, null=True)
    monto = models.TextField()
    confirmado2 = models.DateTimeField(
        blank=True, null=True)  # Por defecto blanco
    smsTicketsPagados = models.DateTimeField(
        blank=True, null=True)  # Por defecto false
    nombre = models.TextField(max_length=40, blank=True, null=True)
    correo = models.TextField(max_length=20, blank=True, null=True)
    dni = models.TextField(blank=True, null=True)
    pregunta1 = models.TextField(max_length=50, blank=True, null=True)
    pregunta2 = models.TextField(max_length=50, blank=True, null=True)
    pregunta3 = models.TextField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return str(self.cip)+" "+str(self.celular)+" "+str(self.monto)


class Tickets(models.Model):
    ticket = models.TextField()  # XYZ(CIUDAD)XYZ(EVENTO)-ABCDE
    codigoseguridad = models.TextField()  # Aleatorio 8 alfanumericos

    # pin cambia codigo de seguridad
    pin = models.TextField(blank=True, null=True)
    # intento de cambio de pin #cuando se cambia o accede se reinicia #si llega a 10 se bloquea
    pinIntentos = models.PositiveIntegerField(default=0)
    fechaHoraIntentoFallido = models.DateTimeField(
        blank=True, null=True)  # Fecha del ultimo intento fallido
    # Fecha generacion igual a la del pin cambio igual a generacion pero con reinicio si se transfiere
    fechaHoraCambio = models.DateTimeField(blank=True, null=True)
    celular         = models.TextField()
    whatsapp        = models.TextField(blank=True, null=True)

    tipo        = models.TextField()
    numeroBox   = models.TextField(max_length=5, default='0')
    cip         = models.TextField()  # antes recibo
    confirmado2 = models.DateTimeField(
        blank=True, null=True)  # Por defecto blanco

    nombre    = models.TextField(max_length=40, blank=True, null=True)
    correo    = models.TextField(max_length=50, blank=True, null=True)
    dni       = models.TextField(blank=True, null=True)
    pregunta1 = models.TextField(max_length=50, blank=True, null=True)
    pregunta2 = models.TextField(max_length=50, blank=True, null=True)

    intentosIngresoFallido = models.PositiveIntegerField(
        blank=True, null=True, default=0)
    fechaHoraIngresoExitoso = models.DateTimeField(blank=True, null=True)
    intentosIngresoOK = models.PositiveIntegerField(
        blank=True, null=True, default=0)

    def __str__(self):
        return str(self.cip)+" "+str(self.tipo)+" "+str(self.ticket)
    
class Tipos(models.Model):
    tipo = models.PositiveIntegerField()
    descripcion = models.TextField()
    cantidad = models.PositiveBigIntegerField(default=100)
    precio = models.PositiveIntegerField()

    def __str__(self):
        return self.descripcion+" "+str(self.cantidad)

class Preguntas(models.Model):
    tipo = models.PositiveIntegerField()
    pregunta = models.CharField(max_length=100)

    def __str__(self):
        return self.pregunta


class smsValidacionCelular(models.Model):
    correlativo = models.AutoField(primary_key=True)
    celular = models.CharField(max_length=9)
    codigoValidacion = models.CharField(max_length=6)
    # Lo llena el script en la computadora
    fechaHoraEnvio = models.DateTimeField(blank=True, null=True)
    # Lo llena el script de la computadora
    estado = models.PositiveIntegerField(default=0)

    class Meta:
        # Reemplaza 'nombre_de_la_tabla' por el nombre que desees para tu tabla
        db_table = 'SMSCelularesyCodigosValidacion'

    def __str__(self):
        return str(self.correlativo)+" "+str(self.celular)+" "+str(self.codigoValidacion)+" "+str(self.estado)

class boxesRestante1(models.Model):
    box     = models.CharField(max_length=5)
    ocupado = models.BooleanField(default=False)

    def __str__(self):
        return "box"+str(self.box)+" "+str("Ocupado" if self.ocupado else "Libre")

class boxesRestante2(models.Model):
    box     = models.CharField(max_length=5)
    ocupado = models.BooleanField(default=False)

    def __str__(self):
        return "box"+str(self.box)+" "+str("Ocupado" if self.ocupado else "Libre")

class boxesRestante3(models.Model):
    box     = models.CharField(max_length=5)
    ocupado = models.BooleanField(default=False)

    def __str__(self):
        return "box"+str(self.box)+" "+str("Ocupado" if self.ocupado else "Libre")
