import heapq
import os
import threading
from multiprocessing import Process

import Levenshtein as distance
#Ϊ�˻�ͼ���ÿ�����ʵ��û��
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pywt
import scipy
import scipy.signal as signal
from datasketch import WeightedMinHashGenerator
from obspy import read as pread
from obspy import Stream
from scipy.signal import resample
from datasketch import MinHash,LeanMinHash
import mynilsimsa
import simhash
import stft
from getdir import *
from pysac import SacStreamIO


class ReadDirFile(GetDirFile):
    def NameFunc(self,name):
        if(name=="part_1.s28.2015337.out"):
            return True
        return False
    def GetTime(self):
        file=open(self.GetList()[0],"r").readlines()
        time=[]
        for itr in file:
            time.append(float([aa for aa in itr.split(" ") if len(aa)>0][1]))
        return time




DIR = "D:/Weiyuan/"
CATLOG = "catlog/"
TEMPLATES = "templates/"
class SacFig():
    def GetData(self,file):
        st=pread(file)
        return st[0].data
    def PlotMat(self,fig,data,name,sp=None):
        return
        if(sp!=None):
            data=np.reshape(data,sp)
        fig.clf()
        ax=fig.add_subplot(111)
        ax.matshow(data)
        fig.savefig(name)
    def PlotWave(self,fig,dt,itr,name):
        return
        fig.clf()
        timelen=self.wlWinN*self.fqLagN+self.fqWinN
        ax=fig.add_subplot(311)
        ax.plot(dt[0][itr:itr+timelen])
        ax=fig.add_subplot(312)
        ax.plot(dt[1][itr:itr+timelen])
        ax=fig.add_subplot(313)
        ax.plot(dt[2][itr:itr+timelen])
        plt.savefig(name)
    def __init__(self,staName,force=False):
        self.wlWinN=200
        self.wlLagN=5
        self.fqWinN=100
        self.fqLagN=1
        self.fqRspN=16
        self.wlRspN=8
        self.selmax=50
        self.wl_x_level=3
        self.cycle=0
        self.num_perm=20
        self.vectLen=self.fqRspN*self.wlRspN
        self.wmg = WeightedMinHashGenerator(self.selmax,sample_size=10, seed=12)
        self.sta=False
        self.sphs=self.fqLagN*self.wlLagN/100
        self.GetSta(staName,force=force)
        #tempdata=self.GetData("D:/Weiyuan/templates/2---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------*******************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************015318092941.s15.z")
    def GetHash(self):
        self.hash=[]
        step=self.fqLagN*self.wlLagN
        for itr in range(self.datalen):
            data=self.STFT(self.dt,itr*step)
            data=self.WAVELET(data,self.wl_x_level)
            data=self.REGU(data)
            data=self.TRIM(data,self.selmax)
            data=self.FIG(data)
            self.hash.append(data)
        return self.hash
    def GetHashTofile(self,fileName,outfile,force=False):
        ext=[DIR+"s28/2015336/2015336_00_00_00_s28_BHZ.SAC",
             DIR+"s28/2015336/2015336_00_00_00_s28_BHN.SAC",
             DIR+"s28/2015336/2015336_00_00_00_s28_BHE.SAC"]
        scFile=GetTempFiles()
        sig=[]
        for itr in scFile[0]:
            sig.append(self.GetData(itr))
        dt=[]
        if(len(self.GetData(fileName[0]))<10000):
            #print(len(self.GetData(fileName[0])<10000))
            for fn in range(len(fileName)):
                ddt=self.GetData(ext[fn])[:10000]
                cp=len(self.GetData(fileName[fn]))
                #ddt[:cp]=ddt[:cp]+np.zeros([cp])
                ddt[:cp]=ddt[:cp]+self.GetData(fileName[fn])
                dt.append(ddt)
        else:
            for fn in fileName:
                dt.append(self.GetData(fn)[:1000000])
            """
            l=len(sig[0])
            for aa in range(3):
                for bb in range(10):
                    dt[aa][bb*50000:bb*50000+l]+=0#sig[aa]
            """
        #dt=[dt[2]]
        datalen=int((len(dt[0])-self.wlLagN*self.wlWinN-self.fqWinN)/self.fqLagN/self.wlLagN)
        file=open(outfile,"w")
        step=self.fqLagN*self.wlLagN
        times=ReadDirFile("D:/Weiyuan/catlog/").GetTime()
        cyle=0
        fig=plt.figure()
        #for itr in times[:10]+[np.random.randint(10000) for aa in range(10)]:
        for itr in range(datalen):
            #itr=np.random.randint(10000)
            data=self.STFT(dt,int(itr*step))

            self.PlotMat(fig,(data),"figure/fq"+str(itr*step)+".jpg")
            self.PlotWave(fig,dt,int(itr*step),"figure/wave"+str(itr*step)+".jpg")
            data=self.WAVELET(data,self.wl_x_level)
            
            self.PlotMat(fig,np.log(data),
                        "figure/wl"+str(itr*step)+".jpg",
                        [self.wlRspN,self.fqRspN])
            
            data=self.REGU(data)

            self.PlotMat(fig,data,
                        "figure/regu"+str(itr*step)+".jpg",
                        [self.wlRspN,self.fqRspN])
            
            data=self.TRIM(data,self.selmax)
            #continue
            
            data=np.array(self.FIG(data))
            #if(self.cycle==0):
                #dataold=data
            #else:
                #print(len(np.where(data==dataold)[0])/float(self.num_perm))
                #dataold=data
            self.cycle+=1
            tm=itr*step/100
            file.write("%f,"%(tm))
            for itr in data:
                file.write("%d,"%itr)
            file.write("\n")
        file.close()
    def GetSta(self,fileName,force=False):
        if(force==True):
            self.sta=False
            if(os.path.exists("stat.out.npz")==True):
                os.remove("stat.out.npz")
        if(self.sta==True):
            return
        if(os.path.exists("stat.out.npz")==True):
            data=np.load("stat.out.npz")
            self.mu=data['a']
            self.sigma=data['b']
            self.sta=True
            return 
        dt_for_sta=np.zeros([4000,self.vectLen])
        dt=[]
        for fn in fileName:
            dt.append(self.GetData(fn))
        for idx in range(4000):
            data=self.STFT(dt,idx*1000)
            dt_for_sta[idx,:]=self.WAVELET(data,3)
        self.mu   =np.average(dt_for_sta,axis=0)
        self.sigma=np.std(dt_for_sta,axis=0)
        np.savez("stat.out.npz",a=self.mu,b=self.sigma)
        self.sta=True
    def STFT(self,xx,idx):
        fqWin=int(self.fqWinN/2)
        sumx=np.zeros([self.wlWinN,fqWin])
        tpx=np.zeros([self.wlWinN,self.fqWinN])
        for itx in xx:
            #w = np.ones([self.fqWinN])
            w = np.hanning(self.fqWinN)
            #w[:1]=0
            tpx[:,:]=np.zeros([self.wlWinN,self.fqWinN])
            for ii in range(self.wlWinN):
                start=ii*self.fqLagN+idx
                tpx[ii,:]=itx[start:start+self.fqWinN]
            tpx[:,:]=tpx/np.max(tpx)
            X=scipy.fft(tpx,axis=1)
            X=(X*w)[:,:fqWin]
            X=np.square(np.abs(X))
            sumx=np.add(sumx,X)
        sumx=np.sqrt(sumx)
        #sumx[:,:5]=0
        sumx=resample(sumx,self.wlRspN,axis=0)
        sumx=resample(sumx,self.fqRspN,axis=1)
        return sumx
    def WAVELET(self,data,level):
        #outdt=pywt.wavedec2(data,'haar',level=level)
        
        #out=np.zeros([self.vectLen])
        #idx=0
        #out2d=np.zeros([self.wlRspN,self.fqRspN])
        #lenx,leny=np.shape(outdt[0])
        #sumx=lenx
        #sumy=leny
        #out2d[:leny,:lenx]=outdt[0]
        #for itr in outdt[1:]:
        #    lenx,leny=np.shape(itr[0])
        #    out2d[sumy:sumy+leny,         :lenx]=itr[0]
        #    out2d[sumy:sumy+leny,sumx:sumx+lenx]=itr[1]
        #    out2d[         :leny,sumx:sumx+lenx]=itr[2]
        #    sumx+=lenx
        #    sumy+=leny
        #out=np.reshape(out2d,[-1])
        #"""
        out=np.concatenate(pywt.wavedec(data,'haar',level=level,axis=1),axis=1)
        out=np.concatenate(pywt.wavedec(out,'haar',level=level,axis=0),axis=0)
        out=np.reshape(out,[-1])
        #"""
        out2=np.sqrt(np.sum(np.square(out)))
        out=np.divide(out,out2)
        return out
    def REGU(self,data):
        rdata=data-self.mu
        rdata=np.divide(rdata,self.sigma)
        return rdata
    def TRIM(self,data,nlarge):
        absdata=np.abs(data)
        large=heapq.nlargest(nlarge,
                             range(len(data)),
                             key=lambda x:absdata[x])
        lst=np.zeros_like(data)
        for itr in large:
            lst[itr]=data[itr]/absdata[itr]

        rtdata=[]
        for itr in range(len(lst)):
            if(lst[itr]==1):
                rtdata.append("%d"%(itr*2))
            elif(lst[itr]==-1):
                rtdata.append("%d"%(itr*2+1))
        return rtdata
    def FIG(self,tr):
        #wm = self.wmg.minhash(tr) # wm1 is of the type WeightedMinHash
        #vl=np.transpose(wm.hashvalues)
        #vl=vl[0]
        m = MinHash(num_perm=self.num_perm)
        for d in tr:
            m.update(d.encode('utf8'))
        return(m.digest())
            
        

