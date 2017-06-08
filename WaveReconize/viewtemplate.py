from DIRS import *
from getfiles.getdir import *
import numpy.fft as fft
import scipy.signal as signal
tpfile=GetTemplate(DIR+TEMPLATES)
tplist=tpfile.GetList()
allinall=[]
ll=[]
for itr in tplist:
    data,time=GetSacInfo(itr)
    allinall.append(signal.resample(data,2000))
    fftdata=fft.fft(data)
    ll.append(signal.resample(fftdata,2000)[:1000])
allinall=np.array(allinall)
np.savez("template.npz",c=allinall)
print(np.shape(allinall))

ary=np.array(ll)
ary=np.abs(ary)
ary2=np.square(ary)
ary2sum=np.sqrt(np.sum(ary2,axis=1))
ary2sum=np.transpose([ary2sum])
ary=np.divide(ary,ary2sum)
aryfilt=np.sum(ary,axis=0)
arystd=np.std(ary,axis=0)
#ary=ary/np.max(ary)
fig=plt.figure(1)
ax=fig.add_subplot(311)
x=np.linspace(0,50,len(ary[0]))
ax.plot(x,aryfilt)
ax=fig.add_subplot(312)
x=np.linspace(0,50,len(ary[0]))
ax.plot(x,arystd)
ax=fig.add_subplot(313)
ax.matshow(signal.resample(ary,100,axis=1))
fig2=plt.figure(2)

plt.show()
