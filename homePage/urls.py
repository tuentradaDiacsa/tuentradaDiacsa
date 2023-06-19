from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views
from .views import comprarPage
#from django.conf.urls import url

urlpatterns = [
    path("", views.homePage, name="homePage"),
    path("comprar/", comprarPage.as_view(), name="comprarPage"),
    path("administrar/", views.administrarPage, name="administrarPage"),
    path('descargar_boleto/<entrada_id>/', views.descargar_boleto, name='descargar_boleto'),
    #path('descargar_boleto/<int:entrada_id>/', views.descargar_boleto, name='descargar_boleto'),
    #path('descargar_boleto/(?P<entrada_id>\d+)/$', views.descargar_boleto, name='descargar_boleto'),
    path("escaner/", views.escanerPage, name="escanerPage"),
     path("api/", views.apiPage, name="apiPage"),
]

urlpatterns += staticfiles_urlpatterns()
