import numpy as np

from obspy import read as pread
from obspy import Stream
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy.signal as signal

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
nzy1,nzd1,nzs1=(stream[0].stats.sac.nzyear,
                stream[0].stats.sac.nzjday,
                stream[0].stats.sac.nzhour*3600+
                stream[0].stats.sac.nzmin*60+
                stream[0].stats.sac.nzsec+
                stream[0].stats.sac.nzmsec/1000)
nzy2,nzd2,nzs2=(stream[1].stats.sac.nzyear,
                stream[1].stats.sac.nzjday,
                stream[1].stats.sac.nzhour*3600+
                stream[1].stats.sac.nzmin*60+
                stream[1].stats.sac.nzsec+
                stream[1].stats.sac.nzmsec/1000)
nzy3,nzd3,nzs3=(stream[2].stats.sac.nzyear,
                stream[2].stats.sac.nzjday,
                stream[2].stats.sac.nzhour*3600+
                stream[2].stats.sac.nzmin*60+
                stream[2].stats.sac.nzsec+
                stream[2].stats.sac.nzmsec/1000)
nzs_t=np.array([nzs1,nzs2,nzs3])
nzpt_t=np.array([stream[0].stats.npts,stream[1].stats.npts,stream[2].stats.npts])
nzs_t1=np.subtract(nzs_t,np.max(nzs_t))*100
nzs=np.max(nzs_t)
nzpt=int(np.min(nzpt_t-nzs_t1))
seismic3d=np.zeros([nzpt,3])
nzs_t1=np.abs(nzs_t1)
print(nzs_t1)
sampling_rate=100
#b, a = signal.iirdesign([0.0001, 0.2], [0.00009, 0.21], 2, 40)
#b, a = signal.iirdesign([0.0001, 0.2], [0.00001, 0.3], 2, 40)

for ii in range(3):
    wave=signal.detrend(stream[ii].data[int(nzs_t1[ii]):int(nzs_t1[ii])+nzpt])
    seismic3d[:,ii]=wave
    #np.real(signal.lfilter(b,a,wave))
la=31.0
lo=102.36


dt1 = FileToList("dir/dir1.txt")
dt2 = FileToList("dir/dir2.txt")
count=0
fig1=plt.figure(1)
fig3=plt.figure(3)
shape=[800,8000]
ptd3d=np.zeros(shape+[3])

for itr in dt1:
    dmy=[float(aa) for aa in itr[0].split("/")]
    hms=[float(aa) for aa in itr[1].split(":")]
    sec=hms[0]*3600+hms[1]*60+hms[1]+(dmy[2]-12)*24*3600

    si1=np.sin(np.pi/2-la/180*np.pi)*6731*np.tan(np.abs(float(itr[3])-lo)/180*np.pi)
    si2=np.sin(np.abs(float(itr[2])-la)/180*np.pi)*6371
    si=np.sqrt(si1**2+si2**2)
    if(si>500):
        continue
    arv_time=si/10
    exceed=0
    ds1=(sec-nzs)+arv_time
    de1=(sec-nzs-nzpt*0.01)+arv_time
        #print(ds1,de1)
    if(ds1<0 or de1>0):
        continue
    for jj in range(shape[0]):
        ptd3d[jj,:,:]=seismic3d[jj+int(ds1*100):jj+int(ds1*100)+shape[1],:]
    ons=np.ones(shape+[3])
    ptd_min=np.min(ptd3d)
    
    ptd=np.subtract(ptd3d,ons*ptd_min)
    ptd_max=np.max(np.abs(ptd))*ons
    ptd=np.divide(ptd,ptd_max)
    ptd3d=ptd*2-1
    #print(np.max(ptd3d),np.min(ptd3d))
    print("fig/"+itr[0]+itr[1]+str(count)+".jpg")
    
    fig1.clf()    
    ax1=fig1.add_subplot(3,1,1)
    ax1.plot(ptd3d[0,:,0])
    ax1=fig1.add_subplot(3,1,2)
    ax1.plot(ptd3d[0,:,1])
    ax1=fig1.add_subplot(3,1,3)
    ax1.plot(ptd3d[0,:,2])
    fig1.savefig("fig/"+str(count)+"_plot"+".jpg")

    fig3.clf()
    ax3=fig3.add_subplot(1,1,1)
    ax3.imshow(np.abs(ptd3d))
    fig3.savefig("fig/"+str(count)+"_mat3d"+".jpg")
    count+=1