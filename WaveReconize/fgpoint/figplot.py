
from getdir import *
import os
import matplotlib.pyplot as plt
import numpy as np
scFile=[[DIR+"s28/2015336/2015336_00_00_00_s28_BHZ.SAC",
        DIR+"s28/2015336/2015336_00_00_00_s28_BHN.SAC",
        DIR+"s28/2015336/2015336_00_00_00_s28_BHE.SAC"],
        [DIR+"s28/2015337/2015337_00_00_00_s28_BHZ.SAC",
        DIR+"s28/2015337/2015337_00_00_00_s28_BHN.SAC",
        DIR+"s28/2015337/2015337_00_00_00_s28_BHE.SAC"],
        [DIR+"s28/2015338/2015338_00_00_00_s28_BHZ.SAC",
        DIR+"s28/2015338/2015338_00_00_00_s28_BHN.SAC",
        DIR+"s28/2015338/2015338_00_00_00_s28_BHE.SAC"]
        ][1:2]

st=pread(scFile[0][0])
st+=pread(scFile[0][1])
st+=pread(scFile[0][2])
st.plot()
a1=st[0].data[500000:1000000]
a2=st[1].data[500000:1000000]
a3=st[2].data[500000:1000000]
x=np.linspace(5000,10000,len(a1))
fig=plt.figure(1)
ax=fig.add_subplot(311)
ax.plot(x,a1)
ax=fig.add_subplot(312)
ax.plot(x,a2)
ax=fig.add_subplot(313)
ax.plot(x,a3)
plt.show()
