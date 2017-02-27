# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 17:21:27 2017

@author: LLL
"""

import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
N=220
TN=2000
class GenData():
    def __init__(self,shape):
        self.shape=shape
        self.data=np.zeros(self.shape)
    def GenWave(self,numSubWave=30):
        
        #data=np.random.random(shape)
        #data=np.subtract(data,0.5)
        ariv=np.zeros([self.shape[0],1])
        if(numSubWave==0):
            return self.data
        
        for itrd in range(self.shape[0]):
            sbn=1+np.random.randint(numSubWave)
            for itr in range(sbn):
                f0=1+np.random.random(1)[0]*3
                Tc=1/(np.random.randint(5)+1)
                per=100
                t=np.linspace(0,1,per)
                wave=(1+np.cos(2.*np.pi*(t-Tc/2.)/Tc))*np.cos(2.*np.pi*f0*(t-Tc/2.))/2.
                nba=np.random.randint(self.shape[1]-per-1)
                ariv[itrd][0]=1
                self.data[itrd,nba:nba+per]=self.data[itrd,nba:nba+per]+wave
        mx=np.max(self.data,axis=1)
        mx=np.reshape(mx,[-1,1])
        self.data=np.multiply(np.divide(self.data,mx),0.2)
        #return ariv
        
        return self.data
    def AddNoise(self,bl=0.5,tp='FX'):
        noise=np.random.random(self.shape)
        noise=np.subtract(noise,0.5)
        if(tp=='RD'):
            bl=np.random.random(1)[0]*bl+0.0001
        noise=np.multiply(noise,bl)
        return np.add(self.data,noise)
def my_weigh(shape):
    init=tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(init)
def my_bias(shape):
    init=tf.constant(0.1,shape=shape)
    return tf.Variable(init)
import tensorflow as tf
x = tf.placeholder(tf.float32,[50,N])
y = tf.placeholder(tf.float32,[50,N])

c1s=[4,1,8]
c2s=[3,8,8]
c3s=[3,8,8]
c4s=[3,8,1]
c5s=[1,32,32]
c6s=[1,32,16]
c7s=[1,16,8]
c8s=[1,8,4]
c9s=[1,4,1]

pool_type='AVG'
kp_prb=tf.placeholder('float')
data1=tf.reshape(x,[50,N,1])
c1_w=my_weigh(c1s)
c1_b=my_weigh([c1s[2]])
c1_f1=tf.nn.conv1d(data1,filters=c1_w,stride=1, padding='SAME')+c1_b
c1_f2=tf.nn.tanh(c1_f1)
c1=tf.nn.pool(c1_f2,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')

c2_w=my_weigh(c2s)
c2_b=my_weigh([c2s[2]])
c2_f1=tf.nn.conv1d(c1,filters=c2_w,stride=1, padding='SAME')+c2_b
c2_f2=tf.nn.tanh(c2_f1)
c2_f2=tf.nn.dropout(c2_f2,kp_prb)
c2=tf.nn.pool(c2_f2,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')

c3_w=my_weigh(c3s)
c3_b=my_weigh([c3s[2]])
c3_f1=tf.nn.conv1d(c2,filters=c3_w,stride=1, padding='SAME')+c3_b
c3_f2=tf.nn.tanh(c3_f1)
c3_f2=tf.nn.dropout(c3_f2,kp_prb)
c3=tf.nn.pool(c3_f2,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')

c4_w=my_weigh(c4s)
c4_b=my_weigh([c4s[2]])
c4_f1=tf.nn.conv1d(c3,filters=c4_w,stride=1, padding='SAME')+c4_b
c4_f2=tf.nn.tanh(c4_f1)
c4_f2=tf.nn.dropout(c4_f2,kp_prb)
c4=tf.nn.pool(c4_f2,window_shape=[1],pooling_type='AVG',strides=[1],padding='SAME')
"""
c5_w=my_weigh(c5s)
c5_b=my_weigh([c5s[2]])
c5_f1=tf.nn.conv1d(c4,filters=c5_w,stride=1, padding='SAME')+c5_b
c5_f2=tf.nn.tanh(c5_f1)
c5_f2=tf.nn.dropout(c5_f2,kp_prb)
c5=tf.nn.pool(c5_f2,window_shape=[2],pooling_type='AVG',strides=[1],padding='SAME')

