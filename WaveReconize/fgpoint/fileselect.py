
from getdir import *
import os
import matplotlib.pyplot as plt
import numpy as np

class GetHashFile(GetDirFile):
    def NameFunc(self,fileName):
        names=fileName.split(".")
        if(names[-1]=="hash"):
            return True
        
class GetTempFile(GetDirFile):
    def NameFunc(self,fileName):
        names=fileName.split(".")
        if(names[-1]=="template"):
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
if __name__=="__main__":
    HSF=GetHashFile(os.getcwd()).GetList()
    TPF=GetTempFile(os.getcwd()).GetList()
    ID=IDX(HSF)
    TP=TMP(TPF).GetData()
    idx=ID.BuildIndex()
    times=[]
    for xx in TP:
        for yy in xx[:8]:
            try:
                times+=idx[0][yy[1]][yy[2]]
            except:
                pass
    times=sorted(times)
    #plt.scatter(times,np.ones_like(times))
    #plt.show()
    time=[]
    old=0
    for itr in times:
        if(itr-old!=0):
            time.append(itr)
        old=itr
    print(time)