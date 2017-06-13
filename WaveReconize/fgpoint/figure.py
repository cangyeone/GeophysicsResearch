import pywt
from scipy.signal import resample
import os
from obspy import read as pread
from obspy import Stream
import numpy as np
import matplotlib.pyplot as plt
from pysac import SacStreamIO
import stft
import heapq
import scipy
#为了画图更好看，其实并没有
import matplotlib as mpl
import scipy.signal as signal

import simhash
import mynilsimsa
from datasketch import WeightedMinHashGenerator   
#mpl.style.use('seaborn-darkgrid')

DIR = "D:/Weiyuan/"
CATLOG = "catlog/"
TEMPLATES = "templates/"
class SacFig():
    def GetData(self,file):
        st=pread(file)
        return st[0].data
    def __init__(self,staName,force=False):
        self.wlWinN=300
        self.wlLagN=5
        self.fqWinN=200
        self.fqLagN=5
        self.fqRspN=32
        self.wlRspN=32
        self.selmax=15
        self.wl_x_level=3
        self.vectLen=self.fqRspN*self.wlRspN
        self.wmg = WeightedMinHashGenerator(self.vectLen,sample_size=2, seed=12)
        self.sta=False
        self.sphs=self.fqLagN*self.wlLagN/100
        self.GetSta(staName,force=force)
        #tempdata=self.GetData("D:/Weiyuan/templates/2015318092941.s15.z")
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
                dt.append(self.GetData(fn)[500000:1000000])
        #dt=[dt[2]]
        datalen=int((len(dt[0])-self.wlLagN*self.wlWinN-self.fqWinN)/self.fqLagN/self.wlLagN)
        file=open(outfile,"w")
        step=self.fqLagN*self.wlLagN
        for itr in range(datalen):
            data=self.STFT(dt,itr*step)
            data=self.WAVELET(data,3)
            data=self.REGU(data)
            data=self.TRIM(data,self.selmax)
            try:
                data=self.FIG(data)
            except:
                data=[0,0]
            tm=itr*self.sphs
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
            w = np.ones([self.fqWinN])
            #w = np.hanning(self.fqWinN)
            w[0]=w[1]=0
            tpx[:,:]=np.zeros([self.wlWinN,self.fqWinN])
            for ii in range(self.wlWinN):
                start=ii*self.fqLagN+idx
                tpx[ii,:]=itx[start:start+self.fqWinN]*w
            tpx[:,:]=tpx/np.max(tpx)
            X=scipy.fft(tpx,axis=1)[:,:fqWin]
            X=np.square(np.abs(X))
            sumx=np.add(sumx,X)
        sumx=np.sqrt(sumx)
        sumx=resample(sumx,self.wlRspN,axis=0)
        sumx=resample(sumx,self.fqRspN,axis=1)
        return sumx
    def WAVELET(self,data,level):
        outdt=pywt.wavedec2(data,'haar',level=level)
        out=np.zeros([self.vectLen])
        idx=0
        for itr in outdt:
            evaldt=np.reshape(itr,[-1])
            cit=len(evaldt)
            out[idx:idx+cit]=evaldt[:]
            idx+=cit
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
        return lst
    def FIG(self,tr):
        wm = self.wmg.minhash(tr) # wm1 is of the type WeightedMinHash
        vl=np.transpose(wm.hashvalues)
        vl=vl[0]
        return(vl.tolist())
            
        
def PrintDT1(outFile,lgt,hdT):
    sc=0
    for it in hdT:
        sc+=1
        tm=lgt*sc
        outFile.write("%f,"%(tm))
        for itr in it:
            outFile.write("%d,"%itr)
        outFile.write("\n")
        #outFile.write("%f,%d,%d\n"%(sc,a1.hash[it][0],a1.hash[it][1]))
        
def PrintDT2(file,dt):
    sc=0
    for it in hdT:
        sc+=1
        tm=1*sc
        #outFile.write("%d:%d:%d,"%(int(tm/3600),int((tm%3600)/60),int(tm%60)))
        outFile.write("%5.1f,"%(it[-1]))
        for itr in it[:-1]:
            outFile.write("%d,"%itr)
        outFile.write("\n")
        #outFile.write("%f,%d,%d\n"%(sc,a1.hash[it][0],a1.hash[it][1]))
import threading
from multiprocessing import Process
from getdir import *
if __name__ == '__main__':
    bits=2
    import time
    USEFOR=["HASH","Template"]
    for useitr in USEFOR:
        if(useitr=="HASH"):
            tag='.hash10'
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
            tag=".template10"
            scFile=GetTempFiles()
        for fileName in scFile:
            names=fileName[0].split('/')
            #Process(target=a1.GetHashTofile,
                #args=(fileName,names[2]+names[3]+tag)).start()
            a1.GetHashTofile(fileName,names[2]+names[3]+tag)
            print(fileName)
            #break

        

    
    
    
 