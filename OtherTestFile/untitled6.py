# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:03:47 2017

@author: LLL
"""

import os
import numpy as np
from scipy import special
import tensorflow as tf


from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

x = tf.placeholder(tf.float32,[None,4,1])
zeo=np.zeros([4,8])
for itr in range(len(zeo)):
    zeo[itr,itr*2:itr*2+2]=[1,1]
ons=tf.constant(zeo,dtype=tf.float32)
xbp=tf.matrix_band_part(ons,1,1)
#out=tf.sparse_matmul(spm,spm,a_is_sparse=True,b_is_sparse=True)


xx=tf.reshape(x,[-1,1,4,1])
w=tf.constant(1.0,shape=[4,4,1])
dla=tf.nn.dilation2d(xx,filter=w,strides=[1,1,1,1],rates=[1,4,4,1],padding='SAME')
#aa=tf.nn.conv1d(xx,filters=w,stride=1, padding='SAME')

xxx=tf.reshape(x,[-1,1,4])

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()



for _ in range(1):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  print(sess.run(xx,feed_dict={x:  [[[x] for x in range(4)],[[x] for x in range(4)]]}))
  print("===============fengexian=========================")
  print(sess.run(dla,feed_dict={x:  [[[x] for x in range(4)],[[x] for x in range(4)]]}))
  #print(sess.run((x_rs), feed_dict={x:  [[[x,x] for x in range(4)],[[x+4,x+4] for x in range(4)]]}))
  #print(sess.run((x_ri), feed_dict={x:  [[[x,x] for x in range(4)],[[x+4,x+4] for x in range(4)]]}))
  #print(sess.run((x_sri), feed_dict={x:  [[[x,x] for x in range(4)],[[x+4,x+4] for x in range(4)]]}))
