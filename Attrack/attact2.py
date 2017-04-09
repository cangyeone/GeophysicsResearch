# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 10:44:43 2016

@author: Q
"""

from scipy.integrate import odeint 
import numpy as np 

def lorenz(w,t,a1,a2,a3,a4,a5,a6): 
    x, y, z = w
    return np.array([a1*(y-x)+a4*x*z,a2*x-x*z+a6*y,a3*z+x*y-a5*x*x]) 

t = np.arange(0, 3, 0.001) # 创建时间点 
# 调用ode对lorenz进行求解, 用两个不同的初始值 
track1 = odeint(lorenz, (1.1, 0, 0.0), t, args=(40,55,1.833,0.16,0.65,20)) 
track2 = odeint(lorenz, (4, 0, 0), t, args=(41,55,1.833,0.16,0.65,20)) 
track3 = odeint(lorenz, (6, 0, 0), t, args=(42,55,1.833,0.16,0.65,20)) 
# 绘图
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 

fig = plt.figure()
ax = Axes3D(fig)
ax.plot(track1[:,0], track1[:,1], track1[:,2],color='cornflowerblue',lw=2,alpha=0.5)
ax.plot(track2[:,0], track2[:,1], track2[:,2],color='orange',lw=2,alpha=0.5)
ax.plot(track3[:,0], track3[:,1], track3[:,2],color='b',lw=2,alpha=0.5)
plt.show()