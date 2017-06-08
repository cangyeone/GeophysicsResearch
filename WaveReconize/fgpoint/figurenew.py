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
    def __init__(self,fileName):
        self.wlWinN=300
        self.wlLagN=10
        self.fqWinN=300
        self.fqLagN=10
        self.fqRspN=64
        self.wlRspN=64
        self.selmax=600
        self.wl_x_level=3
        self.vectLen=self.fqRspN*self.wlRspN
        self.wmg = WeightedMinHashGenerator(self.vectLen,sample_size=2, seed=12)
        self.sta=False
        self.sphs=self.fqLagN*self.wlLagN/100
        self.GetSta(fileName)
        self.fileName=fileName
        self.dt=self.GetData(fileName)[:500000]
        self.datalen=int((len(self.dt)-self.wlLagN*self.wlWinN-self.fqWinN)/self.fqLagN/self.wlLagN)
        tempdata=self.GetData("D:/Weiyuan/templates/2015318092941.s15.z")
        for itr in range(5):
            start=itr*50000+27
            end=start+len(tempdata)
            self.dt[start:end]=self.dt[start:end]+tempdata*0.2
        plt.plot(self.dt)
        plt.show()
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
    def GetHashTofile(self,file):
        self.hash=[]
        step=self.fqLagN*self.wlLagN
        for itr in range(self.datalen):
            data=self.STFT(self.dt,itr*step)
            data=self.WAVELET(data,3)
            data=self.REGU(data)
            data=self.TRIM(data,self.selmax)
            data=self.FIG(data)
            self.hash.append(data)
            tm=itr*self.sphs
            file.write("%f,"%(tm))
            for itr in data:
                file.write("%d,"%itr)
            file.write("\n")
    def GetSta(self,fileName,force=False):
        if(self.sta==True):
            return
        if(os.path.exists("stat.out.npz")==True):
            data=np.load("stat.out.npz")
            self.mu=data['a']
            self.sigma=data['b']
            self.sta=True
            return 
        dt_for_sta=np.zeros([4000,self.vectLen])
        dta=self.GetData(fileName)
        for idx in range(4000):
            dt=self.STFT(dta,idx*1000)
            dt_for_sta[idx,:]=self.WAVELET(dt,3)
        self.mu   =np.average(dt_for_sta,axis=0)
        self.sigma=np.std(dt_for_sta,axis=0)
        np.savez("stat.out.npz",a=self.mu,b=self.sigma)
        self.sta=True
    def STFT(self,x,idx):
        w = np.hanning(self.fqWinN)
        fqWin=int(self.fqWinN/2)
        X=np.zeros([self.wlWinN,self.fqWinN])
        for ii in range(self.wlWinN):
            start=ii*self.fqLagN+idx
            X[ii,:]=
        def IterStft(i):
            start=i*self.fqLagN+idx
            return resample(scipy.fft(w*(x[start:start+self.fqWinN]))[0:fqWin],
                        self.fqRspN)
        X=list(map(IterStft,range(0, self.wlWinN)))
        X=np.abs(np.array(X))
        X=resample(X,self.wlRspN,axis=0)
        return X
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
            if(data[itr] > 0):
                lst[itr]=1
            else:
                lst[itr]=-1
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
if __name__ == '__main__':
    bits=2
    import time
    #scFile=GetSecFile()
    scFile=[[DIR+"s14/2015333/2015333_00_00_00_s14_BHZ.SAC",
             DIR+"s14/2015333/2015333_00_00_00_s14_BHN.SAC",
             DIR+"s14/2015333/2015333_00_00_00_s14_BHE.SAC"]]
    for fileName in scFile[0]:
        a1=SacFig(fileName)
        file=open("hash.txt","w")
        a1.GetHashTofile(file)
        break

        

    
    
    
