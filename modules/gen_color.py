import matplotlib.pyplot as plt
import numpy as np
from modules.gamap_colormap import WhGrYlRd
from matplotlib.colors import to_hex, to_rgb, CSS4_COLORS, LinearSegmentedColormap, ListedColormap
from matplotlib.cm import ScalarMappable
def find_closest_name(col):
    rv, gv, bv = to_rgb(col)
    min_colors = {}
    for col in CSS4_COLORS:
        rc, gc, bc = to_rgb(col)
        min_colors[(rc - rv) ** 2 + (gc - gv) ** 2 + (bc - bv) ** 2] = col
    closest = min(min_colors.keys())
    return min_colors[closest], np.sqrt(closest)




def semi_wgyr_cmap():
    vals = np.linspace(0, 1, 12)
    [(val, to_hex(WhGrYlRd(val))) for val in vals]
    semi_wgyr = [find_closest_name(WhGrYlRd(val))[0] for val in vals]
    return semi_wgyr