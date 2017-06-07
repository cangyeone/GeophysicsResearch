
DIR = "D:/Weiyuan/"
CATLOG = "catlog/"
from obspy import read as pread
from obspy import Stream
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

from getfiles.getdir import *

cGetLogDir=GetLogDir(DIR+CATLOG)

logDirs=cGetLogDir.GetDirList()
ccct=0
for itr in logDirs:
    logFileTime=GetLogFile(itr[0])
    for sacFile in os.listdir(DIR+itr[1]+itr[2]):
        print(DIR+itr[1]+itr[2]+sacFile)
        stream=pread(DIR+itr[1]+itr[2]+sacFile)
        for time_t in logFileTime:
            time_i=int(time_t*100)
            plt.plot(stream[0].data[time_i:time_i+1000],c='k')
            ccct=1
        if(ccct==1):
            break
    if(ccct==1):
        break
plt.show()
