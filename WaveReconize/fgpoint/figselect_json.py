
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

    cont=0
    outFile=open("dt2.json","w")

    outFile.write('{')
    outFile.write('\"nodes\":')
    outFile.write('[')

    idx_pt=[]
    unqtime_pt=[]
    time_cont_pt={}
    file_cont_pt={}
    lk_f_h={}
    lk_h_t={}
    for xx in TP:
        cont+=1
        outFile.write("{\"name\":\"file%d\"},\n"%(cont))
        lk_f_h["file%d"%cont]={"idx":[],"cont":{}}
        for yy in xx[6:50]:
            try:
                if(len(idx[0][yy[1]][yy[2]])>15):
                    continue
                if(len(idx[0][yy[1]][yy[2]])<1):
                    continue
                if(("[%s,%s]"%(yy[1],yy[2]) in idx_pt)==False):
                    idx_pt.append("[%s,%s]"%(yy[1],yy[2]))
                    outFile.write("{\"name\":\"[%s,%s]\"},\n"%(yy[1],yy[2]))
                    lk_h_t["[%s,%s]"%(yy[1],yy[2])]={"time":[]}
                if(("[%s,%s]"%(yy[1],yy[2]) in lk_f_h["file%d"%cont]["idx"])==False):
                    lk_f_h["file%d"%cont]["idx"].append("[%s,%s]"%(yy[1],yy[2]))
                    lk_f_h["file%d"%cont]["cont"]["[%s,%s]"%(yy[1],yy[2])]=0
                for itr in idx[0][yy[1]][yy[2]]:
                    if((itr in lk_h_t["[%s,%s]"%(yy[1],yy[2])]["time"])==False):
                        lk_h_t["[%s,%s]"%(yy[1],yy[2])]["time"].append(itr)
                        lk_f_h["file%d"%cont]["cont"]["[%s,%s]"%(yy[1],yy[2])]+=1
                        #lk_h_t["[%s,%s]"%(yy[1],yy[2])]["time"].append(itr)
                    if((itr in unqtime_pt)==False):
                        unqtime_pt.append(itr)
                        outFile.write("{\"name\":\"time:%.2f\"},\n"%(itr))
                        lk_f_h["file%d"%cont]["cont"]+=1
                        if(time_cont_pt.get("[%s,%s]"%(yy[1],yy[2]))==None):
                            time_cont_pt["[%s,%s]"%(yy[1],yy[2])]=0
                        else:
                            time_cont_pt["[%s,%s]"%(yy[1],yy[2])]+=1
                        if(file_cont_pt.get("file%d"%(cont))==None):
                            file_cont_pt["file%d"%(cont)]={}
                            file_cont_pt["file%d"%(cont)]["[%s,%s]"%(yy[1],yy[2])]=1
                        else:
                            if(file_cont_pt["file%d"%(cont)].get("[%s,%s]"%(yy[1],yy[2]))==None):
                                file_cont_pt["file%d"%(cont)]["[%s,%s]"%(yy[1],yy[2])]=1
                            else:
                                file_cont_pt["file%d"%(cont)]["[%s,%s]"%(yy[1],yy[2])]+=1                            
            except:
                pass
    outFile.seek(outFile.tell()-3)
    outFile.write('],')
    outFile.write('\"links\":')
    outFile.write('[')
    cont=0
    print(lk_f_h)
    print(lk_h_t)
    for xx in lk_f_h:
        for yy in lk_f_h[xx]["idx"]:
            if(lk_f_h[xx]["cont"][yy]==0):
                continue
            else:
                outFile.write("{ \"source\":\"%s\",\"target\":\"%s\",\"value\":%f },\n"
                        %(xx,yy,lk_f_h[xx]["cont"][yy]))

    for xx in lk_h_t:
        for yy in lk_h_t[xx]['time']:
            outFile.write("{ \"source\":\"%s\",\"target\":\"time:%.2f\",\"value\":%f },\n"
                        %(xx,yy,1))
    outFile.seek(outFile.tell()-3)
    outFile.write(']')
    outFile.write('}')
    outFile.close()
    print(tm)