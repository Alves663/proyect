from django.shortcuts import render
from django.http import HttpResponse
from bokeh.plotting import figure
from bokeh.embed import components
# Create your views here.


def index(request):
    return render(request, 'app/index.html')


def bokeh(request):
    plot = figure(plot_width=400, plot_height=400)
    plot.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
    script, div = components(plot)
    return render(request, 'app/bokeh.html', {'script': script, 'div': div})


