# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 11:12:14 2017

@author: LLL
"""


from scipy.integrate import odeint 
import numpy as np 

def lorenz(w, t, p, r, b): 
    # 给出位置矢量w，和三个参数p, r, b计算出
    # dx/dt, dy/dt, dz/dt的值
    x, y = w
    # 直接与lorenz的计算公式对应 
   
    return np.array([-p*np.sin(t)-p*np.cos(t),r*np.cos(t)-r*np.sin(t)]) 

t = np.arange(0, 66, 0.01) # 创建时间点 
# 调用ode对lorenz进行求解, 用两个不同的初始值 
track1 = odeint(lorenz, (1.1,1), t, args=(1,1,1))  
track2 = odeint(lorenz, (3,2), t, args=(1,1,1)) 
track3 = odeint(lorenz, (5,1), t, args=(1,1,1))   
# 绘图
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 

fig = plt.figure()
plt.plot(track1[:,0], track1[:,1],color='cornflowerblue',lw=3)
plt.plot(track2[:,0], track2[:,1],color='b',lw=3)
plt.plot(track3[:,0], track3[:,1],color='orange',lw=3)
#ax.plot(track3[:,0], track3[:,1], track3[:,2],color='b',lw=3,alpha=0.5)
plt.show()