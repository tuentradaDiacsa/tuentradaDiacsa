from django.db import models
class Pagos(models.Model):
    #key = models.ForeignKey()
    fechaHora = models.DateTimeField()        #Actual
    celular = models.TextField()
    cip = models.TextField() #Aleatorio 6 digitos
    pin = models.TextField(blank=True, null=True)       
    monto = models.TextField()
    confirmado = models.DateTimeField(blank=True, null=True)         #Por defecto blanco
    smsTicketsPagados = models.DateTimeField(blank=True, null=True)               #Por defecto false
    nombre = models.TextField(max_length=40, blank=True, null=True)
    correo = models.TextField(max_length=20, blank=True, null=True)
    dni = models.TextField(blank=True, null=True)
    pregunta1 = models.TextField(max_length= 50, blank=True, null=True)
    pregunta2 = models.TextField(max_length= 50, blank=True, null=True)
    
class Tickets(models.Model):
    ticket          = models.TextField() #XYZ(CIUDAD)XYZ(EVENTO)-ABCDE
    codigoseguridad = models.TextField() #Aleatorio 8 alfanumericos

    pin                     = models.TextField(blank=True, null=True)     #pin cambia codigo de seguridad
    pinIntentos             = models.PositiveIntegerField( default=0)     #intento de cambio de pin #cuando se cambia o accede se reinicia #si llega a 10 se bloquea
    fechaHoraIntentoFallido = models.DateTimeField(blank=True, null=True) #Fecha del ultimo intento fallido
    fechaHoraCambio         = models.DateTimeField(blank=True, null=True) #Fecha generacion igual a la del pin cambio igual a generacion pero con reinicio si se transfiere
    celular                 = models.TextField()
    whatsapp                = models.TextField(blank=True, null=True) 

    tipo       = models.TextField()
    cip        = models.TextField()  #antes recibo
    confirmado = models.DateTimeField(blank=True, null=True)
    
    nombre    = models.TextField(max_length=40, blank=True, null=True)
    correo    = models.TextField(max_length=50, blank=True, null=True)
    dni       = models.TextField(blank=True, null=True)
    pregunta1 = models.TextField(max_length= 50, blank=True, null=True)
    pregunta2 = models.TextField(max_length= 50, blank=True, null=True)
    
    intentosIngresoFallido  = models.PositiveIntegerField(blank=True, null=True, default=0)
    fechaHoraIngresoExitoso = models.DateTimeField(blank=True, null=True)
    intentosIngresoOK       = models.PositiveIntegerField(blank=True, null=True, default=0)

    
class Tipos(models.Model):
    tipo        = models.PositiveIntegerField()
    descripcion = models.TextField()
    cantidad    = models.PositiveBigIntegerField(default=100)
    precio      = models.PositiveIntegerField()

class Preguntas(models.Model):
    tipo     = models.PositiveIntegerField()
    pregunta = models.CharField(max_length=100)
    def __str__(self):
        return self.pregunta
    
class smsValidacionCelular(models.Model):
    correlativo      = models.AutoField(primary_key=True)
    celular          = models.CharField(max_length=9)
    codigoValidacion = models.CharField(max_length=6)
    fechaHoraEnvio   = models.DateTimeField(blank=True, null=True) #Lo llena el script en la computadora
    estado           = models.PositiveIntegerField(default=0)              #Lo llena el script de la computadora

    class Meta:
        db_table = 'SMSCelularesyCodigosValidacion'  # Reemplaza 'nombre_de_la_tabla' por el nombre que desees para tu tabla