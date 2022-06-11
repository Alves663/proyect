from django.urls import path
from . import views

# TEMPLATE TAGGING
app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('bokeh', views.bokeh, name='bokeh'),
]