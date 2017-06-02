from obspy import read as pread
from obspy import Stream
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

stream = Stream()
stream = pread("after/SC.XJI.2008133160000.D.00.BHN.sac")
stream += pread("after/SC.XJI.2008133160000.D.00.BHZ.sac")
stream += pread("after/SC.XJI.2008133160001.D.00.BHE.sac")
stream.detrend()
ptd=[]

for ii in range(2000):
        ptd.append(stream[0].data[ii:ii+1000])
plt.matshow(ptd)
plt.show()

print(stream[0].stats.starttime)
print("%d,%d,%d,%d,%d,%d"%(stream[0].stats.sac.nzyear,
                stream[0].stats.sac.nzjday,
                stream[0].stats.sac.nzhour,
                stream[0].stats.sac.nzmin,
                stream[0].stats.sac.nzsec,
                stream[0].stats.sac.nzmsec))
print(stream[1].stats.starttime)
print(stream[1].stats.endtime)
print("%d,%d,%d,%d,%d,%d"%(stream[1].stats.sac.nzyear,
                stream[1].stats.sac.nzjday,
                stream[1].stats.sac.nzhour,
                stream[1].stats.sac.nzmin,
                stream[1].stats.sac.nzsec,
                stream[1].stats.sac.nzmsec))
print(stream[2].stats.starttime)
print("%d,%d,%d,%d,%d,%d"%(stream[2].stats.sac.nzyear,
                stream[2].stats.sac.nzjday,
                stream[2].stats.sac.nzhour,
                stream[2].stats.sac.nzmin,
                stream[2].stats.sac.nzsec,
                stream[2].stats.sac.nzmsec))

print(stream[2].stats.sac.stla)
print(stream[2].stats.sac.stlo)