c6_w=my_weigh(c6s)
c6_b=my_weigh([c6s[2]])
c6_f1=tf.nn.conv1d(c5,filters=c6_w,stride=1, padding='SAME')+c6_b
c6_f2=tf.nn.tanh(c6_f1)
c6_f2=tf.nn.dropout(c6_f2,kp_prb)
c6=tf.nn.pool(c6_f2,window_shape=[2],pooling_type='AVG',strides=[1],padding='SAME')

c7_w=my_weigh(c7s)
c7_b=my_weigh([c7s[2]])
c7_f1=tf.nn.conv1d(c6,filters=c7_w,stride=1, padding='SAME')+c7_b
c7_f2=tf.nn.tanh(c7_f1)
c7_f2=tf.nn.dropout(c7_f2,kp_prb)
c7=tf.nn.pool(c7_f2,window_shape=[2],pooling_type='AVG',strides=[1],padding='SAME')

c8_w=my_weigh(c8s)
c8_b=my_weigh([c8s[2]])
c8_f1=tf.nn.conv1d(c7,filters=c8_w,stride=1, padding='SAME')+c8_b
c8_f2=tf.nn.tanh(c8_f1)
c8=tf.nn.pool(c8_f2,window_shape=[2],pooling_type='AVG',strides=[1],padding='SAME')

c9_w=my_weigh(c9s)
c9_b=my_weigh([c9s[2]])
c9_f1=tf.nn.conv1d(c8,filters=c9_w,stride=1, padding='SAME')+c9_b
c9_f2=tf.nn.tanh(c9_f1)
c9=tf.nn.pool(c9_f2,window_shape=[1],pooling_type='AVG',strides=[1],padding='SAME')
"""



data2=tf.reshape(c4,[50,N])

ce = tf.reduce_mean(tf.abs(data2-y))

train_step = tf.train.AdamOptimizer(1e-2).minimize(ce)
#train_step = tf.train.GradientDescentOptimizer(0.5).minimize(c3)
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

batch = GenData([50,N])
data=batch.GenWave()
data_noise=batch.AddNoise(0.1)
#print(sess.run(tf.shape(c2), feed_dict={x: data_noise, y: data,kp_prb:0.5}))



for itr in range(1000):
    if(itr%2!=7):
        data=batch.GenWave(5)
        data_noise=batch.AddNoise(0.00)
    else:
        data=batch.GenWave(0)
        data_noise=batch.AddNoise(0.1,tp='RD')
    sess.run(train_step, feed_dict={x: data_noise, y: data,kp_prb:0.5})
    #print(data[0])
    #plt.plot(data_noise[0])
    if(itr%100==0):
        print("%d:%f"%(itr,sess.run(ce, feed_dict={x: data_noise, y: data,kp_prb:1.})))
#conv_layer=sess.run(c1_w, feed_dict={x: data_noise, y: data,kp_prb:0.1})
batch2 = GenData([50,TN])
data=batch2.GenWave(15)
data_noise=batch2.AddNoise(0.2)

#============================================================================
kp_t=tf.placeholder('float')
x_t = tf.placeholder(tf.float32,[50,TN])
data_t=tf.reshape(x_t,[50,TN,1])

c1_f1_t=tf.nn.conv1d(data_t,filters=c1_w,stride=1, padding='SAME')+c1_b
c1_f2_t=tf.nn.tanh(c1_f1_t)
c1_t=tf.nn.pool(c1_f2_t,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')

c2_f1_t=tf.nn.conv1d(c1_t,filters=c2_w,stride=1, padding='SAME')+c2_b
c2_f2_t=tf.nn.tanh(c2_f1_t)
c2_f2_t=tf.nn.dropout(c2_f2_t,kp_t)
c2_t=tf.nn.pool(c2_f2_t,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')

c3_f1_t=tf.nn.conv1d(c2_t,filters=c3_w,stride=1, padding='SAME')+c3_b
c3_f2_t=tf.nn.tanh(c3_f1_t)
c3_f2_t=tf.nn.dropout(c3_f2_t,kp_t)
c3_t=tf.nn.pool(c3_f2_t,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')

c4_f1_t=tf.nn.conv1d(c3_t,filters=c4_w,stride=1, padding='SAME')+c4_b
c4_f2_t=tf.nn.tanh(c4_f1_t)
c4_f2_t=tf.nn.dropout(c4_f2_t,kp_t)
c4_t=tf.nn.pool(c4_f2_t,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')
"""
c5_f1_t=tf.nn.conv1d(c4_t,filters=c5_w,stride=1, padding='SAME')+c5_b
c5_f2_t=tf.nn.tanh(c5_f1_t)
c5_f2_t=tf.nn.dropout(c5_f2_t,kp_t)
c5_t=tf.nn.pool(c5_f2_t,window_shape=[2],pooling_type='AVG',strides=[1],padding='SAME')

