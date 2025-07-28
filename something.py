import lattice_utils as lu
import numpy as np
import planning as pla
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from math import pi,asin,sin, cos
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MultipleLocator,StrMethodFormatter


frame = False; fancy = True; shadow = False; facecolor='white'
legendpad = 0.2; hlength = 0.75
legendsize = 8
lettersize = 6
fig = plt.figure(figsize=(6,3))
gs = gridspec.GridSpec(1,2)
fig.subplots_adjust(left = 0.15,right = 0.98, bottom = 0.20, top = 0.9,wspace=.3,hspace=.1)
ax0 = fig.add_subplot(gs[1])
ax1 = fig.add_subplot(gs[0])
colors = ['maroon','blue','k']
notes=['Ti L','','']
#-----------------------------------
lat = lu.lattice(a=4.127,b=4.127,c=5.451,aa=90,bb=90,cc=120)
rlat=lu.recip_lattice(lat)
print('first----------------------------')
v = [-1,2,0]
u = [1,0,0]
modu = lu.modVec(u, rlat)
modv = lu.modVec(v, rlat)    
ax0.set_aspect(modv/modu)
two_theta = [90,110,130]
for j,tth in enumerate(two_theta):
 th = np.arange(5,tth-5+1,5)
 #th = [0,5,10,20,25,30,35,40,45,80]
 alpha = np.zeros_like(th)
 for i,n in enumerate(th):
    a,b,c,d=pla.calcQ(lat, tth, n, wl=26.8, u=u, v=v)
    alpha[i]=b


ax0.plot(a*np.cos(alpha[:]/180*pi)/modu,a*np.sin(alpha[:]/180*pi)/modv,color=colors[j],label=r'2$\theta$ = '+str(tth))
ax0.set_xlim(-.35,.35)
ax0.set_ylim(0,.25)
ax0.set_xlabel('[h,0,0] (r.l.u.)')
ax0.set_ylabel('[-h,2h,0] (r.l.u.)')
ax0.legend(fontsize=legendsize,handlelength=hlength,frameon=frame,fancybox=fancy,shadow=shadow,borderpad=legendpad,borderaxespad=0.2,facecolor=facecolor)


u = [0,0,1]
v = [-1,2,0]
modu = lu.modVec(u, rlat)
modv = lu.modVec(v, rlat)    
ax1.set_aspect(modv/modu)
for j,tth in enumerate(two_theta):
 th = np.arange(5,tth-5+1,5)
 print(th)
 #th = [0,5,10,20,25,30,35,40,45]
 alpha = np.zeros_like(th)
 for i,n in enumerate(th):
    a,b,c,d=pla.calcQ(lat, tth,n, wl=26.8, u=u, v=v)
    alpha[i]=b
 ax1.plot(a*np.cos(alpha[:]/180*pi)/modu,a*np.sin(alpha[:]/180*pi)/modv,color=colors[j],label=r'2$\theta$ = '+str(tth))
ax1.set_ylim(0.,.25)
ax1.set_xlim(-.35,.35)
ax1.set_ylabel('[-h,2h,0] (r.l.u.)')
ax1.set_xlabel('[0,0,l] (r.l.u.)')
ax1.legend(fontsize=legendsize,handlelength=hlength,frameon=frame,fancybox=fancy,shadow=shadow,borderpad=legendpad,borderaxespad=0.2,facecolor=facecolor)


#plt.savefig('Theta_cuts.pdf')
plt.show()
 