# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:32:04 2017

@author: LLL
"""

import tensorflow as tf
import os
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import matplotlib as mpl
mpl.style.use('seaborn-darkgrid')


def GetSecFile(tag=".sec"):
    itrlist=os.walk(os.getcwd())
    sacFile=[]
    for itr in itrlist:
        for it in itr[2]:
            if(it[-4:]==tag):
                sacFile.append(itr[0]+"\\"+it)
    return sacFile

def GetFileData(file):
    dtFile=open(file,"r")
    dData=dtFile.readlines()
    dtL=0
    for itr in dData:
        dtL=dtL+1
        if(itr[0:4]=="DATE"):
            break
    rtData=[]
    for itr in dData[dtL:]:
        slt=[it for it in itr.split(' ') if(len(it)>0)][3:6]
        sltd=[float(it) for it in slt]
        rtData.append(sltd)
    dtFile.close()
    return np.array(rtData)
scFile=GetSecFile()
for itrF in scFile[0:10]:
    rtData=GetFileData(itrF)
    plt.plot(np.transpose(rtData)[0])
    plt.plot(np.transpose(rtData)[1])
    plt.plot(np.transpose(rtData)[2])
plt.show()
