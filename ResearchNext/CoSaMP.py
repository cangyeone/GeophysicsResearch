#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Oct. 7, 2014. Code based on Deanna Needell and Joel Tropp CoSaMP paper

import numpy as np
from scipy.linalg import inv
import random


def norm2(a):
    #return ||a||_2
    return np.sqrt(a.transpose().dot(a))

def supp(a,N):
    return np.argsort(a)[::-1][:N]

def re_build(y,n,k,H):
    r = y   #Current residual
    j = 1   #jth iteration
    precision = 1e-8
    max_itr = 350
    dist = 0.0001
    T = []
    while j <= max_itr and norm2(r)/float(norm2(y)) > dist:
        err = np.abs(H.transpose().dot(r))  #Compute current error
        w = supp(err,2*k)        #Support identiﬁcation (the best 2k support set)
        Omega = np.where( err[w] > precision)
        Omega = w[Omega]
        T = np.union1d(Omega,T).astype('int')  #Strongest support merging
        HT = H[:,T]
        Ht = inv(HT.transpose().dot(HT)).dot(HT.transpose())
        bT = Ht.dot(y)   #Least-square signal estimation
        #Pruning
        w = supp(np.abs(bT),k)              
        updated_indices = np.where( np.abs(bT[w]) > precision)
        updated_indices = w[updated_indices]     
        T = T[updated_indices]
        x = np.zeros(H.shape[1])
        x[T] = bT[w]
        r = y - H.dot(x)        
        j +=1
    return x,r

def gen_data():
    n = 200 # number of predictors
    k = 30 # sparsity level
    m = 90

    x = np.zeros(n)
    #x[:k] = np.random.normal(0,1,k)
    for itr in range(k):
        x[np.random.randint(n)]=np.random.normal()
    #np.random.shuffle(x)
    xsparse = x.T
    H = np.random.normal(0,1./np.sqrt(m),(m,n))# sensing  matrix
    y = H.dot(xsparse)  # samples
    return y,H,x

y,H,origx=gen_data()
m=90
n=200
#H= np.random.normal(0,1./np.sqrt(m),(m,n))
x,r=re_build(y,200,30,H)
#print("Compressed signal is:")
#print(y)
#print("Gauss random Matrix is:")
#print(H)
print("rebuild signal:")
print(x-origx)



