from django.urls import path
from . import views

# TEMPLATE TAGGING
app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('compradores_vendedores', views.compradores_vendedores, name='compradores_vendedores'),
]