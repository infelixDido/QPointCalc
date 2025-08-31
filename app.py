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
from BZdrawer import BZ


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('calculator.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    space_group = float(data['space_group'])
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
    
    #print(f"Received: {a}, {b}, {c}, {aa}, {bb}, {cc}, {u}, {v}, {wl}, {two_theta}")

    lattice = lu.lattice(a, b, c, aa, bb, cc)
    recip_lattice = lu.recip_lattice(lattice)

    def get_lattice_vectors_json(lattice):
        basis = lu.basis_vectors(lattice)
        return [vec.tolist() for vec in basis]
    
    lattice_vectors = get_lattice_vectors_json(lattice)
    recip_lattice_vectors = get_lattice_vectors_json(recip_lattice)
    
    print(f"recip_lattice_vectors: {recip_lattice_vectors}")

    #fcc_vectors = [[-1, 1, 1],
    #                [1, -1, 1],
    #                [1, 1, -1]]
    #bcc_vectors = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]


    # Initialize everything to "P"
    SG_BRAVAIS_MAP = {i: "P" for i in range(1, 231)}

    # Overwrite with exceptions
    overrides = {
        5: "C", 8: "C", 9: "C", 12: "C", 15: "C", 20: "C", 21: "C",
        22: "F",
        23: "I", 24: "I",
        35: "C", 36: "C", 37: "C",
        38: "A", 39: "A", 40: "A", 41: "A",
        42: "F", 43: "F",
        44: "I", 45: "I", 46: "I",
        63: "C", 64: "C", 65: "C", 66: "C", 67: "C", 68: "C",
        69: "F", 70: "F",
        71: "I", 72: "I", 73: "I", 74: "I",
        79: "I", 80: "I",
        82: "I",
        87: "I", 88: "I",
        97: "I", 98: "I",
        107: "I", 108: "I", 109: "I", 110: "I",
        119: "I", 120: "I", 121: "I", 122: "I",
        139: "I", 140: "I", 141: "I", 142: "I",
        146: "R",
        148: "R",
        155: "R",
        160: "R", 161: "R",
        166: "R", 167: "R",
        196: "Fc",
        197: "Ic",
        199: "Ic",
        202: "Fc", 203: "Fc",
        204: "Ic",
        206: "Ic",
        209: "Fc", 210: "Fc",
        211: "Ic",
        214: "Ic",
        216: "Fc",
        217: "Ic",
        219: "Fc",
        220: "Ic",
        225: "Fc", 226: "Fc", 227: "Fc", 228: "Fc",
        229: "Ic", 230: "Ic"
    }

    # Apply overrides
    SG_BRAVAIS_MAP.update(overrides)

    # Determine Bravais lattice type
    bravais_type = SG_BRAVAIS_MAP.get(space_group, "P")

    # Default: use the reciprocal lattice basis directly
    kvector = np.array(recip_lattice_vectors)

    # Apply transformation for C-centered lattice
    if bravais_type == "C":
        # Transformation matrix from screenshot
        T_C = np.array([
            [0.5, -0.5, 0],
            [0.5,  0.5, 0],
            [0.0,  0.0, 1]
        ])
        kvector = (T_C @ kvector)
        print(f"Applied C-centered transform, kvector = {kvector}")
    elif bravais_type == "A":
        # Transformation matrix for A-centered lattice
        T_A = np.array([
            [0.5, -0.5, 0],
            [0.5, 0.5, 0],
            [0, 0, 1]
        ])
        # Transform the basis
        kvector = (T_A @ kvector)
        print(f"Applied A-centered transform, kvector = {kvector}")
    elif bravais_type == "F":
        # Transformation matrix for F-centered lattice
        T_F = np.array([
            [-0.5, 0.5, 0.5],
            [0.5,  -0.5, 0.5],
            [0.5, 0.5, -0.5]
        ])
        # Transform the basis
        kvector = (T_F @ kvector)
        print(f"Applied F-centered transform, kvector = {kvector}")
    elif bravais_type == "I":
        # Transformation matrix for I-centered lattice
        T_I = np.array([
            [0, 0.5, 0.5],
            [0.5, 0, 0.5],
            [0.5, 0.5, 0]
        ])
        kvector = (T_I @ kvector)
        print(f"Applied I-centered transform, kvector = {kvector}")
    elif bravais_type == "R":
        # Transformation matrix for R-centered lattice
        T_R = np.array([
            [0.666, 0.333, 0.333],
            [-0.333, 0.333, 0.333],
            [-0.333, -0.666, 0.333]
        ])
        kvector = (T_R @ kvector)
        print(f"Applied R-centered transform, kvector = {kvector}")
    elif bravais_type == "Fc":
        # Transformation matrix for face-centered cubic lattice
        T_Fc = np.array([
            [-0.5, 0.5, 0.5],
            [0.5, -0.5, 0.5],
            [0.5, 0.5, -0.5]
        ])
        kvector = (T_Fc @ kvector)
        print(f"Applied Fc-centered transform, kvector = {kvector}")
    elif bravais_type == "Ic":
        # Transformation matrix for body-centered cubic lattice
        T_Ic = np.array([
            [0, 0.5, 0.5],
            [0.5, 0, 0.5],
            [0.5, 0.5, 0]
        ])
        kvector = (T_Ic @ kvector)
        print(f"Applied Ic-centered transform, kvector = {kvector}")
    else:
        print(f"Using default reciprocal lattice for {bravais_type}, kvector = {kvector}")

    # Now compute BZ from the chosen primitive reciprocal lattice
    brillouin_zone = BZ(kvector)
    brillouin_zone.bulkBZ()


    bz_vertices = [p.tolist() for p in brillouin_zone.hs_points]
    bz_edges = []
    for line in brillouin_zone.hs_lines_f:
        d = line[:3]       # direction vector
        p0 = line[3:6]     # a point on the line
        t_min = line[6]
        t_max = line[7]
        start = (p0 + t_min * d).tolist()
        end   = (p0 + t_max * d).tolist()
        bz_edges.append({'start': start, 'end': end})

    #print(f"bz stuff: {bz_vertices} {bz_edges}")
    #print(f"Lattice Vectors {lattice_vectors}")
    #print(f"Recipricol Lattice Vectors {recip_lattice_vectors}")

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
        "reciprocal_lattice_visual": recip_lattice_vectors,
        'bz_vertices': bz_vertices,
        'bz_edges': bz_edges,
    })

if __name__ == '__main__':
    app.run(debug=True)