if __name__ == '__main__':
    bits=2
    import time
    USEFOR=["HASH","Template"]
    for useitr in USEFOR[1:]:
        if(useitr=="HASH"):
            tag='.hash12'
            scFile=[[DIR+"s28/2015336/2015336_00_00_00_s28_BHE.SAC",
                    DIR+"s28/2015336/2015336_00_00_00_s28_BHN.SAC",
                    DIR+"s28/2015336/2015336_00_00_00_s28_BHZ.SAC"],
                    [DIR+"s28/2015337/2015337_00_00_00_s28_BHE.SAC",
                    DIR+"s28/2015337/2015337_00_00_00_s28_BHN.SAC",
                    DIR+"s28/2015337/2015337_00_00_00_s28_BHZ.SAC"],
                    [DIR+"s28/2015338/2015338_00_00_00_s28_BHE.SAC",
                    DIR+"s28/2015338/2015338_00_00_00_s28_BHN.SAC",
                    DIR+"s28/2015338/2015338_00_00_00_s28_BHZ.SAC"]
                    ][1:2]
            a1=SacFig(scFile[0],force=True)
        else:
            a1=SacFig([DIR+"s28/2015336/2015336_00_00_00_s28_BHE.SAC",
                    DIR+"s28/2015336/2015336_00_00_00_s28_BHN.SAC",
                    DIR+"s28/2015336/2015336_00_00_00_s28_BHZ.SAC"],force=False)
            tag=".template12"
            scFile=GetTempFiles()
        for fileName in scFile:
            names=fileName[0].split('/')
            #Process(target=a1.GetHashTofile,
                #args=(fileName,names[2]+names[3]+tag)).start()
            a1.GetHashTofile(fileName,names[2]+names[3]+tag)
            print(fileName)
        #break

