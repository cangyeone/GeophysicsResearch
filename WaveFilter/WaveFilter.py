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

        self.conv1_stri=2
        self.conv1_shape=[16,self.data_chenel_n,64]
        self.conv2_stri=1
        self.conv2_shape=[4,64,128]
        self.conv3_stri=1
        self.conv3_shape=[4,128,128]
        self.conv4_stri=2
        self.conv4_shape=[4,128,256]
        self.conv5_stri=1
        self.conv5_shape=[4,256,256]
        self.conv6_stri=2
        self.conv6_shape=[4,256,128]
        self.conv7_stri=1
        self.conv7_shape=[4,128,128]
        self.conv7_stri=1
        self.conv7_shape=[4,128,64]
        self.conv8_stri=2
        self.conv8_shape=[4,64,self.data_chenel_n]

        
    def init_var(self,data):
        self.x=tf.placeholder(tf.float32,shape=[None,self.data_n,self.data_chenel_n])
        self.y=tf.placeholder(tf.float32,shape=[None,self.data_y_len])
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

        x_w6=self.my_weigh(self.conv6_shape)
        x_b6=self.my_bias([self.conv6_shape[2]])
        x_wb6=self.my_conv_1d_up(x_fn5,x_w6,self.conv6_stri)+x_b6
        x_fn6=self.nn_fn(x_wb6)
                
        x_w7=self.my_weigh(self.conv7_shape)
        x_b7=self.my_bias([self.conv7_shape[2]])
        x_wb7=self.my_conv_1d_up(x_fn6,x_w7,self.conv7_stri)+x_b7
        x_fn7=self.nn_fn(x_wb7)
                
        x_w8=self.my_weigh(self.conv8_shape)
        x_b8=self.my_bias([self.conv8_shape[2]])
        x_wb8=self.my_conv_1d_up(x_fn7,x_w8,self.conv8_stri)+x_b8
        x_fn8=self.nn_fn(x_wb8)
        
        self.kp_prb=tf.placeholder('float')
        x_drop=tf.nn.dropout(x_fn8,self.kp_prb)
        
        #cross_entropy=tf.reduce_sum(tf.reshape(self.x,[-1,self.data_n])*tf.reshape(x_drop,[-1,self.data_n]))
        cross_entropy=tf.reduce_sum(tf.reshape(x_drop,[-1,self.data_n]))
        self.train_step =tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
        #self.train_step=tf.train.GradientDescentOptimizer()
        self.sess.run(tf.global_variables_initializer())
        print(self.sess.run(tf.shape(tf.reshape(self.x,[-1,self.data_n])*tf.reshape(x_drop,[-1,self.data_n])),feed_dict={self.x: data[0], self.y: data[1], self.kp_prb:0.5}))
        #print(fc1_len)
        #print(np.shape(self.sess.run(result,feed_dict={self.x: np.zeros([10,784]),self.y: np.zeros([10,10]), self.kp_prb: 0.5})))
    def my_conv_1d_down(self,data,flt,stri):
        return tf.nn.conv1d(data,filters=flt,stride=stri, padding='SAME')
    def my_conv_1d_up(self,data,flt,stri):
        sp=tf.shape(data)
        data_2d=tf.reshape(data,[sp[0],1,sp[1],sp[2]])
        data_2d_n=tf.image.resize_images(data_2d,[1,sp[1]*stri],method=tf.image.ResizeMethod.AREA)
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
        print(self.sess.run(self.train_step,feed_dict={self.x: data[0], self.y: data[1], self.kp_prb:0.5}))
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
        
        
if __name__ == '__main__':
    print("Do not run this file directily!")
    print("Try to run simple file:")
    from tensorflow.examples.tutorials.mnist import input_data
    mnist = input_data.read_data_sets('MNIST_data', one_hot=True)
    batch = mnist.train.next_batch(50)
        #plt.clf()
        #plt.imshow(np.reshape(batch[0][5],[28,28]),cmap=plt.get_cmap('Blues'))
    trans=np.reshape(batch[0],[-1,784,1])
    aa=WaveFilterTrain()
    aa.init_var([trans,batch[1]])

  
            
    #aa.restore(109)
    #print("restore test")
    #print(aa.validate([mnist.test.images,mnist.test.labels]))


#con_x_1d=tf.nn.conv1d(x1d,filters=x1d_cov,stride=1, padding='SAME')