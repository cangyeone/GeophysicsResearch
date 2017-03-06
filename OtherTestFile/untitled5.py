# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 18:27:41 2017

@author: LLL
"""

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


import tensorflow as tf
x = tf.placeholder(tf.float32, [None, 784])

W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))

y = tf.nn.softmax(tf.matmul(x, W) + b)

y_ = tf.placeholder(tf.float32, [None, 10])


tfcst=tf.Variable([[0],[0.1],[0.2],[0.3],[0.4],[0.5],[0.6],[0.7],[0.8],[0.9]],trainable=False)
fl=tf.matmul(y_,tfcst)
tfvst=tf.Variable([[0],[0.1],[0.2],[0.3],[0.4],[0.5],[0.6],[0.7],[0.8],[0.9]])

cross_entropy = tf.reduce_sum(tf.abs(tf.matmul(y,tfcst)-fl))
train_step = tf.train.AdamOptimizer(0.01).minimize(cross_entropy)
sess = tf.InteractiveSession()

correct_prediction = tf.reduce_mean(tf.abs(tf.matmul(y,tfcst)-fl))
tf.global_variables_initializer().run()




for itr in range(10000):
  batch_xs, batch_ys = mnist.train.next_batch(50)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
  if(itr%9==0):

      print(sess.run(correct_prediction, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

  

accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


