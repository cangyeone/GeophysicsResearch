# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 13:53:58 2015

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
print(data[0])
plt.figure()
for frame in data:
    plt.quiver(frame[0],frame[1],frame[2],frame[3])
plt.show()




#plt.show()
