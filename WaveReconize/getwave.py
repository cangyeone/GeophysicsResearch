import numpy as np

from obspy import read as pread
from obspy import Stream
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def FileToList(fileName):
    f=open(fileName,"r",encoding=None)
    fdata=f.readlines()
    data=[]
    for itr in fdata:
        #print(itr)
        if(itr[:2]=='20'):
            data.append([ii.strip() for ii in itr.split() if(len(ii)>0)])
    return data

stream = Stream()
stream = pread("after/SC.XJI.2008133160000.D.00.BHN.sac")
stream += pread("after/SC.XJI.2008133160000.D.00.BHZ.sac")
stream += pread("after/SC.XJI.2008133160001.D.00.BHE.sac")
stream.detrend()
ptd=[]
"""
for ii in range(1000):
        ptd.append(stream[0].data[ii:ii+1000])
plt.matshow(ptd)
plt.show()
"""

nzy1,nzd1,nzs1=(stream[0].stats.sac.nzyear,
                stream[0].stats.sac.nzjday,
                stream[2].stats.sac.nzhour*3600+
                stream[2].stats.sac.nzmin*60+
                stream[2].stats.sac.nzsec+
                stream[2].stats.sac.nzmsec/1000)
nzy2,nzd2,nzs2=(stream[1].stats.sac.nzyear,
                stream[1].stats.sac.nzjday,
                stream[2].stats.sac.nzhour*3600+
                stream[2].stats.sac.nzmin*60+
                stream[2].stats.sac.nzsec+
                stream[2].stats.sac.nzmsec/1000)
nzy3,nzd3,nzs3=(stream[2].stats.sac.nzyear,
                stream[2].stats.sac.nzjday,
                stream[2].stats.sac.nzhour*3600+
                stream[2].stats.sac.nzmin*60+
                stream[2].stats.sac.nzsec+
                stream[2].stats.sac.nzmsec/1000)

nzs=[nzs1,nzs2,nzs3]
la=31.0
lo=102.36
dt1 = FileToList("dir/dir1.txt")
dt2 = FileToList("dir/dir2.txt")
#print(dt1[:3])
#print(dt2[:3])

count=0
fig1=plt.figure(1)
fig2=plt.figure(2)
for itr in dt1:
    dmy=[float(aa) for aa in itr[0].split("/")]
    hms=[float(aa) for aa in itr[1].split(":")]
    sec=hms[0]*3600+hms[1]*60+hms[1]+(dmy[2]-12)*24*3600

    si1=np.sin(np.pi/2-la/180*np.pi)*6731*np.tan(np.abs(float(itr[3])-lo)/180*np.pi)
    si2=np.sin(np.abs(float(itr[2])-la)/180*np.pi)*6371
    si=np.sqrt(si1**2+si2**2)
    if(si>500):
        continue
    arv_time=si/8
    fig1.clf()
    exceed=0
    fig2.clf()
    for ii in range(3):
        ds1=(sec-nzs[ii])+arv_time-1000
        de1=(sec-nzs[ii]-stream[ii].stats.npts*stream[ii].stats.delta)+arv_time
        ax1=fig1.add_subplot(3,1,ii+1)
        if(ds1>0 and de1<0):
            ax1.plot(stream[ii].data[int(ds1*100):int(ds1*100)+20000])
        else:
            exceed=1
        ptd=[]
        for jj in range(2000):
                ptd.append(stream[ii].data[jj+int(ds1*100):jj+int(ds1*100)+20000])
        ax2=fig2.add_subplot(3,1,ii+1)
        ax2.matshow(np.log(ptd))
        
    count+=1
    if(exceed==1):
        continue
    print("fig/"+itr[0]+itr[1]+str(count)+".jpg")
    fig1.savefig("fig/"+str(count)+".jpg")
    fig2.savefig("fig/"+str(count)+"_mat"+".jpg")