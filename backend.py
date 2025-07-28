import numpy as np
import matplotlib.pyplot as plt
from math import sin, cos, asin, acos, pi

class Lattice:
    def __init__(self, a=1.0, b=1.0, c=1.0, aa=90.0, bb=90.0, cc=90.0):
        """
        Class representing a crystallographic lattice.
        """
        self.a = a
        self.b = b
        self.c = c
        self.aa = np.deg2rad(aa)
        self.bb = np.deg2rad(bb)
        self.cc = np.deg2rad(cc)
        self.gtensor = self.compute_gtensor()
    
    def __str__(self):
        return f"""
        Lattice Parameters:
        a = {self.a:.4f}, b = {self.b:.4f}, c = {self.c:.4f}
        alpha = {np.rad2deg(self.aa):.3f}, beta = {np.rad2deg(self.bb):.3f}, gamma = {np.rad2deg(self.cc):.3f}
        """
    
    def compute_gtensor(self):
        """
        Compute and return the metric tensor of the lattice.
        """
        g = np.empty((3, 3))
        g[0, 0] = self.a ** 2
        g[0, 1] = self.a * self.b * np.cos(self.cc)
        g[0, 2] = self.a * self.c * np.cos(self.bb)
        g[1, 0] = g[0, 1]
        g[1, 1] = self.b ** 2
        g[1, 2] = self.b * self.c * np.cos(self.aa)
        g[2, 0] = g[0, 2]
        g[2, 1] = g[1, 2]
        g[2, 2] = self.c ** 2
        return g
    
    def compute_volume(self):
        """
        Compute the unit cell volume.
        """
        return self.a * self.b * self.c * np.sqrt(1 - cos(self.aa)**2 - cos(self.bb)**2 - cos(self.cc)**2 + 2 * cos(self.aa) * cos(self.bb) * cos(self.cc))


def compute_reciprocal_lattice(lattice):
    """
    Compute and return the reciprocal lattice parameters.
    """
    volume = lattice.compute_volume()
    a_star = 2 * pi * lattice.b * lattice.c * sin(lattice.aa) / volume
    b_star = 2 * pi * lattice.a * lattice.c * sin(lattice.bb) / volume
    c_star = 2 * pi * lattice.a * lattice.b * sin(lattice.cc) / volume
    
    aa_star = acos((cos(lattice.bb) * cos(lattice.cc) - cos(lattice.aa)) / (sin(lattice.bb) * sin(lattice.cc)))
    bb_star = acos((cos(lattice.aa) * cos(lattice.cc) - cos(lattice.bb)) / (sin(lattice.aa) * sin(lattice.cc)))
    cc_star = acos((cos(lattice.aa) * cos(lattice.bb) - cos(lattice.cc)) / (sin(lattice.aa) * sin(lattice.bb)))
    
    return Lattice(a_star, b_star, c_star, np.rad2deg(aa_star), np.rad2deg(bb_star), np.rad2deg(cc_star))

def angle(V1, V2, lattice):
    """
    Compute the angle between two vectors in degrees.
    """
    g = lattice.gtensor
    dot_product = np.dot(V1, np.dot(g, V2))
    norm1 = np.sqrt(np.dot(V1, np.dot(g, V1)))
    norm2 = np.sqrt(np.dot(V2, np.dot(g, V2)))
    return np.degrees(np.arccos(dot_product / (norm1 * norm2)))

def run_cases(lattice, theta_angles, directions, wl, tth):
    """
    Compute Q vectors for different theta and directions.
    """
    for n, u in enumerate(directions):
        for theta in theta_angles:
            print(f'phi = {n * 45} deg, u = {u}, theta = {theta} deg')
            Q = calc_q(lattice, tth, theta, wl, u, [1, 1, 1])
            print(f'Q = {np.round(Q, 3)}')

def dynamic_range_plot(Efixed, E, E_max, theta_range=[10, 120], step=10):
    """
    Plot the accessible dynamic range in momentum-energy space.
    """
    omega = np.linspace(0, E_max, 100)
    theta_s = np.arange(theta_range[0], theta_range[1], step) * pi / 180
    Q = np.empty([theta_s.size, omega.size], float)

    if Efixed == "Ef":
        kf = np.sqrt(E / 2.072)
        ki = np.sqrt((omega + E) / 2.072)
    elif Efixed == "Ei":
        ki = np.sqrt(E / 2.072)
        kf = np.sqrt((E - omega) / 2.072)

    for i, theta in enumerate(theta_s):
        Q[i] = np.sqrt(ki**2 + kf**2 - 2 * ki * kf * np.cos(theta))
        plt.plot(Q[i], omega, '--', label=r"$2\theta_s$ =" f"{np.round(theta * 180 / pi, 1)}$^o$")
    
    plt.xlabel(r'Q ($\AA^{-1}$)')
    plt.ylabel('Energy Transfer (meV)')
    plt.title(f'Accessible dynamic range for {Efixed} fixed = {E} meV')
    plt.legend()
    plt.grid()
    plt.show()

