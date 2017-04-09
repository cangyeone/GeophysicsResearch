# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 10:56:46 2016

@author: Q
"""

from scipy.integrate import odeint 
import numpy as np 

def lorenz(w,t,a1,a2,a3,a4,a5,a6,a7): 
    x, y, z = w
    return np.array([a1*y+a2*x+a3*y*z,a4*y-z+a5*x*z,a6*z+a7*x*y]) 

t = np.arange(0,60, 0.001) # 创建时间点 
# 调用ode对lorenz进行求解, 用两个不同的初始值 
track1 = odeint(lorenz, (5, 5, 5), t, args=(2.4,-3.78,14,-11,4,5.58,1)) 
track2 = odeint(lorenz, (1.3, 0, 0), t, args=(2.4,-3.78,14,-11,4,5.58,1)) 
track3 = odeint(lorenz, (1.6, 0, 0), t, args=(2.4,-3.78,14,-11,4,5.58,1)) 
# 绘图
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 

fig = plt.figure()
ax = Axes3D(fig)
ax.plot(track1[:,0], track1[:,1], track1[:,2],color='cornflowerblue',lw=2,alpha=0.5)
ax.plot(track2[:,0], track2[:,1], track2[:,2],color='orange',lw=2,alpha=0.5)
ax.plot(track3[:,0], track3[:,1], track3[:,2],color='b',lw=2,alpha=0.5)
plt.show()