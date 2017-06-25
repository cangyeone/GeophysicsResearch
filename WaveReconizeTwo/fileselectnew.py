
from getdir import *
import os
import matplotlib.pyplot as plt
import numpy as np
import time as tm
from obspy import read as pread
from obspy import Stream
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
class Select():
    def __init__(self,idxFile,hashFile):
        self.idxFile=idxFile
        self.hashFile=hashFile
    def GetTempFile(self):
        self.temp=[]
        #self.hash=[]
        for xx in self.idxFile:
            ff=[]
            for yy in open(xx).readlines():
                datas=[aa for aa in yy.strip().split(",") if len(aa)>0]
                #ff.append(float(datas[0]))
                ff.append([float(datas[0]),
                    np.array([int(aa) for aa in datas[1:]])])
            self.temp.append(ff)
    def GetHashFile(self):
        #self.temp=[]
        self.hash=[]
        for xx in self.hashFile:
            ff=[]
            for yy in open(xx).readlines():
                datas=[aa for aa in yy.strip().split(",") if len(aa)>0]
                ff.append([float(datas[0]),
                    np.array([int(aa) for aa in datas[1:]])])
            self.hash.append(ff)
    def GetTime(self):
        #print(self.hash[0])
        time=[]
        for xx in self.hash[0]:
            old=0
            for yy in self.temp:
                for zz in yy[:4]:
                    if(len(np.where(zz[1]==xx[1])[0])/len(zz[1])>0.5):
                        if(xx[0]-old>5):
                            time.append(xx[0])
                            old=xx[0]
        return time
    def Find(self,hh):
        time=[]
        d=float(len(hh))
        old=0
        for xx in self.hash[0]:
            #print(len(np.where(xx[1]==hh)[0])/d)
            if(len(np.where(xx[1]==hh)[0])/d>0.45):
                #print(xx[0]-old)
                if(xx[0]-old>5):
                    time.append(xx[0])
                    old=xx[0]
        return time
from obspy import read as pread

def trunk():
    HSF=GetHashFile(os.getcwd()+'/').GetList()
    TPF=GetTempFile(os.getcwd()+'/').GetList()
    mysel=Select(TPF,HSF)
    mysel.GetHashFile()
    mysel.GetTempFile()
    #tm=mysel.GetTime()
    #print(tm)
    #return
    files=[DIR+"s28/2015337/2015337_00_00_00_s28_BHE.SAC",
                    DIR+"s28/2015337/2015337_00_00_00_s28_BHN.SAC",
                    DIR+"s28/2015337/2015337_00_00_00_s28_BHZ.SAC"]
    st=Stream()
    dt=[]
    for file in files:
        st=pread(file)
        dt.append(st[0].data)
    #tm=mysel.Find(np.array([22813171,127266168,12470431,17266034,132721297,6361937,30551886,56546867,27689246,235320713,86101458,93624353,13858394,49972221,103683464,31376115,104910045,64306427,143938973,121058633]))
    tm=mysel.Find(np.array([22813171,24130584,12470431,17266034,132721297,173306923,100774281,39951099,27689246,289724735,86101458,75492665,29604049,183910497,45187728,27032361,97663355,7276142,143938973,70629991]))
    print(tm)
    #return
    fig=plt.figure()
    timelen=300
    jsfile=open("D:/xampp/htdocs/data/data_plot.json","w")
    
    jsfile.write("{\"timeseries\":[")
    for itr in tm:
        jsfile.write("%d,"%int(itr))
    jsfile.seek(jsfile.tell()-1)
    jsfile.write("],\n")
    jsfile.write("\"datas\":[")
    for itr in tm:
        itr=int(itr*100)
        jsfile.write("[[")
        for itry in range(timelen):
            jsfile.write("[%f,%f],"%((itry)/100,dt[0][itr+itry]))
        jsfile.seek(jsfile.tell()-1)
        jsfile.write("],\n[")
        for itry in range(timelen):
            jsfile.write("[%f,%f],"%((itry)/100,dt[1][itr+itry]))
        jsfile.seek(jsfile.tell()-1)
        jsfile.write("],\n[")
        for itry in range(timelen):
            jsfile.write("[%f,%f],"%((itry)/100,dt[2][itr+itry]))
        jsfile.seek(jsfile.tell()-1)
        jsfile.write("]],\n")
    
        #name="selfig/"+("%.2f"%(itr/100))+".jpg"
        #fig.clf()
        #ax=fig.add_subplot(311)
        #ax.plot(dt[0][itr:itr+timelen])
        #ax=fig.add_subplot(312)
        #ax.plot(dt[1][itr:itr+timelen])
        #ax=fig.add_subplot(313)
        #ax.plot(dt[2][itr:itr+timelen])
        #plt.savefig(name)
    jsfile.seek(jsfile.tell()-3)
    jsfile.write("]}")
    jsfile.close()

if __name__=="__main__":
    trunk()