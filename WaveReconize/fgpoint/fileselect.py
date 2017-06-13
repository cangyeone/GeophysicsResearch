
from getdir import *
import os
import matplotlib.pyplot as plt
import numpy as np
import time as tm
DIR = "D:/Weiyuan/"
CATLOG = "catlog/"
TEMPLATES = "templates/"
class GetHashFile(GetDirFile):
    def NameFunc(self,fileName):
        names=fileName.split(".")
        if(names[-1]=="hash8"):
            return True
        
class GetTempFile(GetDirFile):
    def NameFunc(self,fileName):
        names=fileName.split(".")
        if(names[-1]=="template8"):
            return True
class IDX():
    def __init__(self,fileName):
        self.fileName=fileName
    def BuildIndex(self):
        self.idx=[]
        self.ReadFile()
        return self.data
    def ReadFile(self):
        self.data=[]
        for itr in self.fileName:
            file=open(itr).readlines()
            dta=[]
            dic={}
            for fle in file:
                dta.append([aa.strip() for aa in fle.split(',') if len(aa)>0])
            for ii in dta:
                try:
                    if(dic.get(ii[1])==None):
                        dic[ii[1]]={}
                        dic[ii[1]][ii[2]]=[]
                        dic[ii[1]][ii[2]].append(float(ii[0]))
                    else:
                        if(dic[ii[1]].get(ii[2])==None):
                            dic[ii[1]][ii[2]]=[]
                            dic[ii[1]][ii[2]].append(float(ii[0]))
                        else:
                            dic[ii[1]][ii[2]].append(float(ii[0]))
                except:
                    print("Err build idx",ii)
            self.data.append(dic)
class TMP():
    def __init__(self,fileName):
        self.fileName=fileName
    def GetData(self):
        self.idx=[]
        self.ReadFile()
        return self.data
    def ReadFile(self):
        self.data=[]
        for itr in self.fileName:
            file=open(itr).readlines()
            dta=[]
            for fle in file:
                dta.append([aa.strip() for aa in fle.split(',') if len(aa)>0])
            self.data.append(dta)
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
from obspy import read as pread
if __name__=="__main__":
    start=tm.clock()
    HSF=GetHashFile(os.getcwd()+'/').GetList()
    TPF=GetTempFile(os.getcwd()+'/').GetList()
    ID=IDX(HSF)
    TP=TMP(TPF).GetData()
    idx=ID.BuildIndex()
    times=[]
    for xx in TP:
        for yy in xx[6:12]:
            try:
                if(len(idx[0][yy[1]][yy[2]])>10000):
                    pass
                times+=idx[0][yy[1]][yy[2]]
            except:
                pass
    times=sorted(times)
    #plt.scatter(times,np.ones_like(times))
    #plt.show()
    time=[[0,0]]
    cont=0
    old=0
    for itr in times:
        if(itr-old>10):
            time[-1][1]=cont
            cont=1
            time.append([itr,0])
        else:
            cont+=1
        old=itr
    file=open("out.select","w")
    cont=0
    
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
    fig=plt.figure(1)
    xxx=np.linspace(0,20,2000)
    a1=st[0].data
    a2=st[1].data
    a3=st[2].data
    for itr in time:
        if(itr[1]>1):
            plt.clf()
            file.write(str(itr[0])+"\n")
            continue
            stt=int(itr[0]*100)
            edd=stt+2000
            ax=fig.add_subplot(311)
            ax.plot(xxx+5000+itr[0],a1[stt:edd])
            ax=fig.add_subplot(312)
            ax.plot(xxx+5000+itr[0],a2[stt:edd])
            ax=fig.add_subplot(313)
            ax.plot(xxx+5000+itr[0],a3[stt:edd])
            plt.savefig("figure/"+str(5000+itr[0])+".jpg")
    end=tm.clock()
    print("Time:",end-start)