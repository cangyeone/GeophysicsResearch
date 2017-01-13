# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 11:13:43 2015

@author: Cy
"""

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

def atof(data):
    dts=data.split('frame\n')
    rtdata=[]
    zh=0
    for fts in dts:
        if(len(fts)>10):
            pic=[]
            frame=fts.split('lines\n')
            for lines in frame:
                x=[]
                y=[]
                if(len(lines)>10):
                    data=lines.split('\n')
                    for elems in data:
                        if(len(elems)>10):
                            elem=elems.split(',')
                            x.append(float(elem[0].strip()))
                            y.append(float(elem[1].strip()))
                pic.append([x,y,[zh for ddtm in x]])
            rtdata.append(pic)
        zh=zh+1
    return rtdata
        

fig = plt.figure()
ax = fig.gca(projection='3d')

faultFileName='lines.txt'
inFile=open(faultFileName,'r')
asciiData=inFile.read()
data=atof(asciiData)
for frame in data[1:]:
    for lines in frame[1:]:
        ax.plot(lines[0],lines[1],lines[2],c='k',alpha=0.4)
ax.set_xlabel("X(km)")
ax.set_ylabel("Y(km)")
ax.set_zlabel("Time(s)")
ax.set_title("2D Frame Graph in Time Domain")
plt.savefig('TimeDomainFrameGraph.png',dpi=300)
plt.show()
