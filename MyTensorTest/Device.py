# -*- coding: utf-8 -*-
"""
Created on Thu May 25 20:10:11 2017

@author: LLL
"""
import tensorflow as tf
# Creates a graph.
# Creates a graph.
lstm_size=5
lstm = tf.contrib.rnn.BasicLSTMCell(lstm_size)
# Creates a session with allow_soft_placement and log_device_placement set
# to True.
sess = tf.Session(config=tf.ConfigProto(
      allow_soft_placement=True, log_device_placement=True))
# Runs the op.
print(sess.run(c))