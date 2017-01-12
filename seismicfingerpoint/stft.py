# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 18:49:17 2016

@author: LLL
"""
import scipy
import numpy as np
from scipy.signal import resample
import scipy.signal as ssg
def stft(x,framesamp,hopsamp,rspN):
    w = np.hanning(framesamp)
    fqWin=int(framesamp/2)
    def IterStft(i):
        return resample(scipy.fft(w*(x[i:i+framesamp]))[0:fqWin],rspN)
    X=list(map(IterStft,range(0, len(x)-framesamp, hopsamp)))
    return np.array(X)


def dataresample(data,num):
    rdata=[]
    for dt in data:
        rdata.append(resample(dt,num))
    return np.array(rdata)
    
def istft(X, fs, T, hop):
    x = scipy.zeros(T*fs)
    framesamp = X.shape[1]
    hopsamp = int(hop*fs)
    for n,i in enumerate(range(0, len(x)-framesamp, hopsamp)):
        x[i:i+framesamp] += scipy.real(scipy.ifft(X[n]))
    return x
    
def norm(x):
    for itr in range(len(x)):
        x[itr]=np.divide(x[itr],np.max(x[itr]))
import pywt        
def mywavelet_x(data,win_n_len,lap_n_len,level=3):
    rdata=[]
    
    for itr in data:
        nitr=len(itr)
        rws=np.array([])
        for ii in range(0,nitr-win_n_len,lap_n_len):
            #rw=pywt.wavedec(resample(itr[ii:ii+win_n_len],rsp),'haar',level=level)
            rw=pywt.wavedec(resample(itr[ii:ii+win_n_len],rsp),'haar',level=level)
            for ii in range(level+1):
                rws=np.append(rws,rw[ii])
            #rws=np.append(rws,rw[3])
            #rws=np.append(rws,rw[4])
        rdata.append(rws)
    return np.array(rdata)
    
def mywavelet_y(data,win_n_len,lap_n_len,rsp,level=3):
    rdata=[]
    
    for itr in data:
        rws=np.array([])
        rw=pywt.wavedec(itr, 'haar',level=level)
        for ii in range(level+1):
            rws=np.append(rws,rw[ii])
        rdata.append(rws)
    return np.array(rdata)

def mywavelet2d(data,winLen,lapLen,rsp):
    nx=len(data[0])
    rdata=np.zeros([len(data),int((nx-winLen)/lapLen+1)*rsp])
    
    xin=int(rsp/2)
    yin=int(len(data)/2)
    for ii in range(0,nx-winLen,lapLen):
        data2d=data[:,(ii):(ii+winLen)]
        data2d=dataresample(data2d,rsp)
        coeffs = pywt.dwt2(data2d, 'haar')
        cA, (cH, cV, cD) = coeffs
        for xi in range(xin):
            for yi in range(yin):

                rdata[yi+yin,int(ii/lapLen*rsp)+xi]=cD[yi,xi]
                rdata[yi+yin,int(ii/lapLen*rsp)+xi+xin]=cV[yi,xi]
                rdata[yi,int(ii/lapLen*rsp)+xi]=cA[yi,xi]
                rdata[yi,int(ii/lapLen*rsp)+xi+xin]=cH[yi,xi]
    return rdata
    
def mywaveletwithresample(data,win_n_len,lap_n_len):
    rdata=[]
    
    for itr in data:
        nitr=len(itr)
        rws=np.array([])
        for ii in range(0,nitr-win_n_len,lap_n_len):
            rw=pywt.wavedec(itr[ii:ii+win_n_len],'haar',level=4)
            rws=np.append(rws,rw[0])
            rws=np.append(rws,rw[1])
            rws=np.append(rws,rw[2])
            rws=np.append(rws,rw[3])
            rws=np.append(rws,rw[4])
        rdata.append(rws)
    return np.array(rdata)

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    