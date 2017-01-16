# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 09:16:54 2017

@author: Cangye
"""

import numpy as np
from scipy import special
import tensorflow as tf
#from scipy import integrate
ctype='complex64'
class WaveNumber():
    def __init__(self):
        print("start:")
        sess = tf.Session()
        self.GetPar()
        self.omega=tf.placeholder(tf.complex64, [None,1], name='omega')
        self.k=tf.placeholder(tf.complex64, [None,1], name='k')
        self.GetParV()
        
        
        init=tf.global_variables_initializer()
        sess.run(init)
        print(sess.run(self.kk,feed_dict={self.omega:[[1]],self.k:[[1],[2],[3],[4],[5]]}))
    def GetPar(self):
        par_t=[]
        for ii in range(10):
            #1000m=1km=0.001
            par_t.append([1,1,1,1])
        self.par=tf.Variable(par_t,dtype='complex64')
    def GetParV(self):
        a=self.par
        self.aa=tf.sqrt(tf.divide(a[:,0]+2*a[:,1],a[:,2]))
        self.bb=tf.sqrt(a[:,1]/a[:,2])
        self.rr=tf.sqrt(self.k*self.k-self.omega*self.omega/self.aa/self.aa)
        self.vv=tf.sqrt(self.k*self.k-self.omega*self.omega/self.bb/self.bb)
        #self.kk=tf.Variable([self.aa.values()[0,0],0],[0,0]],dtype='complex64')
        #self.kkk=tf.multiply(self.kk,self.k[0,0])
        self.kk=tf.Variable([[1,1],[1,1]],dtype='complex64')
        self.mm=[]
        for itr in range(10):
            self.mm.append(tf.Variable([[1,1],[1,1]],dtype='complex64'))
        for itr in range(10):
            self.kk=self.kk+self.mm[itr]
            #self.mat=tf.multiply(self.aa,self.kk)
        
        
        
aa=WaveNumber()

