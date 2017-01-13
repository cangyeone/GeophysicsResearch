# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:07:55 2015

@author: Cy
"""
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy

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
        

fig = plt.figure()
ax=fig.add_subplot(111);
plt.axis('equal')
ax.set_xlabel("X(km)")
ax.set_ylabel("Y(km)")

faultFileName='frame.txt'
inFile=open(faultFileName,'r')
asciiData=inFile.read()
data=atof(asciiData)

def update_lines(t):
    plt.cla();
    frame=data[int(t*10)]
    x=frame[0]
    y=frame[1]
    u=frame[2]
    v=frame[3]
    scal=[]
    for idx in range(0,len(x)):
        scal.append((u[idx]*u[idx]+v[idx]*v[idx])*60)
    ax.scatter(x, y, s=scal,c='k',alpha=0.4)
    return mplfig_to_npimage(fig)
    
# Attaching 3D axis to the figure
# Fifty lines of random 3-D lines

# Creating the Animation object
 
animation =mpy.VideoClip(update_lines, duration=9)
animation.write_gif("st.gif", fps=10)
#plt.show()