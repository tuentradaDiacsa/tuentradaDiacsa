from django.contrib import admin
from .models import smsValidacionCelular, Tipos, Pagos, Tickets, boxesRestante1, boxesRestante2, boxesRestante3
# Register your models here.
admin.site.register(smsValidacionCelular)
admin.site.register(Tipos)
admin.site.register(Pagos)
admin.site.register(Tickets)
admin.site.register(boxesRestante1)
admin.site.register(boxesRestante2)
admin.site.register(boxesRestante3)
