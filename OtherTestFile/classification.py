# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 11:56:37 2017

@author: Ziye Yu
"""


import os
import numpy as np
from scipy import special
import tensorflow as tf

class WaveIdentifyTrain():
    def __init__(self,m=24,n=28):
        #define m and n
       
        self.sess=tf.Session()
        self.data_class_attr=m*n
        #定义分类数量
        self.class_quantity=10
        #建立隐藏层
        self.hidden_layer_1=300
        self.hidden_layer_2=100
        self.hidden_layer_3=50


    def init_var(self):
        self.x=tf.placeholder(tf.float32,shape=[None,self.data_class_attr])

        x_w0=self.my_weigh([self.data_class_attr,self.hidden_layer_1])
        x_b0=self.my_bias([self.hidden_layer_1])
        x_wb0=tf.matmul(self.x,x_w0)+x_b0
        x_sigm0=tf.nn.relu(x_wb0)
        
        x_w1=self.my_weigh([self.hidden_layer_1,self.hidden_layer_2])
        x_b1=self.my_bias([self.hidden_layer_2])
        x_wb1=tf.matmul(x_sigm0,x_w1)+x_b1
        x_sigm1=tf.nn.relu(x_wb1)
        
        x_w2=self.my_weigh([self.hidden_layer_2,self.hidden_layer_3])
        x_b2=self.my_bias([self.hidden_layer_3])
        x_wb2=tf.matmul(x_sigm1,x_w2)+x_b2
        x_sigm2=tf.nn.relu(x_wb2)

        
        x_w3=self.my_weigh([self.hidden_layer_3,self.class_quantity])
        x_b3=self.my_bias([self.class_quantity])
        x_wb3=tf.matmul(x_sigm2,x_w3)+x_b3
        x_sigm3=tf.nn.relu(x_wb3)
        
        #去除其他不存在的情况
        self.kp_prb=tf.placeholder('float')
        result=tf.nn.dropout(x_sigm3,self.kp_prb)
        
        #定义损失函数
        cross_entropy=-tf.reduce_sum(result*tf.log(result))
        
        #训练过程
        self.train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
        #self.train_step=tf.train.GradientDescentOptimizer()
        self.sess.run(tf.global_variables_initializer())
        
        #print(fc1_len)
        #print(np.shape(self.sess.run(result,feed_dict={self.x: np.zeros([10,784]),self.y: np.zeros([10,10]), self.kp_prb: 0.5})))

    def my_bias(self,shape):
        init=tf.constant(0.1,shape=shape)
        return tf.Variable(init)
    def my_weigh(self,shape):
        init=tf.truncated_normal(shape,stddev=0.1)
        return tf.Variable(init)
    
    def train(self,data):
        return self.sess.run(self.train_step,feed_dict={self.x: data[0], self.kp_prb:0.5})

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
    aa=WaveIdentifyTrain()
    aa.init_var()
    import matplotlib.pyplot as plt
    for i in range(5000):
        batch = mnist.train.next_batch(50)

        trans=np.reshape(batch[0],[-1,784])
        aa.train([trans,batch[1]])
        
