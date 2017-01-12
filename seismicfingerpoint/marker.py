# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:39:10 2016
@author: Cangye
"""

#SAC File Read

"""
============= =========== ===================
头段区          第一数据区     第二数据区（可选）
============= =========== ===================
起始字: 0       起始字：158   起始字：158+NPTS
长度(字): 158   长度：NPTS   长度: NPTS
内容见下表       -因变量      -自变量(非等间隔数据)
           -振幅        -相位
           -实部        -虚部
============= =========== ===================
"""

import struct
class SacStreamIO():
    def __init__(self,fileName,mode="rb"):
        self.HRN=0
        self.GDN=0
        self.file=open(fileName,mode)
        self.ReadHead()
        self.ReadData()
        self.file.close()
    def ReadHead(self):
        self.file.seek(0,0)
        self.fileHeadB=self.file.read(632)
        out=self.head=struct.unpack('<70f40i24q',self.fileHeadB)
        self.b=out[5]
        self.e=out[6]
        self.delta=out[0]
        self.npts=out[79]
        self.leven=out[105]
        self.nxsize=out[82]
        self.nysize=out[83]
        self.year=out[70]
        self.day=out[70] 
        self.HRN=1
        self.lat=out[31]
        self.lon=out[32]

    def ReadData(self):
        if(self.GDN==1):
            print('Data has read twice!')
            return
        import numpy as np
        if(self.leven==1):
            dataBy=self.file.read(4*self.npts)
            self.yVect=np.array(struct.unpack('<'+str(self.npts)+'f',dataBy))
            self.xVect=np.linspace(0,self.npts*self.delta,self.npts)
        elif(self.leven==0):
            dataBx=self.file.read(4*self.npts)
            dataBy=self.file.read(4*self.npts)
            self.xVect=np.array(struct.unpack('<'+str(self.npts)+'f',dataBx))
            self.yVect=np.array(struct.unpack('<'+str(self.npts)+'f',dataBy))
        self.GDN=1
    def DataDetrend(self):
        import scipy.signal as ssg
        self.yVect=ssg.detrend(self.yVect)
    def ViewHeadData(self):
        for ii in range(14):
            ii5=ii*5
            print("Line %2d :%16.3f %16.3f %16.3f %16.3f %16.3f"%(ii,self.head[ii5],self.head[ii5+1],self.head[ii5+2],self.head[ii5+3],self.head[ii5+4]))
        for ii in range(14,24):
            ii5=ii*5
            print("Line %2d :%16d %16d %16d %16d %16d"%(ii,self.head[ii5],self.head[ii5+1],self.head[ii5+2],self.head[ii5+3],self.head[ii5+4]))
        for ii in range(24,32):
            ii5=ii*3
            print("Line %2d :%16d %16d %16d"%(ii,self.head[ii5],self.head[ii5+1],self.head[ii5+2]))
    def ViewData(self):
        print("%10.3f %10.3f %10.3f\n...(%d dots)...\n%10.3f %10.3f %10.3f"%(self.yVect[0],self.yVect[1],self.yVect[2],self.npts,self.yVect[-3],self.yVect[-2],self.yVect[-1]))

class SacPlot(SacStreamIO):
    def __init__(self,fileName,hashDot):
        import matplotlib  

        import matplotlib.pyplot as plt

        SacStreamIO.__init__(self,fileName)
        self.DataDetrend()#去除线性趋势
        self.ViewHeadData()
        self.ViewData()
        plt.plot(self.xVect,self.yVect,color='k')
        cont=0
        cr_time_st=0
        for dt in hashDot:
            cr_time=int(dt[0]*100)
            #if((cr_time-cr_time_st)<19*100):
               # continue
           
            plt.annotate('Look',xy = (dt[0],0),xytext = (dt[0],500),arrowprops = dict(facecolor = 'black', shrink = 0.1))
           
            
def findExist(lst,a):
    ls=len(a)
    for itr in lst[0:1]:
        sm=0
        for ii in range(1,ls,1):
            
            if(a[ii]==itr[ii]):
                sm+=1
        if(sm==2):
            return 1
    return 0
        
if __name__ == '__main__':
    import os
    from datasketch import WeightedMinHashGenerator 

    fileDot=open("st26_0826.z_hash_file.txt")
    fileMap=open("st02_cut.z_min_2_4.txt")
    fileDt=fileDot.readlines()
    fileMp=fileMap.readlines()
    data=[]
    mData=[]
    for aa in fileDt:
        data.append([float(ii.strip()) for ii in aa.split(',')])
    for aa in fileMp:
        mData.append([float(ii.strip()) for ii in aa.split(',')])
    needV=[]
    for dt in data[:10000]:
        cct=0
        nd=0
        if(findExist(mData,dt)==1):
            needV.append(dt)

    print(len(needV))
    SacPlot("st26_0826.z",needV) 
        
        
        
        
        
        
        
        
        
        
        
        
    