# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 11:05:54 2017

@author: LLL
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 17:21:27 2017

@author: LLL
"""

import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
N=3000
class GenData():
    def __init__(self,shape):
        self.shape=shape
        self.data=np.zeros(self.shape)
    def GenWave(self):
        
        #data=np.random.random(shape)
        #data=np.subtract(data,0.5)
        ariv=np.zeros([self.shape[0],1])
        m=0
        for itrd in range(self.shape[0]):
            sbn=1+np.random.randint(30)
            m=m+1
            for itr in range(sbn):
                f0=1+np.random.random(1)[0]*10
                Tc=1/(np.random.randint(5)+1)
                per=100
                t=np.linspace(0,1,per)
                wave=(1+np.cos(2.*np.pi*(t-Tc/2.)/Tc))*np.cos(2.*np.pi*f0*(t-Tc/2.))/2.
                nba=np.random.randint(self.shape[1]-per-1)
                ariv[itrd][0]=1
                self.data[itrd,nba:nba+per]=self.data[itrd,nba:nba+per]+wave
            #mx=np.max(self.data[itrd])
            #self.data[itrd]=np.divide(self.data[itrd],mx)
            self.data[itrd]=np.add(self.data[itrd],m)
        
        return self.data
    def AddNoise(self,bl=0.5):
        noise=np.random.random(self.shape)
        noise=np.subtract(noise,0.5)
        noise=np.multiply(noise,bl)
        return np.add(self.data,noise)


batch = GenData([50,784])
data=batch.GenWave()
data_noise=batch.AddNoise(0.1)
plt.figure(1)
plt.plot(data,color='b',lw=1,alpha=0.2)
plt.figure(2)
plt.plot(data,color='b',lw=1,alpha=0.2)

plt.show()

        #outz.WriteData(data_noise)
    #outz.CleanFile()
        

















