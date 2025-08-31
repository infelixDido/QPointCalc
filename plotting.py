import lattice_utils as lu
import numpy as np
import planning as pla
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from math import pi,asin,sin, cos
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator,StrMethodFormatter

def get_theta_cut_plot_data(u, v, lat, rlat, wl, two_theta):
    plot_data = {"traces": [], "layout": {}}
    colors = ['maroon', 'blue', 'black']
    modu = lu.modVec(u, rlat)
    modv = lu.modVec(v, rlat)

    for j, tth in enumerate(two_theta):
        th = np.arange(5,tth-5+1,5)
        x_vals = []
        y_vals = []
        
        for n in th:
            modQ, angle, X, Y = pla.calcQ(lat, tth, n, wl=wl, u=u, v=v)
            x_vals.append(float(modQ * cos(angle / 180 * pi) / modu))
            y_vals.append(float(modQ * sin(angle / 180 * pi) / modv))
        

        trace = {
            "x": x_vals,
            "y": y_vals,
            "mode": "lines",
            "line": {"dash": "dot", "color": colors[j % len(colors)]},
            "name": f"2θ = {tth}",
        }

        plot_data["traces"].append(trace)

    
    plot_data["layout"] = {
        "xaxis": {"title": f"{u} (r.l.u.)", "range": [-0.35, 0.35]},
        "yaxis": {"title": f"{v} (r.l.u.)", "range": [0.0, 0.25]},

        
        "title": "Theta Cuts for Lattice",
        "hovermode": False,
    }
              
    return plot_data