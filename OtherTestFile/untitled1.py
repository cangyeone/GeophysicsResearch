# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 19:36:24 2017

@author: LLL
"""
import numpy as np
import matplotlib.pyplot as plt
per=100
f0=8
Tc=1/3
t=np.linspace(0,1,per)
wa=(1+np.cos(2.*np.pi*(t-Tc/2.)/Tc))*np.cos(2.*np.pi*f0*(t-Tc/2.))/2.




def Gdata(shape=[50,784]):
        sbn=np.random.randint(10)
        #data=np.random.random(shape)
        #data=np.subtract(data,0.5)
        data=np.zeros(shape)
        plt.plot(data[0][1:50])
        for itrd in range(shape[0]):
            for itr in range(sbn):
                f0=1+np.random.random(1)[0]*10
                Tc=1/(np.random.randint(5)+1)
                per=100
                t=np.linspace(0,1,per)
                wave=(1+np.cos(2.*np.pi*(t-Tc/2.)/Tc))*np.cos(2.*np.pi*f0*(t-Tc/2.))/2.
                nba=np.random.randint(shape[1]-per-1)
                data[itrd,nba:nba+per]=data[itrd,nba:nba+per]+wave
        plt.plot(data[0][1:50])
        plt.show()
Gdata(shape=[1,784])
np.max()
np.trnp