c6_f1_t=tf.nn.conv1d(c5_t,filters=c6_w,stride=1, padding='SAME')+c6_b
c6_f2_t=tf.nn.tanh(c6_f1_t)
c6_f2_t=tf.nn.dropout(c6_f2_t,kp_t)
c6_t=tf.nn.pool(c6_f2_t,window_shape=[2],pooling_type='AVG',strides=[1],padding='SAME')

c7_f1_t=tf.nn.conv1d(c6_t,filters=c7_w,stride=1, padding='SAME')+c7_b
c7_f2_t=tf.nn.tanh(c7_f1_t)
c7_f2_t=tf.nn.dropout(c7_f2_t,kp_t)
c7_t=tf.nn.pool(c7_f2_t,window_shape=[2],pooling_type='AVG',strides=[1],padding='SAME')

c8_f1_t=tf.nn.conv1d(c7_t,filters=c8_w,stride=1, padding='SAME')+c8_b
c8_f2_t=tf.nn.tanh(c8_f1_t)
c8_f2_t=tf.nn.dropout(c8_f2_t,kp_t)
c8_t=tf.nn.pool(c8_f2_t,window_shape=[2],pooling_type='AVG',strides=[1],padding='SAME')

c9_f1_t=tf.nn.conv1d(c8_t,filters=c9_w,stride=1, padding='SAME')+c9_b
c9_f2_t=tf.nn.tanh(c9_f1_t)
c9_t=tf.nn.pool(c9_f2_t,window_shape=[1],pooling_type='AVG',strides=[1],padding='SAME')
"""
kp_prb=tf.placeholder('float')
data2_t=tf.reshape(c4_t,[50,TN])

#===========================================================================
outdata=sess.run(data2_t, feed_dict={x_t: data_noise,kp_prb:1,kp_t:1})

cvl1=(np.transpose(np.reshape(sess.run(c1_w.value()),[c1s[0],c1s[2]])))
plt.figure(1)
plt.subplot(511)
plt.plot(data_noise[0],color='b',lw=1,alpha=0.2)
plt.plot(outdata[0],color='cornflowerblue',lw=3)
plt.plot(data[0],color='orange',lw=1,alpha=0.5)

plt.subplot(512)
plt.plot(data_noise[1],color='b',lw=1,alpha=0.2)
plt.plot(outdata[1],color='cornflowerblue',lw=3)
plt.plot(data[1],color='orange',lw=1,alpha=0.5)

plt.subplot(513)
plt.plot(data_noise[2],color='b',lw=1,alpha=0.2)
plt.plot(outdata[2],color='cornflowerblue',lw=3)
plt.plot(data[2],color='orange',lw=1,alpha=0.5)

plt.subplot(514)
plt.plot(data_noise[3],color='b',lw=1,alpha=0.2)
plt.plot(outdata[3],color='cornflowerblue',lw=3)
plt.plot(data[3],color='orange',lw=1,alpha=0.5)

import scipy.signal as signal
b, a = signal.iirdesign([0.01, 0.15], [0.005, 0.17], 2, 40)
out = signal.lfilter(b, a, data_noise[3])

plt.subplot(515)
plt.plot(data_noise[3],color='b',lw=1,alpha=0.2)
plt.plot(out,color='cornflowerblue',lw=3)
plt.plot(data[3],color='orange',lw=1,alpha=0.5)

plt.figure(2)
plt.plot(np.transpose(cvl1))

plt.show()

for itry in range(3):
    outfile_no=open("no_data"+str(itry)+".txt","w")
    outfile_rw=open("rw_data"+str(itry)+".txt","w")
    outfile_fl=open("fl_data"+str(itry)+".txt","w")
    #outz=SacStreamIO("no_data"+str(itry)+".z","wb")
    #outz.WriteHead(784)
    for itrx in range(N):
        outfile_no.write(str(data_noise[itry][itrx])+"\n")
        outfile_rw.write(str(data[itry][itrx])+"\n")
        outfile_fl.write(str(outdata[itry][itrx])+"\n")
        #outz.WriteData(data_noise)
    #outz.CleanFile()
        

