def user_input_lattice():
    """
    Allow user to input lattice parameters and compute the reciprocal cell.
    """
    a = float(input("Enter lattice parameter a: "))
    b = float(input("Enter lattice parameter b: "))
    c = float(input("Enter lattice parameter c: "))
    aa = float(input("Enter angle alpha (degrees): "))
    bb = float(input("Enter angle beta (degrees): "))
    cc = float(input("Enter angle gamma (degrees): "))
    lattice = Lattice(a, b, c, aa, bb, cc)
    recip_lattice = compute_reciprocal_lattice(lattice)
    print("Reciprocal Lattice:")
    print(recip_lattice)
    return lattice, recip_lattice

def miller_indices(V, lattice):
    """
    Compute Miller indices from fractional coordinates.
    """
    g = lattice.gtensor
    h = (g[0, 0] * V[0] + g[1, 0] * V[1] + g[2, 0] * V[2]) / (2. * pi)
    k = (g[0, 1] * V[0] + g[1, 1] * V[1] + g[2, 1] * V[2]) / (2. * pi)
    l = (g[0, 2] * V[0] + g[1, 2] * V[1] + g[2, 2] * V[2]) / (2. * pi)
    return [h, k, l]

def vector_magnitude(V, lattice):
    """
    Compute magnitude of a vector given its Miller indices.
    """
    return np.sqrt(np.dot(V, np.dot(lattice.gtensor, V)))

def d_spacing(V, reciprocal_lattice):
    """
    Compute the d-spacing corresponding to given Miller indices.
    """
    return 2 * pi / vector_magnitude(V, reciprocal_lattice)

def bragg_angle(wavelength, q, reciprocal_lattice):
    """
    Compute Bragg angle for given wavelength and reciprocal lattice vector.
    """
    d = d_spacing(q, reciprocal_lattice)
    theta = np.degrees(asin(wavelength / (2 * d)))
    print(f"\td = {d:.3f}, wavelength = {wavelength:.2f}, Q = {q}, Two-theta = {2 * theta:.3f}")
    return 2 * theta

def calc_q(lattice, tth, th, wl=651, u=[1, 0, 0], v=[0, 0, 1], eV=True):
    """
    Compute the Q value for elastic scattering in Miller indices.
    If eV=True, the wavelength is treated as energy in eV and converted to inverse Angstroms.
    """
    if eV:
        wl = 12.398 / wl  # Convert eV to inverse Angstroms
    
    modQ = 4 * pi / wl * sin(np.radians(tth / 2))
    alpha = (180 - tth) / 2 + th
    
    reciprocal_lattice = compute_reciprocal_lattice(lattice)
    u, v = np.array(u, dtype=np.float64), np.array(v, dtype=np.float64)
    
    u /= np.linalg.norm(u)
    v -= np.dot(v, u) * u
    v /= np.linalg.norm(v)
    
    qx, qy = modQ * cos(np.radians(alpha)) * u, modQ * sin(np.radians(alpha)) * v
    return qx + qy


def dynamic_range(Efixed, E, E_max, theta_range=[10, 120], step=10, color='k', showplot=True):
    """
    Plot the accessible dynamic range in momentum-energy space.
    """
    omega = np.linspace(0, E_max, 100)
    theta_s = np.arange(theta_range[0] * np.pi / 180, theta_range[1] * np.pi / 180, step * np.pi / 180)
    Q = []

    if Efixed == "Ef":
        kf = np.sqrt(E / 2.072)
        ki = np.sqrt((omega + E) / 2.072)
    elif Efixed == "Ei":
        ki = np.sqrt(E / 2.072)
        kf = np.sqrt((E - omega) / 2.072)

    for i, theta in enumerate(theta_s):
        Q_row = np.sqrt(ki ** 2 + kf ** 2 - 2 * ki * kf * np.cos(theta))
        Q.append(Q_row.tolist())
    
    return {
        "theta_angles": theta_s.tolist(),
        "omega": omega.tolist(),
        "Q": Q
    }

if __name__ == "__main__":
    lattice, recip_lattice = user_input_lattice()
    
    angle_between = angle([1, 0, 0], [0, 1, 0], recip_lattice)
    print(f"Angle between [1,0,0] and [0,1,0]: {angle_between:.3f} degrees")
    
    theta_angles = [10, 20, 30]
    directions = [[1, 0, 0], [0, 1, 0]]
    run_cases(lattice, theta_angles, directions, 1.54, 45)
    dynamic_range_plot("Ef", 10, 50)