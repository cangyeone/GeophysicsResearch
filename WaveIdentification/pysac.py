# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:39:10 2016
@author: Cangye
"""

#SAC File Read



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
        matplotlib.use('Agg')  
        import matplotlib.pyplot as plt

        SacStreamIO.__init__(self,fileName)
        self.DataDetrend()#去除线性趋势
        self.ViewHeadData()
        self.ViewData()
        #plt.plot(self.xVect,self.yVect,color='k')
        cont=0
        cr_time_st=0
        for dt in hashDot:
            if(dt[1]==451 and dt[2]==1728 and dt[3]==155 and dt[4]==1063):
                cont+=1
                continue
            cont=0
            cr_time=int(dt[0]*100)
            #if((cr_time-cr_time_st)<19*100):
               # continue
            plt.clf()
            plt.plot(self.xVect[cr_time:cr_time+2000],self.yVect[cr_time:cr_time+2000])
            plt.annotate('Look',xy = (dt[0],0),xytext = (dt[0],500),arrowprops = dict(facecolor = 'black', shrink = 0.1))
            plt.savefig('save_fig_sums5/'+str(dt[5])+'_'+str(int(cr_time/100)))
            cr_time_st=cr_time
            #plt.annotate('Look',xy = (dt[0],max(self.yVect)*0.5)), xytext = (dt[0],max(self.yVect)*0.5)+5),arrowprops = dict(facecolor = 'black', shrink = 0.1))
            #plt.text(dt[0],0,'LOOK!!')
        #plt.text(0,max(self.yVect)*0.5,'year:'+str(self.year)+'\nlongitude:'+str(self.lon)+'\nlatitude:'+str(self.lat))


        
if __name__ == '__main__':
    import os
    from datasketch import WeightedMinHashGenerator 
    v1 = [1, 3, 4, 5, 6, 7, 8, 9, 10, 4]
    v2 = [1, 3, 4, 5, 2, 3, 8, 9, 10, 4]
    fileName="st26_0826.z"
    wmg = WeightedMinHashGenerator(len(v1),sample_size=4, seed=12)
    wm1 = wmg.minhash(v1) # wm1 is of the type WeightedMinHash
    wm2 = wmg.minhash(v2)
    fileDot=open("st26_0826.zhash.hh")

    fileDt=fileDot.readlines()
    data=[]
    for aa in fileDt:
        data.append([float(ii.strip()) for ii in aa.split(',')])
    tripDt=[[1,1,1,1,1]]
    style=0
    cont=0
    for dt in data:
        cct=0
        wm1.hashvalues=[[dt[1],0],[dt[2],0],[dt[3],0],[dt[4],0]]
        for td in tripDt:
            wm2.hashvalues=[[td[1],0],[td[2],0],[td[3],0],[td[4],0]]
            if(wm2.jaccard(wm1)>0.5):
                cct=1
                data[cont].append(td[5])
                cont+=1
                break
        if(cct==1):
            continue
        style+=1
        tripDt.append([dt[0],dt[1],dt[2],dt[3],dt[4],style])
        data[cont].append(style)
        cont+=1
    os.makedirs('save_fig_sums5/')
    SacPlot(fileName,data) 
        
        
        
        
        
        
        
        
        
        
        
        
    