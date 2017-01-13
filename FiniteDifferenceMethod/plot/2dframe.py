# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 11:13:43 2015

@author: Cy
"""
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
faultFileName='lines.txt'
inFile=open(faultFileName,'r')
asciiData=inFile.read()
data=atof(asciiData)
for lines in data[4]:
    plt.plot(lines[0],lines[1],c='k',alpha=0.4)

plt.savefig('2DTimeDomainFrameGraph.png',dpi=300)
plt.show()
