# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 19:32:40 2016

@author: Q
"""

from scipy.integrate import odeint 
import numpy as np 

def lorenz(w, t, p, r, b): 
    # 给出位置矢量w，和三个参数p, r, b计算出
    # dx/dt, dy/dt, dz/dt的值
    x, y, z = w
    # 直接与lorenz的计算公式对应 
   
    return np.array([-y-z, x+p*y, r+z*(x-b)]) 

t = np.arange(0, 66, 0.01) # 创建时间点 
# 调用ode对lorenz进行求解, 用两个不同的初始值 
track1 = odeint(lorenz, (1.1, 0, 0.0), t, args=(0.2,0.2,5.7)) 
track2 = odeint(lorenz, (1, 0, 0), t, args=(0.2,0.2,5.7)) 
track3 = odeint(lorenz, (2, 0, 0), t, args=(0.2,0.2,5.7)) 
# 绘图
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 

fig = plt.figure()
ax = Axes3D(fig)
ax.plot(track1[:,0], track1[:,1], track1[:,2],color='cornflowerblue',lw=3)
ax.plot(track2[:,0], track2[:,1], track2[:,2],color='orange',lw=3)
ax.plot(track3[:,0], track3[:,1], track3[:,2],color='b',lw=3,alpha=0.5)
plt.show()