import numpy as np
"""
A set of utilities for simple calculations involving crystal lattices
"""
def check_vecs(V1,V2):
    """
    Simple utility to check that V1 and V1 are of the same dimension 
    """
    if np.ndim(V1) > np.ndim(V2):
        np.tile(V2,(np.shape(V1)[1],1))
    else :
        np.tile(V1,(np.shape(V2)[1],1))
    return [V1,V2]
def gtensor(latt):
    
    """
    return the gtensor for a given lattice
    
    Arguments:
    latt -- is a lattice object
    """
    g = np.empty([3,3])
    
    g[0,0] = latt.a**2
    g[0,1] = latt.a*latt.b*np.cos(latt.cc)
    g[0,2] = latt.a*latt.c*np.cos(latt.bb)
    g[1,0] = g[0,1]
    g[1,1] = latt.b**2
    g[1,2] = latt.c*latt.b*np.cos(latt.aa)
    g[2,0] = g[0,2]
    g[2,1] = g[1,2]
    g[2,2] = latt.c**2
    return g
def Miller(V,latt):
    """
    Calculates the Miller indicies of a vector given by its fractional coordinates 
    """
    g = latt.gtensor
    
    h = (g[0,0]*V[0] + g[1,0]*V[1] + g[2,0]*V[2])/(2.*np.pi)
    k = (g[0,1]*V[0] + g[1,1]*V[1] + g[2,1]*V[2])/(2.*np.pi)
    l = (g[0,2]*V[0] + g[1,2]*V[1] + g[2,2]*V[2])/(2.*np.pi)
    return [h,k,l]
def recip_lattice(latt):
    """
    Calculate the reciprocal lattice given a real space lattice
    Arguments:
    latt -- is a lattice object
    """
    a_vect = np.array([latt.a, 0, 0])
    b_vect = np.array([latt.b*np.cos(latt.cc), latt.b*np.sin(latt.cc), 0])
    c_vect =latt.c*np.array([np.cos(latt.bb), 
			np.sin(latt.bb)*np.cos(latt.aa)*np.sin(latt.cc), 
			np.sin(latt.aa)*np.sin(latt.bb)])
   
    vol = np.sum(a_vect * np.cross(b_vect,c_vect))
    
    a_star = 2*np.pi*latt.b*latt.c*np.sin(latt.aa)/vol
    b_star = 2*np.pi*latt.a*latt.c*np.sin(latt.bb)/vol
    c_star = 2*np.pi*latt.a*latt.b*np.sin(latt.cc)/vol
    aa_star = np.arccos((np.cos(latt.bb)*np.cos(latt.cc)-np.cos(latt.aa))/(np.sin(latt.bb)*np.sin(latt.cc)))
    bb_star = np.arccos((np.cos(latt.aa)*np.cos(latt.cc)-np.cos(latt.bb))/(np.sin(latt.aa)*np.sin(latt.cc)))
    cc_star = np.arccos((np.cos(latt.aa)*np.cos(latt.bb)-np.cos(latt.cc))/(np.sin(latt.aa)*np.sin(latt.bb)))
    
    aa_star = np.rad2deg(aa_star)
    bb_star = np.rad2deg(bb_star)
    cc_star = np.rad2deg(cc_star)
    r_latt = lattice(a_star,b_star,c_star,aa_star,bb_star,cc_star)
    return r_latt
def angle(V1,V2,latt):
    """
    Calculate the angle, in degress, between two vectors defined by miller indicies in the space of the lattice.
    Arguments:
    V1 -- miller indicies defining a vector
    V2 -- miller indicies defining a second vector
    latt -- lattice object, can be either a real space or reciprocal space lattice
    """
    
   # if not isinstance(latt_,lattice)
   #     # some sort of error
    #V1,V2 = check_vecs(V1,V2) 
    a_vect = np.array([latt.a, 0, 0])
    b_vect = np.array([latt.b*np.cos(latt.cc), latt.b*np.sin(latt.cc), 0])
    c_vect =latt.c*np.array([np.cos(latt.bb), 
			np.sin(latt.bb)*np.cos(latt.aa)*np.sin(latt.cc), 
			np.sin(latt.aa)*np.sin(latt.bb)])
    vect1 = a_vect[:,np.newaxis]*V1[0] + b_vect[:,np.newaxis]*V1[1] + c_vect[:,np.newaxis]*V1[2]
    vect2 = a_vect[:,np.newaxis]*V2[0] + b_vect[:,np.newaxis]*V2[1] + c_vect[:,np.newaxis]*V2[2]
    nrmV1 = np.sqrt(np.sum(vect1**2))
    nrmV2 = np.sqrt(np.sum(vect2**2))
    # exploit broadcasting to deal with V1 and V2 of different sizes
    angle = np.rad2deg(np.arccos((vect1[0]*vect2[0]+vect1[1]*vect2[1]+vect1[2]*vect2[2])/(nrmV1*nrmV2)))
    return angle
