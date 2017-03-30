import numpy as np  
import pywt
from scipy.signal import resample
import os

import numpy as np
import matplotlib.pyplot as plt
#为了画图更好看，其实并没有
import matplotlib as mpl
#mpl.style.use('seaborn-darkgrid')
class SacFig():
    def GetFileData(self,file):
        dtFile=open(file,"r")
        dData=dtFile.readlines()
        dtL=0
        for itr in dData:
            dtL=dtL+1
            if(itr[0:4]=="DATE"):
                break
        rtData=[]
        for itr in dData[dtL:]:
            slt=[it for it in itr.split(' ') if(len(it)>0)][3:6]
            sltd=[float(it) for it in slt]
            rtData.append(sltd)
        dtFile.close()
        return np.transpose(np.array(rtData))
    def __init__(self,file_name):
        from pysac import SacStreamIO
        import stft
        import numpy as np
        self.hash=[]
        self.wlWinN=60
        self.wlLagN=6
        self.fqWinN=60
        self.fqLagN=10
        
        self.fqRspN=32
        self.wlRspN=32
        self.max900=0
        self.wl_x_level=3;
        #sac file read
        
        self.sac_st=self.GetFileData(fileName)
        nize=GenData([1,600])
        nzdt=nize.GenWave()
        import scipy.signal as ssg
        for temp_data in self.sac_st[0:1]:
            
            temp_data[3000:3000+600]=temp_data[3000:3000+600]+nzdt[0]
            temp_data[9000:9000+600]=temp_data[9000:9000+600]+nzdt[0]
            self.sac_data=ssg.detrend(temp_data)
            #calcaute stft
            fqData=stft.stft(self.sac_data,self.fqWinN,self.fqLagN,self.fqRspN)
            fqData=np.abs(fqData)
            wlDataX=self.WaveLetX(fqData,level=3)
            self.wlData=self.WaveLetAndRegular(wlDataX,level=3)
            self.wlData=self.RegularY(self.wlData)
            self.wlData=self.TrimData(self.wlData)
            self.GetFingerPoint(2)
    def PlotWaveWithFingerPoint(self,figureNum):
        import matplotlib.pyplot as plt
        plt.figure(figureNum)
        ax1=plt.subplot(1,1,1)
        t_x=np.linspace(0,len(self.sac_data)*self.sac_delta,len(self.sac_data))
        ax1.plot(t_x,self.sac_data,c='k')
        for nn in range(len(self.hash)):
            itv=np.max(t_x)/len(self.hash)
            ax1.text(itv*nn,np.max(self.sac_data)*0.9,"hash:"+str(self.hash[nn]))
            
    def GetFingerPoint(self,hashbit):
        import simhash
        import mynilsimsa
        from datasketch import WeightedMinHashGenerator   
        """
        schar=[]
        for iy in range(len(self.wlData)):
            tsc=[]
            for ix in range(len(self.wlData[0])):
                if(self.wlData[iy,ix]==1):
                    tsc.append('a')
                elif(self.wlData[iy,ix]==-1):
                    tsc.append('c')
                else:
                    tsc.append('d')
            schar.append(tsc)
      
        for cr in schar: 
            hh=simhash.simhash(''.join(cr),hashbits=hashbit)
            self.hash.append(hh.hash)

        """ 
        #"""
        wmg = WeightedMinHashGenerator(len(self.wlData[0]),sample_size=4, seed=12)
        for tr in self.wlData:
            
            wm = wmg.minhash(tr) # wm1 is of the type WeightedMinHash
            vl=np.transpose(wm.hashvalues)
            vl=vl[0]
            self.hash.append(vl.tolist())
        #""" 
    def IterWaveLetX(self,dt):
        rw=pywt.wavedec(dt,'haar',level=self.wl_x_level)
        rw=np.concatenate(rw)
        return rw
    def WaveLetX(self,data,level=3):
        rta=map(self.IterWaveLetX,data)
        rta=np.array(list(rta))
        return rta
        
    def WaveLetAndRegular(self,data,level=3):
        def IterWaveFram(itf):
            fram=data[itf:itf+self.wlWinN,:]
            fram=resample(fram,self.wlRspN)
            fram=np.transpose(fram)
            wlFram=np.transpose(self.WaveLetX(fram,3))
            wlFramL=np.reshape(wlFram,[-1])
            wlFramL2=np.sum(np.square(wlFramL))
            wlFramL=np.divide(wlFramL,wlFramL2)
            return wlFramL
        rData=list(map(IterWaveFram,range(0,len(data)-self.wlWinN,self.wlLagN)))

        return (np.array(rData))
    def RegularY(self,data):
        mu=np.transpose(np.average(data,axis=0))
        sigma=np.transpose(np.std(data,axis=0))
        rdata=np.divide(np.subtract(data,mu),sigma)
        return rdata
    def IterSetZeroRow(self,rowD):
        sort_t=np.sort(np.abs(rowD))
        self.max900=sort_t[self.fqRspN*self.wlRspN-300]
        #print(self.max900)
        return list(map(self.IterSetZeroCol,rowD))
    def IterSetZeroCol(self,colD):
        if(np.abs(colD)<self.max900):
            return 0
        elif(np.abs(colD)>=self.max900 and colD>0):
            return 1
        else:
            return -1        
    def TrimData(self,data):
        trip_data=list(map(self.IterSetZeroRow,data))
        return np.array(trip_data)

