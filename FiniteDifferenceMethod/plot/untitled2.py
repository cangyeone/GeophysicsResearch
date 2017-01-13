# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:19:34 2015

@author: Cy
"""

import pylab as plt
def atof(data):
    dts=data.split('frame\n')
    rtdata=[]
    for fts in dts:
        rtline=[]
        dtasc=fts.split('\n')
        x=[]
        y=[]
        u=[]
        v=[]
        for dotasc in dtasc:
            if (len(dotasc)>10):
                sdot=dotasc.split(',')
                x.append(float(sdot[0].strip()))
                y.append(float(sdot[1].strip()))
                u.append(float(sdot[2].strip()))
                v.append(float(sdot[3].strip()))
        rtline=[x,y,u,v]
        rtdata.append(rtline)
    return rtdata
        
faultFileName='out.txt'
inFile=open(faultFileName,'r')
asciiData=inFile.read()
data=atof(asciiData)
plt.figure()
count=0
x=[]
y=[]
z=[]
u=[]
v=[]
w=[]
for frame in data[1:]:
    count=count+1
    x=x+frame[0]
    y=y+frame[1]
    u=u+frame[2]
    v=v+frame[3]
    for nb in frame[0]:
        z.append(count)
        w.append(0)
plt.quiver(x,y,z,u,v,w)
plt.show()
