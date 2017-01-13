# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 19:57:43 2016

@author: Q
"""

import matplotlib.pyplot as plt
import numpy as np
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
from scipy.integrate import odeint  
# DRAW A FIGURE WITH MATPLOTLIB
 
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
duration = 2


fig = plt.figure()

faultFileName='lines.txt'
inFile=open(faultFileName,'r')
asciiData=inFile.read()
data=atof(asciiData)

ax=fig.add_subplot(111);
ax.set_xlabel("X(km)")
ax.set_ylabel("Y(km)")
ax.set_title("2D Frame Graph in Time Domain")
plt.axis('equal')
# ANIMATE WITH MOVIEPY (UPDATE THE CURVE FOR EACH t). MAKE A GIF.


def update_lines(t):
    plt.cla();

    for lines in data[int(t*10)]:
        ax.plot(lines[0],lines[1],c='k',alpha=0.4)
    return mplfig_to_npimage(fig)
    
# Attaching 3D axis to the figure
# Fifty lines of random 3-D lines

# Creating the Animation object
 
animation =mpy.VideoClip(update_lines, duration=9)
animation.write_gif("long.gif", fps=10)