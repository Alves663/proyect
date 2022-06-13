from django.shortcuts import render
from django.http import HttpResponse
from app.olistdata import OlistData
from app.plotutils import plot_map, plot_bars
from colorcet import rainbow
import datashader as ds
import holoviews as hv
import pandas as pd
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
                   rainbow).options(height=600, width=500)
    consumidores_div = renderer.html(consumidores_img)
    #Vendedores
    vendedores_distribution = olist_data.get_seller_distribution()
    agg_name_seller = "seller_id"
    vendedores_img = plot_map(vendedores_distribution, "Distribución de los Vendedores", ds.mean(agg_name_seller),
             agg_name_seller, rainbow).options(height=600, width=500)
    vendedores_div = renderer.html(vendedores_img)
    revenue = olist_data.get_incomes()
    agg_name_revenue = 'revenue'
    revenue = renderer.html(plot_map(revenue, "Ingresos en miles de R$", ds.mean(agg_name_revenue), agg_name_revenue,
                                     rainbow).options(height=600, width=500))

    return render(request, 'app/compradores_vendedores.html',
                  {'div_cosumidores': consumidores_div, 'div_vendedores': vendedores_div, 'revenue': revenue})


def top_products(request):
    years = {k: False for k in range(2016, 2018 + 1)}
    years["All"] = True
    months = {k: False for k in range(1, 12 + 1)}
    months["All"] = True
    return render(request, 'app/top_products.html', {'years': years, 'months': months, 'top_categories': "",
                                                     'top_products': ""})


def ajax_top_products(request):
    if request.method == "POST":
        year = request.POST.get('year')
        month = request.POST.get('month')
        ntop = int(request.POST.get('ntop'))
        if year == "All":
            year = None
        else:
            year = int(float(year))
        if month == "All":
            month = None
        else:
            month = int(float(month))
        olist_data = OlistData()
        order_items_sell = olist_data.product_buy_by_costumer(year=year, month=month)
        years = {k: False for k in range(2016, 2018+1)}
        years["All"] = False
        months = {k: False for k in range(1, 12+1)}
        months["All"] = False
        if year is None:
            years["All"] = True
        else:
            years[year] = True
        if month is None:
            months["All"] = True
        else:
            months[month] = True

        top_product_data, top_categories_data = olist_data.product_best_sellers(order_items_sell, n_top=ntop)
        top_product = renderer.html(plot_bars(top_product_data, title="Top Productos").options(height=600, width=500))
        top_categories = renderer.html(plot_bars(top_categories_data, title="Top Categorías de Productos").options(height=600, width=500))
        top_products_by_costumer = olist_data.top_products_by_costumer(order_items_sell)
        agg_name_top_products_by_costumer = "order_item_id"
        top_products_by_costumer_img = renderer.html(plot_map(top_products_by_costumer,
                                                              f"Top Sellers. Año {year} y Mes {month}",
                                                ds.mean(agg_name_top_products_by_costumer),
                                                agg_name_top_products_by_costumer, rainbow).options(height=600, width=600))

        return render(request, 'app/top_products.html', {'years': years, 'months': months,
                                                         'top_categories': top_categories,
                                                         'top_products': top_product,
                                                         'top_products_by_costumer_img': top_products_by_costumer_img})
