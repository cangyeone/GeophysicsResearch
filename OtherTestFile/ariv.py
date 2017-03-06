# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 18:34:36 2017

@author: LLL
"""
import os
import numpy as np
from scipy import special
import tensorflow as tf

class WaveIdentifyTrain():
    def __init__(self):
        self.sess=tf.Session()
        self.data_patch_len=784
        self.data_y_len=1
        self.data_chenel_n=1
        self.w1_shape=[784,784]
        self.w2_shape=[784,784]
        self.conv1_shape=[4,self.data_chenel_n,8]
        self.conv2_shape=[4,8,16]

    def init_var(self):
        self.x=tf.placeholder(tf.float32,shape=[None,self.data_patch_len,self.data_chenel_n])
        self.y=tf.placeholder(tf.float32,shape=[None,self.data_y_len])
        x_3d=tf.reshape(self.x,[-1,self.data_patch_len,self.data_chenel_n])
        
        x_w1=self.my_weigh(self.conv1_shape)
        x_b1=self.my_bias([self.conv1_shape[2]])
        x_wb1=self.my_conv_1d(x_3d,x_w1)+x_b1
        x_sigm1=tf.nn.relu(x_wb1)
        x_pool1=self.my_max_pool_1d(x_sigm1)
        
        x_w2=self.my_weigh(self.conv2_shape)
        x_b2=self.my_bias([self.conv2_shape[2]])
        x_wb2=self.my_conv_1d(x_pool1,x_w2)+x_b2
        x_sigm2=tf.nn.relu(x_wb2)
        x_pool2=self.my_max_pool_1d(x_sigm2)
        
        fc1_len=int(self.data_patch_len/1/1)
        x_fc1=self.my_weigh([fc1_len*self.conv2_shape[2],128])
        b_fc1=self.my_bias([128])
        xb_fc1=tf.matmul(tf.reshape(x_pool2,[-1,fc1_len*self.conv2_shape[2]]),x_fc1)+b_fc1
        x_fc_sigma1=tf.nn.relu(xb_fc1)
        
        self.kp_prb=tf.placeholder('float')
        x_drop=tf.nn.dropout(x_fc_sigma1,self.kp_prb)
        
        fc_w1=self.my_weigh([128,self.data_y_len])
        fc_b1=self.my_bias([self.data_y_len])
        result=tf.matmul(x_drop,fc_w1)+fc_b1

        
        self.cross_entropy=tf.reduce_mean((self.y-result)*(self.y-result))
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(self.cross_entropy)
        #self.train_step=tf.train.GradientDescentOptimizer()
        self.sess.run(tf.global_variables_initializer())

    def my_conv_1d(self,data,flt):
        return tf.nn.conv1d(data,filters=flt,stride=1, padding='SAME')
    def my_bias(self,shape):
        init=tf.constant(0.1,shape=shape)
        return tf.Variable(init)
    def my_weigh(self,shape):
        init=tf.truncated_normal(shape,stddev=0.1)
        return tf.Variable(init)
    def my_max_pool_1d(self,data):
        return tf.nn.pool(data,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')
    def validate(self,data):
        return self.sess.run(self.cross_entropy,feed_dict={self.x: data[0], self.y: data[1], self.kp_prb:0.5})
    def train(self,data):
        return self.sess.run(self.train_step,feed_dict={self.x: data[0], self.y: data[1], self.kp_prb:0.5})
  
    def saver(self,step):
        self.sv=tf.train.Saver()
        try:
            self.sv.save(self.sess,'var_back/model',global_step=step)
        except:
            os.mkdir('var_back')
            self.sv.save(self.sess,'var_back/model',global_step=step)
    def restore(self,step=-1):
        if(step>0):
            self.sv.restore(self.sess,'var_back/model-'+str(step))
        else:
            self.sv.recover_last_checkpoints('var_back/')
        
class GenData():
    def __init__(self,shape):
        self.shape=shape
        self.data=np.zeros(self.shape)
    def GenWave(self):
        sbn=1
        #data=np.random.random(shape)
        #data=np.subtract(data,0.5)
        ariv=np.zeros([self.shape[0],1])
        for itrd in range(self.shape[0]):
            for itr in range(sbn):
                f0=1
                Tc=1
                per=100
                t=np.linspace(0,1,per)
                wave=(1+np.cos(2.*np.pi*(t-Tc/2.)/Tc))*np.cos(2.*np.pi*f0*(t-Tc/2.))/2.
                nba=np.random.randint(self.shape[1]-per-1)
                ariv[itrd][0]=nba
                self.data[itrd,nba:nba+per]=self.data[itrd,nba:nba+per]+wave
        mx=np.max(self.data,axis=1)
        mx=np.reshape(mx,[-1,1])
        self.data=np.divide(self.data,mx)
        return nba
    def AddNoise(self,bl=0.5):
        noise=np.random.random(self.shape)
        noise=np.subtract(noise,0.5)
        noise=np.multiply(noise,bl)
        return np.add(self.data,noise)
if __name__ == '__main__':
    print("Do not run this file directily!")
    print("Try to run simple file:")
    from tensorflow.examples.tutorials.mnist import input_data
    import matplotlib.pyplot as plt
    
    batch = GenData([50,784])

    aa=WaveIdentifyTrain()
    aa.init_var()
    for i in range(10000):
        data=batch.GenWave()
        data_noise=batch.AddNoise(0.3)
        aa.train([np.reshape(data_noise,[-1,784,1]),np.reshape(data,[-1,1])])
        if(i%99==1):
            print(aa.validate([np.reshape(data_noise,[-1,784,1]),np.reshape(data,[-1,1])]))

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        