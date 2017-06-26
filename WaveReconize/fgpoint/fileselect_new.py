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
        if(names[-1]=="hash10"):
            return True
        
class GetTempFile(GetDirFile):
    def NameFunc(self,fileName):
        names=fileName.split(".")
        if(names[-1]=="template10"):
            return True


class Find():
    def __init__(self):
        pass
    def GetFileData(self,name):
        rt=[]
        for itr in open(name,"r").readlines():
            dts=[aa for aa in itr.strip().split(',') if(len(aa)>0)]
            rt.append([float(dts[0]),np.array([int(aa) for aa in dts[1:]])])
        return rt
    def GetIndex(self,names):
        self.index=[]
        for itr in names:
            self.index.append(self.GetFileData(itr))

    def Search(self,hash,level=0.5):
        times=[]
        #print(self.index)
        for itrx in self.index:
            old=0
            for itry in itrx:
                if(len(np.where(hash==itry[1])[0])/len(hash)>level):
                    if(itry[0]-old>5):
                        times.append(itry[0])
                        old=itry[0]
        return times

def trunk():
    HSF=GetHashFile(os.getcwd()+'/').GetList()
    TPF=GetTempFile(os.getcwd()+'/').GetList()
    engine=Find()
    engine.GetIndex(HSF)
    times=engine.Search(np.array([22813171,24130584,12470431,17266034,132721297,173306923,100774281,39951099,27689246,289724735,86101458,75492665,29604049,183910497,45187728,27032361,97663355,7276142,143938973,70629991
                        ]),level=0.45)
    print(times)
if __name__=="__main__":
    trunk()
    
