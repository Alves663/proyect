from django.urls import path
from . import views

# TEMPLATE TAGGING
app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('ajax_top_products', views.ajax_top_products, name="ajax_top_products"),
    path('top_products', views.top_products, name='top_products'),
    path('compradores_vendedores', views.compradores_vendedores, name='compradores_vendedores'),
]