from django.shortcuts import render
from django.http import HttpResponse
from app.olistdata import OlistData
from app.plotutils import plot_map
from colorcet import rainbow
import datashader as ds
import holoviews as hv
hv.extension('bokeh')
renderer = hv.renderer('bokeh')

# Create your views here.


def index(request):
    return render(request, 'app/index.html')


def compradores_vendedores(request):
    olist_data = OlistData()
    # Consumidores
    costumer_distribution = olist_data.get_costumer_distribution()
    agg_name_costumer = "customer_id"
    consumidores_img = plot_map(costumer_distribution, "Distribución de los Consumidores", ds.mean(agg_name_costumer), agg_name_costumer,
                   rainbow).options(height=500, width=500)
    consumidores_div = renderer.html(consumidores_img)
    #Vendedores
    vendedores_distribution = olist_data.get_seller_distribution()
    agg_name_seller = "seller_id"
    vendedores_img = plot_map(vendedores_distribution, "Distribución de los Vendedores", ds.mean(agg_name_seller),
             agg_name_seller, rainbow).options(height=500, width=500)
    vendedores_div = renderer.html(vendedores_img)

    return render(request, 'app/compradores_vendedores.html',
                  {'div_cosumidores': consumidores_div, 'div_vendedores': vendedores_div})


