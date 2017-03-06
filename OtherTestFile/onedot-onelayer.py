# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 09:19:44 2017

@author: LLL
"""

import tensorflow as tf
import numpy as np


class GenData():
    def __init__(self,shape):
        self.shape=shape
        self.data=np.random.random(self.shape)
    def Func(self,x):
        x=x[0]
        return [x*0.5+0.1]
    def GenWave(self,numSubWave=30):
        
        self.outdata=np.array(list(map(self.Func,self.data)))
        
        return self.data,self.outdata
    def AddNoise(self,bl=0.5,tp='FX'):
        noise=np.random.random(self.shape)
        noise=np.subtract(noise,0.5)
        if(tp=='RD'):
            bl=np.random.random(1)[0]*bl+0.0001
        noise=np.multiply(noise,bl)
        return np.add(self.data,noise)




x = tf.placeholder(tf.float32, [None,1])
y = tf.placeholder(tf.float32, [None,1])


W = tf.Variable(tf.zeros([1.,1.]))
b = tf.Variable(tf.zeros([1.]))

result = tf.nn.sigmoid(tf.matmul(x, W) + b)


cross_entropy = tf.reduce_mean(tf.abs(result-y))

train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
aa=GenData([50,1])

for _ in range(1000):
    dt,odt=aa.GenWave()
    sess.run(train_step, feed_dict={x: dt, y: odt})

dt,odt=aa.GenWave()
rdt=sess.run(result,feed_dict={x: dt, y: odt})
import matplotlib.pyplot as plt
cof = np.polyfit(np.reshape(dt,[-1]),np.reshape(rdt,[-1]),1) 
p=np.poly1d(cof)
plt.scatter(np.reshape(dt,[-1]),np.reshape(rdt,[-1]))
plt.text(0,0.1,'$f(x)=%20.15f+%20.15fx$'%(cof[1],cof[0]))
x=np.linspace(0,1,50)
plt.plot(x,p(x),lw=2)
plt.show()
    
  


