def GetSecFile(tag=".sec"):
    itrlist=os.walk(os.getcwd())
    sacFile=[]
    for itr in itrlist:
        for it in itr[2]:
            if(it[-4:]==tag):
                sacFile.append(itr[0]+"\\"+it)
    return sacFile              



class MergeFile():
    def Group(self,st,lvl):
        rdata=[]
        ch=st[0][lvl]
        nw=[]
        for itr in st:
            if(itr[lvl]==ch):
                nw.append(itr)
            else:
                rdata.append(nw)
                nw=[]
                nw.append(itr)
            ch=itr[lvl]
        return rdata
    def __init__(self,hash_data):                
        print("Grouping data:")
        for itr in range(len(hash_data)):
            hash_data[itr].append(itr)
        
        #self.sdata=sorted(hash_data,key=lambda x:(x[0]))
        self.sgdata=[hash_data]
        for itr in range(len(hash_data[0])-1):
            tdt=[]
            ssm=0
            for tsg in self.sgdata:
                st_data=sorted(tsg,key=lambda x:(x[itr]))
                ssm=ssm+len(st_data)
                tdt.extend(self.Group(st_data,itr))
            self.sgdata=tdt
            print(len(self.sgdata))
            print(ssm)
    def GetData(self):
        rtdt=[]
        for itrx in self.sgdata:
            for itry in itrx:
                rtdt.append(itry)
        return rtdt
    def GetDataANO(self):
        rtdt=[]
        for itrx in self.sgdata:
            if(len(itrx)>1):
                continue
            for itry in itrx:
                rtdt.append(itry)
        return rtdt
class GenData():
    def __init__(self,shape=[1,1]):
        self.shape=shape
        self.data=np.zeros(self.shape)
    def GenWave(self,numSubWave=30):
        
        #data=np.random.random(shape)
        #data=np.subtract(data,0.5)
        ariv=np.zeros([self.shape[0],1])
        if(numSubWave==0):
            return self.data      
        for itrd in range(self.shape[0]):
            sbn=1+np.random.randint(numSubWave)
            for itr in range(sbn):
                f0=0.3
                Tc=1
                per=300
                t=np.linspace(0,1,per)
                wave=(1+np.cos(2.*np.pi*(t-Tc/2.)/Tc))*np.cos(2.*np.pi*f0*(t-Tc/2.))/2.
                nba=np.random.randint(self.shape[1]-per-1)
                ariv[itrd][0]=1
                self.data[itrd,nba:nba+per]=self.data[itrd,nba:nba+per]+wave
        mx=np.max(self.data,axis=1)
        mx=np.reshape(mx,[-1,1])
        self.data=np.multiply(np.divide(self.data,mx),10)
        #return ariv
        #self.data=self.data+np.random.random(1)[0]*0.5-0.25
        return self.data
    def AddNoise(self,bl=0.5,tp='FX'):
        noise=np.random.random(self.shape)
        noise=np.subtract(noise,0.5)
        if(tp=='RD'):
            bl=np.random.random(1)[0]*bl+0.0001
        noise=np.multiply(noise,bl)
        return np.add(self.data,noise)
        
def PrintDT1(file,lgt,hdT):
    sc=0
    for it in hdT:
        sc+=1
        tm=lgt*sc
        outFile.write("%d,"%(tm))
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
    scFile=GetSecFile()
    for fileName in scFile:
        st=time.clock()
        a1=SacFig(fileName)
        outFile=open(fileName+"_hash_file.txt","w")
        sc=0
        hdT=a1.hash

        PrintDT1(outFile,a1.fqLagN*a1.wlLagN,hdT)
        ed=time.clock()
        outFile.flush()
        print("time consumption:%f",ed-st)

        

    
    
    