def angle2(V1,V2,lattice):
    """
    Calculate the angle, in radian, between two vectors in real space and in reciprocal space.
    Real space vector V1 is in fractional cell coordinates
    Reciprocal space vector V2 is in Miller indicies
    Arguments:
    V1 -- fractional real space coordinates defining a vector
    V2 -- miller indicies defining a second vector
    lattice -- lattice object, defines a real space lattice
    """
    rlatt = recip_lattice(lattice)
    phi = np.arccos((2*np.pi*(V1[0]*V2[0]+V1[1]*V2[1]+V1[2]*V2[2]))/modVec(V1,lattice)/modVec(V2,rlatt))
    
    return phi
def scalar(V1,V2,latt):
    """
    Calculates the scalar product of two vectors defined by their Miller indicies
    Arguments:
    V1 -- miller indicies defining a vector
    V2 -- miller indicies defining a second vector
    latt -- lattice object, can be either a real space or reciprocal space lattice
    """
    # calculate the scalar product of two vectors defined by their Miller indicies
    [x1,y1,z1] = V1
    [x2,y2,z2] = V2
    #(latt.cc,latt.bb,latt.aa)
    s1 = x1*x2*latt.a**2 + y1*y2*latt.b**2 + z1*z2*latt.c**2
    s2 = (x1*y2 + x2* y1) * latt.a *latt.b*np.cos(latt.cc)
    s3 = (x1*z2 + x2* z1) * latt.a *latt.c*np.cos(latt.bb)
    s4 = (z1*y2 + z2* y1) * latt.c *latt.b*np.cos(latt.aa)
    s = s1+s2+s3+s4
    
    return s    
def vector(V1,V2,latt):
    """
    Calculates the vector product of two vectors defined by their Miller indicies
    Arguments:
    V1 -- miller indicies defining a vector
    V2 -- miller indicies defining a second vector
    latt -- lattice object, can be either a real space or reciprocal space lattice
    """
    u = (V1[1]*V2[2]-V2[1]*V1[2])
    v = (V1[2]*V2[0]-V2[2]*V1[0])
    w = (V1[0]*V2[1]-V2[0]*V1[1])
    
    [X,Y,Z] = Miller([u,v,w],latt)
    
    return [X,Y,Z]
    
def modVec(V1,latt):
    """
    Calculates the magnitude of a vector defined by its Miller indicies
    Arguments:
    V1 -- Miller indicies defining a vector
    latt -- lattice object, can be either a real of reciprocal space lattice
    """
    mod = np.sqrt(scalar(V1,V1,latt))
    return mod
def dspacing(V1,r_latt):
    """
    Calculates the d spacing corresponding to a given set of Miller indicies
    Arguments:
    V1 -- Miller indicies defining a partular reflection
    r_latt -- reciprocal space lattice
    """
    d = 2*np.pi/modVec(V1,r_latt)
    return d
def basis_vectors(latt):
    a = latt.a
    b = latt.b
    c = latt.c
    alpha = latt.aa
    beta = latt.bb
    gamma = latt.cc

    va = np.array([a, 0, 0])
    vb = np.array([b * np.cos(gamma), b * np.sin(gamma), 0])
    
    cx = c * np.cos(beta)
    cy = c * (np.cos(alpha) - np.cos(beta) * np.cos(gamma)) / np.sin(gamma)
    cz = np.sqrt(c**2 - cx**2 - cy**2)
    vc = np.array([cx, cy, cz])

    return np.array([va, vb, vc])
class lattice:
    def __init__(self,a=1.,b=1.,c=1.,aa=90.,bb=90.,cc=90.):
        self.a = a
        self.b = b
        self.c = c
        self.aa = np.deg2rad(aa)
        self.bb = np.deg2rad(bb)
        self.cc = np.deg2rad(cc)
        self.lvec = [a,b,c,np.deg2rad(aa),np.deg2rad(bb),np.deg2rad(cc)]
        self.gtensor = gtensor(self)
    def __str__(self):
        out1 = '\ta = {0:.4f}, b = {1:.4f}, c = {2:.4f} \n'.format(self.a,self.b,self.c)
        out2 = '\talpha = {0:.3f},  beta = {1:.3f}, gamma = {2:.3f} \n'.format(self.aa,self.bb,self.cc)
        out = out1 + out2
        return out 
    def __expr__(self):
        out = 'lattice constants: [{0} {1} {2}] \n angles: [{3} {4} {5}]'.format(self.a,self.b,self.c, self.aa,self.bb.self.cc)
        return out 
    def __repr__(self):
        return self.__str__()

                                 
 