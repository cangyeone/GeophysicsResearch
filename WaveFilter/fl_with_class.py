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
from pysac import SacStreamIO
N=256
TN=2000
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
                f0=50+np.random.random(1)[0]*50

                per=100
                t=np.linspace(0,1,per)
                wave=np.sin(f0*t)
                nba=np.random.randint(self.shape[1]-per-1)
                ariv[itrd][0]=1
                self.data[itrd,nba:nba+per]=self.data[itrd,nba:nba+per]+wave
        mx=np.max(self.data,axis=1)
        mx=np.reshape(mx,[-1,1])
        self.data=np.multiply(np.divide(self.data,mx),0.0)
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
        c1s=[16,1,8]
        c2s=[4,8,16]
        c3s=[4,16,1]
        
        pool_type='MAX'
        pool_window=[4,2,2]
        pool_stride=[4,2,1]
        
        x = tf.placeholder(tf.float32,[50,N])
        y = tf.placeholder(tf.float32,[50,int(N/pool_stride[0]/pool_stride[1]/pool_stride[2])])
        

        kp_prb=tf.placeholder('float')
        data1=tf.reshape(x,[50,N,1])
        self.c1_w=self.my_weigh(c1s)
        c1_b=self.my_weigh([c1s[2]])
        c1_f1=tf.nn.conv1d(data1,filters=self.c1_w,stride=1, padding='SAME')+c1_b
        c1_f2=tf.nn.tanh(c1_f1)
        c1=tf.nn.pool(c1_f2,window_shape=[pool_window[0]],pooling_type=pool_type,strides=[pool_stride[0]],padding='SAME')
        
        c2_w=self.my_weigh(c2s)
        c2_b=self.my_weigh([c2s[2]])
        c2_f1=tf.nn.conv1d(c1,filters=c2_w,stride=1, padding='SAME')+c2_b
        c2_f2=tf.nn.tanh(c2_f1)
        c2_f2=tf.nn.dropout(c2_f2,kp_prb)
        c2=tf.nn.pool(c2_f2,window_shape=[pool_window[1]],pooling_type=pool_type,strides=[pool_stride[1]],padding='SAME')
        
        c3_w=self.my_weigh(c3s)
        c3_b=self.my_weigh([c3s[2]])
        c3_f1=tf.nn.conv1d(c2,filters=c3_w,stride=1, padding='SAME')+c3_b
        c3_f2=tf.nn.tanh(c3_f1)
        c3=tf.nn.pool(c3_f2,window_shape=[pool_window[2]],pooling_type=pool_type,strides=[pool_stride[2]],padding='SAME')
        
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
        
        
        
        data2=tf.reshape(c3,[50,int(N/pool_stride[0]/pool_stride[1]/pool_stride[2])])
        
        ce = tf.reduce_mean(tf.abs(data2-y))
        
        train_step = tf.train.AdamOptimizer(1e-3).minimize(ce)
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
                data_noise=func.AddNoise(0.1,tp='RD')
            self.sess.run(train_step, feed_dict={x: data_noise, y: sig.resample(data,int(N/pool_stride[0]/pool_stride[1]/pool_stride[2]),axis=1),kp_prb:0.8})
            #print(data[0])
            #plt.plot(data_noise[0])
            if(itr%100==0):
                print("%d:%f"%(itr,self.sess.run(ce, feed_dict={x: data_noise, y:sig.resample(data,int(N/pool_stride[0]/pool_stride[1]/pool_stride[2],),axis=1),kp_prb:1.})))
        #conv_layer=sess.run(c1_w, feed_dict={x: data_noise, y: data,kp_prb:0.1})
        
        
        #============================================================================
        kp_t=tf.placeholder('float')
        sp=np.shape(raw_data)
        x_t = tf.placeholder(tf.float32,sp)
        data_t=tf.reshape(x_t,[sp[0],sp[1],1])
        
        c1_f1_t=tf.nn.conv1d(data_t,filters=self.c1_w,stride=1, padding='SAME')+c1_b
        c1_f2_t=tf.nn.tanh(c1_f1_t)
        c1_t=tf.nn.pool(c1_f2_t,window_shape=[pool_window[0]],pooling_type=pool_type,strides=[pool_stride[0]],padding='SAME')
        
        c2_f1_t=tf.nn.conv1d(c1_t,filters=c2_w,stride=1, padding='SAME')+c2_b
        c2_f2_t=tf.nn.tanh(c2_f1_t)
        c2_f2_t=tf.nn.dropout(c2_f2_t,kp_t)
        c2_t=tf.nn.pool(c2_f2_t,window_shape=[pool_window[1]],pooling_type=pool_type,strides=[pool_stride[1]],padding='SAME')
        
        c3_f1_t=tf.nn.conv1d(c2_t,filters=c3_w,stride=1, padding='SAME')+c3_b
        c3_f2_t=tf.nn.tanh(c3_f1_t)
        c3_f2_t=tf.nn.dropout(c3_f2_t,kp_t)
        c3_t=tf.nn.pool(c3_f2_t,window_shape=[pool_window[2]],pooling_type=pool_type,strides=[pool_stride[2]],padding='SAME')
        
        
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
        data2_t=tf.reshape(c3_t,[sp[0],-1])
        
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
        
