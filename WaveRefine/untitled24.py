# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 17:21:27 2017

@author: LLL
"""

import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
import tensorflow as tf
import scipy.signal as sig
import os
#from pysac import SacStreamIO
N=2048
TN=2048
class GenData():
    def __init__(self,shape=[1,1]):
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
                f0=1+np.random.random(1)[0]*0.5
                Tc=1/(np.random.randint(5)+1)
                per=2000
                t=np.linspace(0,1,per)
                wave=(1+np.cos(2.*np.pi*(t-Tc/2.)/Tc))*np.cos(2.*np.pi*f0*(t-Tc/2.))/2.
                nba=np.random.randint(self.shape[1]-per-1)
                ariv[itrd][0]=1
                self.data[itrd,nba:nba+per]=self.data[itrd,nba:nba+per]+wave
        mx=np.max(self.data,axis=1)
        mx=np.reshape(mx,[-1,1])
        self.data=np.multiply(np.divide(self.data,mx),0.2)
        #return ariv
        #self.data=self.data+np.random.random(1)[0]*0.5-0.25
        return self.data
    def AddNoise(self,bl=0.5,tp='FX'):
        noise=np.random.random(self.shape)
        noise=np.subtract(noise,0.5)
        if(tp=='RD'):
            bl=np.random.random(1)[0]*bl+0.0001
        noise=np.multiply(noise,bl)
        return np.add(self.data,noise)
        
class GenDataSin():
    def __init__(self,shape=[1,1]):
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
                f0=np.random.random(1)[0]*10
                per=100
                t=np.linspace(0,1,per)
                wave=np.sin(f0*t)
                nba=np.random.randint(self.shape[1]-per-1)
                ariv[itrd][0]=1
                self.data[itrd,nba:nba+per]=self.data[itrd,nba:nba+per]+wave
        mx=np.max(self.data,axis=1)
        mx=np.reshape(mx,[-1,1])
        self.data=np.multiply(np.divide(self.data,mx),0.4)
        self.data=self.data+np.random.random(1)[0]*0.3-0.15
        #self.ndata=np.multiply(np.divide(self.data,mx),0.0)
        #return ariv
        
        return self.data
    def AddNoise(self,bl=0.5,tp='FX'):
        noise=np.random.random(self.shape)
        noise=np.subtract(noise,0.5)
        if(tp=='RD'):
            bl=np.random.random(1)[0]*bl+0.0001
        noise=np.multiply(noise,bl)
        return np.add(self.data,noise)

class GenDataLin():
    def __init__(self,shape=[1,1]):
        self.shape=shape
        self.data=np.zeros(self.shape)
    def GenWave(self,numSubWave=30):
        
        #data=np.random.random(shape)
        #data=np.subtract(data,0.5)
        if(numSubWave==0):
            return self.data
        
        for itrd in range(self.shape[0]):
            rds=0.2*np.random.random(1)[0]
            rsf=np.random.randint(4)-2
            self.data[itrd,:]=np.multiply(np.subtract(np.linspace(0,rds,self.shape[1]),rds/2),rsf)
        #return ariv
        
        return self.data
    def AddNoise(self,bl=0.5,tp='FX'):
        noise=np.random.random(self.shape)
        noise=np.subtract(noise,0.5)
        if(tp=='RD'):
            bl=np.random.random(1)[0]*bl+0.0001
        noise=np.multiply(noise,bl)
        return np.add(self.data,noise)
def MovAvg(interval, window_size):
    window = np.ones(int(window_size))/float(window_size)
    return np.convolve(interval, window, 'same')        
        
class FilterTrain():
    def my_weigh(self,shape):
        init=tf.truncated_normal(shape,stddev=0.1)
        return tf.Variable(init)
    def my_bias(self,shape):
        init=tf.constant(0.1,shape=shape)
        return tf.Variable(init)


    def __init__(self,func,raw_data):
        c1s=[32,1,8]
        c2s=[16,8,8]
        c3s=[8,8,8]
        c4s=[8,8,8]
        c5s=[8,8,4]
        c6s=[8,4,1]        
        pool_type='AVG'
        pool_window=[16,16,4 ,4 ,4 ,4 ]
        pool_stride=[16 ,4 ,2 ,1 ,1 ,1 ]
        ctm=1
        for itr in pool_stride:
            ctm=ctm*itr
        
        x = tf.placeholder(tf.float32,[50,N])
        y = tf.placeholder(tf.float32,[50,int(N/ctm)])
        

        kp_prb=tf.placeholder('float')
        data1=tf.reshape(x,[50,N,1])
        c1_w=self.my_weigh(c1s)
        c1_b=self.my_weigh([c1s[2]])
        c1_f1=tf.nn.conv1d(data1,filters=c1_w,stride=1, padding='SAME')+c1_b
        c1_f2=tf.nn.tanh(c1_f1)
        c1=tf.nn.pool(c1_f2,window_shape=[pool_window[0]],pooling_type=pool_type,strides=[pool_stride[0]],padding='SAME')
        
        c2_w=self.my_weigh(c2s)
        c2_b=self.my_weigh([c2s[2]])
        c2_f1=tf.nn.conv1d(c1,filters=c2_w,stride=1, padding='SAME')+c2_b
        c2_f2=tf.nn.tanh(c2_f1)
        c2=tf.nn.pool(c2_f2,window_shape=[pool_window[1]],pooling_type=pool_type,strides=[pool_stride[1]],padding='SAME')
        
        c3_w=self.my_weigh(c3s)
        c3_b=self.my_weigh([c3s[2]])
        c3_f1=tf.nn.conv1d(c2,filters=c3_w,stride=1, padding='SAME')+c3_b
        c3_f2=tf.nn.tanh(c3_f1)
        c3=tf.nn.pool(c3_f2,window_shape=[pool_window[2]],pooling_type=pool_type,strides=[pool_stride[2]],padding='SAME')
   
        c4_w=self.my_weigh(c4s)
        c4_b=self.my_weigh([c4s[2]])
        c4_f1=tf.nn.conv1d(c3,filters=c4_w,stride=1, padding='SAME')+c4_b
        c4_f2=tf.nn.tanh(c4_f1)
        c4=tf.nn.pool(c4_f2,window_shape=[pool_window[3]],pooling_type=pool_type,strides=[pool_stride[3]],padding='SAME')
        
        c5_w=self.my_weigh(c5s)
        c5_b=self.my_weigh([c5s[2]])
        c5_f1=tf.nn.conv1d(c4,filters=c5_w,stride=1, padding='SAME')+c5_b
        c5_f2=tf.nn.tanh(c5_f1)
        c5=tf.nn.pool(c5_f2,window_shape=[pool_window[4]],pooling_type=pool_type,strides=[pool_stride[4]],padding='SAME')
        
        c6_w=self.my_weigh(c6s)
        c6_b=self.my_weigh([c6s[2]])
        c6_f1=tf.nn.conv1d(c5,filters=c6_w,stride=1, padding='SAME')+c6_b
        c6_f2=tf.nn.tanh(c6_f1)
        c6=tf.nn.pool(c6_f2,window_shape=[pool_window[5]],pooling_type=pool_type,strides=[pool_stride[5]],padding='SAME')
        

        data2=tf.reshape(c6,[50,int(N/ctm)])
        
        ce = tf.reduce_mean(tf.abs(data2-y))
        
        train_step = tf.train.AdamOptimizer(1e-2).minimize(ce)
        #train_step = tf.train.GradientDescentOptimizer(0.5).minimize(c3)
        self.sess = tf.InteractiveSession()
        tf.global_variables_initializer().run()
        
        func.__init__([50,N])
        data=func.GenWave()
        data_noise=func.AddNoise(0.2)
        #print(sess.run(tf.shape(c2), feed_dict={x: data_noise, y: data,kp_prb:0.5}))
        
        for itr in range(1000):
            if(itr%2!=7):
                data=func.GenWave(3)
                data_noise=func.AddNoise(0.0)
            else:
                data=func.GenWave(0)
                data_noise=func.AddNoise(0.0,tp='RD')
            self.sess.run(train_step, feed_dict={x: data_noise, y: sig.resample(data,int(N/ctm),axis=1),kp_prb:0.8})
            #print(data[0])
            #plt.plot(data_noise[0])
            if(itr%100==0):
                print("%d:%f"%(itr,self.sess.run(ce, feed_dict={x: data_noise, y:sig.resample(data,int(N/ctm),axis=1),kp_prb:1.})))
        #conv_layer=sess.run(c1_w, feed_dict={x: data_noise, y: data,kp_prb:0.1})
        
        
        #============================================================================
        kp_t=tf.placeholder('float')
        sp=np.shape(raw_data)
        x_t = tf.placeholder(tf.float32,sp)
        data_t=tf.reshape(x_t,[sp[0],sp[1],1])
        
        c1_f1_t=tf.nn.conv1d(data_t,filters=c1_w,stride=1, padding='SAME')+c1_b
        c1_f2_t=tf.nn.tanh(c1_f1_t)
        c1_t=tf.nn.pool(c1_f2_t,window_shape=[pool_window[0]],pooling_type=pool_type,strides=[pool_stride[0]],padding='SAME')
        
        c2_f1_t=tf.nn.conv1d(c1_t,filters=c2_w,stride=1, padding='SAME')+c2_b
        c2_f2_t=tf.nn.tanh(c2_f1_t)
        #c2_f2_t=tf.nn.dropout(c2_f2_t,kp_t)
        c2_t=tf.nn.pool(c2_f2_t,window_shape=[pool_window[1]],pooling_type=pool_type,strides=[pool_stride[1]],padding='SAME')
        
        c3_f1_t=tf.nn.conv1d(c2_t,filters=c3_w,stride=1, padding='SAME')+c3_b
        c3_f2_t=tf.nn.tanh(c3_f1_t)
        #c3_f2_t=tf.nn.dropout(c3_f2_t,kp_t)
        c3_t=tf.nn.pool(c3_f2_t,window_shape=[pool_window[2]],pooling_type=pool_type,strides=[pool_stride[2]],padding='SAME')
        
        
        c4_f1_t=tf.nn.conv1d(c3_t,filters=c4_w,stride=1, padding='SAME')+c4_b
        c4_f2_t=tf.nn.tanh(c4_f1_t)
        #c4_f2_t=tf.nn.dropout(c3_f2_t,kp_t)
        c4_t=tf.nn.pool(c4_f2_t,window_shape=[pool_window[3]],pooling_type=pool_type,strides=[pool_stride[3]],padding='SAME')
        
        c5_f1_t=tf.nn.conv1d(c4_t,filters=c5_w,stride=1, padding='SAME')+c5_b
        c5_f2_t=tf.nn.tanh(c5_f1_t)
        #c5_f2_t=tf.nn.dropout(c3_f2_t,kp_t)
        c5_t=tf.nn.pool(c5_f2_t,window_shape=[pool_window[4]],pooling_type=pool_type,strides=[pool_stride[4]],padding='SAME')
        
        c6_f1_t=tf.nn.conv1d(c5_t,filters=c6_w,stride=1, padding='SAME')+c6_b
        c6_f2_t=tf.nn.tanh(c6_f1_t)
        #c6_f2_t=tf.nn.dropout(c3_f2_t,kp_t)
        c6_t=tf.nn.pool(c6_f2_t,window_shape=[pool_window[5]],pooling_type=pool_type,strides=[pool_stride[5]],padding='SAME')

        kp_prb=tf.placeholder('float')
        data2_t=tf.reshape(c6_t,[sp[0],-1])
        
        #===========================================================================
        self.outdata=self.sess.run(data2_t, feed_dict={x_t: raw_data,kp_prb:1,kp_t:1})

class GenDataErr():
    def __init__(self,shape=[1,1]):
        self.shape=shape
        self.data=np.zeros(self.shape)
        self.nzdata=np.zeros(self.shape)
    def GenWave(self,numSubWave=30):
        
        #data=np.random.random(shape)
        #data=np.subtract(data,0.5)
        ariv=np.zeros([self.shape[0],1])
        if(numSubWave==0):
            return self.data
        
        for itrd in range(self.shape[0]):
            sbn=1+np.random.randint(numSubWave)
            for itr in range(sbn):
                f0=1+np.random.random(1)[0]*0.5
                Tc=1/(np.random.randint(5)+1)
                per=100
                t=np.linspace(0,1,per)
                wave=(1+np.cos(2.*np.pi*(t-Tc/2.)/Tc))*np.cos(2.*np.pi*f0*(t-Tc/2.))/2.
                blk=np.random.randint(30)   
                vvae=np.array(wave[:])
                vvae[blk:blk+10]=np.zeros([10])
                #wave[blk:blk+30]=np.zeros([30])
                nba=np.random.randint(self.shape[1]-per-1)
                ariv[itrd][0]=1
                self.data[itrd,nba:nba+per]=self.data[itrd,nba:nba+per]+wave
                self.nzdata[itrd,nba:nba+per]=self.nzdata[itrd,nba:nba+per]+vvae
        mx=np.max(self.data,axis=1)
        mx=np.reshape(mx,[-1,1])
        self.data=np.multiply(np.divide(self.data,mx),0.2)
        #return ariv
        self.nzdata=np.multiply(np.divide(self.nzdata,mx),0.2)
        return self.data,self.nzdata
    def AddNoise(self,bl=0.5,tp='FX'):
        noise=np.random.random(self.shape)
        noise=np.subtract(noise,0.5)
        if(tp=='RD'):
            bl=np.random.random(1)[0]*bl+0.0001
        noise=np.multiply(noise,bl)
        return np.add(self.data,noise)        
        



#======================================
def GetSecFile(tag=".sec"):
    itrlist=os.walk(os.getcwd())
    sacFile=[]
    for itr in itrlist:
        for it in itr[2]:
            if(it[-4:]==tag):
                sacFile.append(itr[0]+"\\"+it)
    return sacFile

def GetFileData(file):
    dtFile=open(file,"r")
    dData=dtFile.readlines()
    dtL=0
    for itr in dData:
        dtL=dtL+1
        if(itr[0:4]=="DATE"):
            break
    rtData=[]
    for itr in dData[dtL:]:
        slt=[it for it in itr.split(' ') if(len(it)>0)][3:6]
        sltd=[float(it) for it in slt]
        rtData.append(sltd)
    dtFile.close()
    return np.transpose(np.array(rtData))
scFile=GetSecFile()
rtData=GetFileData(scFile[0])
rtData=np.abs(rtData/np.max(np.abs(rtData))*0.1)
from scipy.signal import detrend
rtData=detrend(rtData,axis=1)
rtData[0][40000:40060]=rtData[0][40000:40060]+np.ones([60])*0.3
rtData[1][40000:40060]=rtData[1][40000:40060]+np.ones([60])*0.3
rtData[2][40000:40060]=rtData[2][40000:40060]+np.ones([60])*0.3
#======================================


batch2 = GenData([50,TN])
data=batch2.GenWave(5)
#rtData=batch2.AddNoise(0.1)


bb=GenData([50,TN])
flt2=FilterTrain(bb,rtData)
outdata=flt2.outdata
print(np.shape(outdata))

import matplotlib as mpl
mpl.style.use('seaborn-darkgrid')
plt.subplot(311)
plt.plot(rtData[0],color='b',lw=1,alpha=0.2)
plt.plot(sig.resample(outdata[0],len(rtData[0])),color='cornflowerblue',lw=3)
#plt.plot(data[0],color='orange',lw=1,alpha=0.5)

plt.subplot(312)
plt.plot(rtData[1],color='b',lw=1,alpha=0.2)
plt.plot(sig.resample(outdata[1],len(rtData[0])),color='cornflowerblue',lw=3)
#plt.plot(data[1],color='orange',lw=1,alpha=0.5)

plt.subplot(313)
plt.plot(rtData[2],color='b',lw=1,alpha=0.2)
plt.plot(sig.resample(outdata[2],len(rtData[0])),color='cornflowerblue',lw=3)
#plt.plot(data[2],color='orange',lw=1,alpha=0.5)

plt.show()

















