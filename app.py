from flask import Flask, render_template, jsonify, request, send_file
import sqlite3
#import matplotlib.pyplot as plt
#import pandas as pd
import io
import os
from datetime import datetime, timedelta
import lattice_utils as lu
import numpy as np
import planning as pla
from math import pi, asin, sin, cos
from plotting import get_theta_cut_plot_data
import plotly.graph_objects as go

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    a = float(data['param1'])
    b = float(data['param2'])
    c = float(data['param3'])
    aa = float(data['param4'])
    bb = float(data['param5'])
    cc = float(data['param6'])
    wl = float(data['param7'])
    u = data['u']
    v = data['v']
    r = data['r']
    w = data['w']
    two_theta = data['two_theta']
    
    print(f"Received: {a}, {b}, {c}, {aa}, {bb}, {cc}, {u}, {v}, {wl}, {two_theta}")

    lattice = lu.lattice(a, b, c, aa, bb, cc)
    recip_lattice = lu.recip_lattice(lattice)

    def get_lattice_vectors_json(lattice):
        basis = lu.basis_vectors(lattice)
        return [vec.tolist() for vec in basis]
    
    lattice_vectors = get_lattice_vectors_json(lattice)
    recip_lattice_vectors = get_lattice_vectors_json(recip_lattice)

    print(f"Lattice Vectors {lattice_vectors}")
    print(f"Recipricol Lattice Vectors {recip_lattice_vectors}")

    
    angle_between = lu.angle(u, v, recip_lattice)

    theta_cut_plot = get_theta_cut_plot_data(w, r, lattice, recip_lattice, wl, two_theta)
    #dynamic_result = pla.dynamic_range("Ef", 10, 50)

    return jsonify({
        "lattice": str(lattice),
        "reciprocal_lattice": str(recip_lattice),
        "angle": round(float(angle_between), 3),
        #"plot": dynamic_result,
        "theta_cut": theta_cut_plot,
        "lattice_visual": lattice_vectors,
        "reciprocal_lattice_visual": recip_lattice_vectors
    })
   

if __name__ == '__main__':
    app.run(debug=True)