batch2 = GenDataErr([50,TN])
data,nzdata=batch2.GenWave(5)
data_noise=batch2.AddNoise(0.1)



bb=GenData()
flt2=FilterTrain(bb,nzdata)
outdata=flt2.outdata

"""
aa=SacStreamIO('st02_cut.z','rb')

aa.DataDetrend()
dt=aa.yVect
dt1=0;np.random.random(np.shape(dt))*0.1
dt=np.divide(np.reshape(dt,[-1,np.shape(dt)[0]]),np.max(dt)*5)
dts=dt+dt1
flt3=FilterTrain(bb,dts)
dtflt=flt3.outdata

print(dtflt)
cvl1=(np.transpose(np.reshape(flt2.sess.run(flt2.c1_w.value()),[4,8])))
plt.figure(1)
plt.subplot(511)
plt.plot(dts[0],color='b',lw=1,alpha=0.2)
plt.plot(sig.resample(dtflt[0],np.shape(dt)[1]),color='cornflowerblue',lw=3)
plt.plot(dt[0],color='orange',lw=1,alpha=0.5)
"""
plt.subplot(411)
plt.plot(nzdata[1],color='b',lw=1,alpha=0.2)
plt.plot(sig.resample(outdata[1],TN),color='cornflowerblue',lw=3)
plt.plot(data[1],color='orange',lw=1,alpha=0.5)

plt.subplot(412)
plt.plot(nzdata[2],color='b',lw=1,alpha=0.2)
plt.plot(sig.resample(outdata[2],TN),color='cornflowerblue',lw=3)
plt.plot(data[2],color='orange',lw=1,alpha=0.5)

plt.subplot(413)
plt.plot(nzdata[3],color='b',lw=1,alpha=0.2)
plt.plot(sig.resample(outdata[3],TN),color='cornflowerblue',lw=3)
plt.plot(data[3],color='orange',lw=1,alpha=0.5)

import scipy.signal as signal
b, a = signal.iirdesign([0.01, 0.15], [0.005, 0.17], 2, 40)
out = signal.lfilter(b, a, data_noise[3])

plt.subplot(414)
plt.plot(data_noise[3],color='b',lw=1,alpha=0.2)
plt.plot(sig.resample(out,TN),color='cornflowerblue',lw=3)
plt.plot(data[3],color='orange',lw=1,alpha=0.5)
"""
plt.figure(2)
plt.plot(np.transpose(cvl1))
"""
plt.show()
"""
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
"""     

















