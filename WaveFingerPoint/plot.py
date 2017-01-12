# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 14:36:53 2017

@author: LLL
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 20:29:31 2017

@author: LLL
"""
import numpy as np  
import pywt
from scipy.signal import resample
class SacFig():
    def __init__(self,file_name):
        from pysac import SacStreamIO
        import stft
        import numpy as np
        self.hash=[]
        self.wlWinN=100
        self.wlLagN=10
        self.fqWinN=100
        self.fqLagN=50
        self.fqRspN=64
        self.wlRspN=64
        self.max900=0
        self.wl_x_level=3;
        #sac file read
        sac_st=SacStreamIO(file_name)
        sac_st.DataDetrend()
        self.sac_delta=sac_st.delta
        self.sac_data=sac_st.yVect
        print("Sac File Read Finished!")

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
        wmg = WeightedMinHashGenerator(len(self.wlData[0]),sample_size=2, seed=12)
        for tr in self.wlData:
            try:
                wm = wmg.minhash(tr) # wm1 is of the type WeightedMinHash
                vl=np.transpose(wm.hashvalues)
                vl=vl[0]
                self.hash.append(vl.tolist())
            except:
                print(tr)
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
        mu=(np.average(data,axis=1))
        lx=len(mu)
        mu=np.reshape(mu,[lx,1])
        sigma=(np.std(data,axis=1))
        sigma=np.reshape(sigma,[lx,1])
        rdata=np.divide(np.subtract(data,mu),sigma)
        return rdata
    def IterSetZeroRow(self,rowD):
        sort_t=np.sort(np.abs(rowD))
        self.max900=sort_t[15]
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
                    
            
if __name__ == '__main__':
    bits=2
    import time
    import matplotlib.pyplot as plt
    from scipy.signal import resample
    fileName="st26_0826.z"
    st=time.clock()
    a1=SacFig(fileName)
    plt.plot(np.linspace(0,a1.sac_delta*len(a1.sac_data),len(a1.sac_data)),a1.sac_data)
    print("time consumption:%f",ed-st)
    #print(a1.hash)
    #a1.PlotWaveWithFingerPoint(1)
    

    """"""
    
    
    