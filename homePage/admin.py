from django.contrib import admin
from .models import smsValidacionCelular, Tipos, Pagos, Tickets
# Register your models here.
admin.site.register(smsValidacionCelular)
admin.site.register(Tipos)
admin.site.register(Pagos)
admin.site.register(Tickets)
