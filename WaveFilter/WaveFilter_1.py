# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 18:34:36 2017

@author: LLL
"""
import os
import numpy as np
from scipy import special
import tensorflow as tf

class WaveFilterTrain():
    def __init__(self):
        self.sess=tf.Session()
        self.data_n=784
        self.data_y_len=10
        self.data_chenel_n=1

        self.conv1_stri=4
        self.conv1_shape=[32,self.data_chenel_n,64]
        self.pool1_shape=0
        self.conv2_stri=3
        self.conv2_shape=[16,64,128]
        self.conv3_stri=2
        self.conv3_shape=[4,128,128]
        self.conv4_stri=1
        self.conv4_shape=[4,128,128]
        self.conv5_stri=1
        self.conv5_shape=[4,128,32]
        divd=self.conv1_stri*self.conv2_stri*self.conv3_stri*self.conv4_stri*self.conv5_stri
        self.full1_shape=[int(self.data_n/divd+1)*self.conv5_shape[2],self.data_n]
        
        #self.full1_shape=[9*self.conv5_shape[2],self.data_n]
        
        self.conv6_stri=2
        self.conv6_shape=[4,256,128]
        self.conv7_stri=1
        self.conv7_shape=[4,128,128]
        self.conv7_stri=1
        self.conv7_shape=[4,128,64]
        self.conv8_stri=2
        self.conv8_shape=[4,64,self.data_chenel_n]

        
    def init_var(self):
        self.x=tf.placeholder(tf.float32,shape=[None,self.data_n,self.data_chenel_n])
        self.y=tf.placeholder(tf.float32,shape=[None,self.data_n])
        x_3d=tf.reshape(self.x,[-1,self.data_n,self.data_chenel_n])
        
        x_w1=self.my_weigh(self.conv1_shape)
        x_b1=self.my_bias([self.conv1_shape[2]])
        x_wb1=self.my_conv_1d_down(x_3d ,x_w1,self.conv1_stri)+x_b1
        x_fn1=self.nn_fn(x_wb1)
        
        x_w2=self.my_weigh(self.conv2_shape)
        x_b2=self.my_bias([self.conv2_shape[2]])
        x_wb2=self.my_conv_1d_down(x_fn1,x_w2,self.conv2_stri)+x_b2
        x_fn2=self.nn_fn(x_wb2)
        
        x_w3=self.my_weigh(self.conv3_shape)
        x_b3=self.my_bias([self.conv3_shape[2]])
        x_wb3=self.my_conv_1d_down(x_fn2,x_w3,self.conv3_stri)+x_b3
        x_fn3=self.nn_fn(x_wb3)
        
        x_w4=self.my_weigh(self.conv4_shape)
        x_b4=self.my_bias([self.conv4_shape[2]])
        x_wb4=self.my_conv_1d_down(x_fn3,x_w4,self.conv4_stri)+x_b4
        x_fn4=self.nn_fn(x_wb4)

        x_w5=self.my_weigh(self.conv5_shape)
        x_b5=self.my_bias([self.conv5_shape[2]])
        x_wb5=self.my_conv_1d_down(x_fn4,x_w5,self.conv5_stri)+x_b5
        x_fn5=self.nn_fn(x_wb5)

        x_w6=self.my_weigh([self.full1_shape[0],self.data_n])
        x_b6=self.my_bias([self.data_n])
        x_fn5_rs=tf.reshape(x_fn5,[-1,self.full1_shape[0]])
        x_wb6=tf.matmul(x_fn5_rs,x_w6)+x_b6
        x_fn6=self.nn_fn(x_wb6)
                
        
        self.kp_prb=tf.placeholder('float')
        self.x_drop=tf.nn.dropout(x_fn6,self.kp_prb)
        
        #cross_entropy=tf.reduce_sum(tf.reshape(self.x,[-1,self.data_n])*tf.reshape(x_drop,[-1,self.data_n]))
        #cross_entropy=-tf.reduce_sum(tf.reshape(x_drop,[-1,self.full1_shape[1]])*self.y)
        cross_entropy=tf.reduce_sum(tf.abs(tf.reshape(self.x_drop,[-1,self.full1_shape[1]])-self.y))
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
        #self.train_step=tf.train.GradientDescentOptimizer()
        self.sess.run(tf.global_variables_initializer())
        self.acc=tf.reduce_sum(tf.abs(tf.reshape(self.x_drop,[-1,self.full1_shape[1]])-self.y))
        #print(self.sess.run(tf.shape(x_fn5),feed_dict={self.x: data[0], self.y: data[1], self.kp_prb:0.5}))
        #print(fc1_len)
        #print(np.shape(self.sess.run(result,feed_dict={self.x: np.zeros([10,784]),self.y: np.zeros([10,10]), self.kp_prb: 0.5})))
    def my_conv_1d_down(self,data,flt,stri):
        return tf.nn.conv1d(data,filters=flt,stride=stri, padding='SAME')
    def my_conv_1d_up(self,data,flt,stri):
        sp=tf.shape(data)
        data_2d=tf.reshape(data,[sp[0],1,sp[1],sp[2]],name="test")
        data_2d_n=tf.Variable(tf.image.resize_images(data_2d,[1,sp[1]*stri],method=tf.image.ResizeMethod.AREA),[sp[0],1,sp[1]*stri,sp[2]])
        data_rs=tf.reshape(data_2d_n,[sp[0],sp[1]*stri,sp[2]])
        return tf.nn.conv1d(data_rs,filters=flt,stride=1,padding='SAME')
    def my_bias(self,shape):
        init=tf.constant(0.1,shape=shape)
        return tf.Variable(init)
    def my_weigh(self,shape):
        init=tf.truncated_normal(shape,stddev=0.1)
        return tf.Variable(init)
    def nn_fn(self,x):
        return tf.nn.relu(x)
    def my_max_pool_1d(self,data):
        return tf.nn.pool(data,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')
    
    def train(self,data):
        return self.sess.run(self.train_step,feed_dict={self.x: data[0], self.y: data[1], self.kp_prb:0.5})

    def validate(self,data):
        return self.sess.run(self.acc,feed_dict={self.x: data[0], self.y: data[1], self.kp_prb:1})
    def validate_fig(self,data):
        import matplotlib.pyplot as plt
        dt=self.sess.run(self.x_drop,feed_dict={self.x: data[0], self.y: data[1], self.kp_prb:1})
        plt.plot(dt[0])
        plt.plot(data[1][0])
        plt.show()
        
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
        sbn=np.random.randint(10)+1
        #data=np.random.random(shape)
        #data=np.subtract(data,0.5)
        for itrd in range(self.shape[0]):
            for itr in range(sbn):
                f0=1+np.random.random(1)[0]*10
                Tc=1/(np.random.randint(5)+1)
                per=100
                t=np.linspace(0,1,per)
                wave=(1+np.cos(2.*np.pi*(t-Tc/2.)/Tc))*np.cos(2.*np.pi*f0*(t-Tc/2.))/2.
                nba=np.random.randint(self.shape[1]-per-1)
                self.data[itrd,nba:nba+per]=self.data[itrd,nba:nba+per]+wave
        mx=np.max(self.data,axis=1)
        mx=np.reshape(mx,[-1,1])
        self.data=np.divide(self.data,mx)
        return self.data
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

    aa=WaveFilterTrain()
    aa.init_var()
    for i in range(1):
        #plt.clf()
        #plt.imshow(np.reshape(batch[0][5],[28,28]),cmap=plt.get_cmap('Blues'))
        data=batch.GenWave()
        data_noise=batch.AddNoise(0.5)
        plt.plot(data[0])
        #plt.plot(data_noise[0])
        aa.train([np.reshape(data_noise,[-1,784,1]),data])
        if(i%9==0):
            print("iter %4d:%6.1f"%(i,aa.validate([np.reshape(data_noise,[-1,784,1]),data])))
    data=batch.GenWave()
    data_noise=batch.AddNoise(0.1)
    #aa.validate_fig([np.reshape(data_noise,[-1,784,1]),data])
  
            
    #aa.restore(109)
    #print("restore test")
    #print(aa.validate([mnist.test.images,mnist.test.labels]))


#con_x_1d=tf.nn.conv1d(x1d,filters=x1d_cov,stride=1, padding='SAME')