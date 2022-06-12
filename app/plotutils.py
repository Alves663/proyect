from holoviews.element.tiles import OSM
import holoviews as hv
from holoviews.operation.datashader import datashade, dynspread, rasterize
from holoviews import opts
from holoviews.streams import RangeXY

T = 0.05
PX = 1


def plot_map(data, label, agg_data, agg_name, cmap):
    geomap = OSM()
    points = hv.Points(hv.Dataset(data, kdims=['x', 'y'], vdims=[agg_name]))
    agg = datashade(points, element_type=hv.Image, aggregator=agg_data, cmap=cmap)
    zip_codes = dynspread(agg, threshold=T, max_px=PX)
    hover = hv.util.Dynamic(rasterize(points, aggregator=agg_data, width=50, height=25, streams=[RangeXY]),
                            operation=hv.QuadMesh)
    hover = hover.options(cmap=cmap)
    img = geomap * zip_codes * hover
    img = img.relabel(label)
    img.opts(opts.QuadMesh(tools=['hover'], colorbar=True, alpha=0, hover_alpha=0.2))
    img.opts(labelled=[])
    return img
