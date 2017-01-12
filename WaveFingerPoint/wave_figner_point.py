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
        self.fqWinN=1000
        self.fqLagN=10
        self.fqRspN=32
        self.wlRspN=64
        #sac file read
        sac_st=SacStreamIO(file_name)
        sac_st.DataDetrend()
        self.sac_delta=sac_st.delta
        self.sac_data=sac_st.yVect
        print("Sac File Read Finished!")
        #calcaute stft
        fqData=stft.stft(self.sac_data,self.fqWinN,self.fqLagN,self.fqRspN)
        fqData=np.abs(fqData)
        print("STFT Trans Finished!")
        wlDataX=self.WaveLetX(fqData,level=3)
        self.wlData=self.WaveLetAndRegular(wlDataX,level=3)
        print("Wavelet Trans Finished!")
        self.wlData=self.RegularY(self.wlData)
        print("Regular Finished!")
        self.TrimData(self.wlData)
        print("Bit Trans Finished!")
        self.GetFingerPoint(2)
        print("Hash Trans Finished!")
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
            
            wm = wmg.minhash(tr) # wm1 is of the type WeightedMinHash
            vl=np.transpose(wm.hashvalues)
            vl=vl[0]
            self.hash.append(vl.tolist())
        #""" 
           
    def WaveLetX(self,data,level=3):
        rdata=[]
        for row in data:
            rws=np.array([])
            rw=pywt.wavedec(row,'haar',level=level)
            for trans in range(len(rw)):
                rws=np.append(rws,rw[trans])
            rdata.append(rws)
        rta=np.array(rdata)
        return rta
        
    def WaveLetAndRegular(self,data,level=3):
        rdata=[]
        for itf in range(0,len(data)-self.wlWinN,self.wlLagN):
            fram=data[itf:itf+self.wlWinN,:]
            fram=resample(fram,self.wlRspN)
            fram=np.transpose(fram)
            wlFram=np.transpose(self.WaveLetX(fram,3))
            wlFramL=np.reshape(wlFram,[-1])
            wlFramL2=np.sum(np.square(wlFramL))
            wlFramL=np.divide(wlFramL,wlFramL2)
            rdata.append(wlFramL)
        return (np.array(rdata))
    def RegularY(self,data):
        mu=np.transpose(np.average(data,axis=0))
        sigma=np.transpose(np.std(data,axis=0))
        rdata=np.divide(np.subtract(data,mu),sigma)
        return rdata
          
    def TrimData(self,data):
        dN=len(data)
        rN=len(data[0])
        for row in range(dN):
            sort=np.sort(np.abs(data[row]))
            max900=sort[self.fqRspN*self.wlRspN-900]
                
            for dt in range(rN):
                if(np.abs(data[row,dt])<max900):
                    data[row,dt]=0
                elif(np.abs(data[row,dt])>=max900 and data[row,dt]>0):
                    data[row,dt]=1
                else:
                    data[row,dt]=-1
                    
                    
            
if __name__ == '__main__':
    bits=2
    import time
    fileName="st26_0826.z"
    st=time.clock()
    a1=SacFig(fileName)
    outFile=open(fileName+"_min_2_no_map.hash","w")
    for it in range(len(a1.hash)):
        sc=it*a1.sac_delta*a1.fqLagN*a1.wlLagN
        #outFile.write("%f,%d,%d,%d,%d\n"%(sc,a1.hash[it][0],a1.hash[it][1],a1.hash[it][2],a1.hash[it][3]))
        #outFile.write("%f,%d\n"%(sc,a1.hash[it]))
        outFile.write("%f,%d,%d\n"%(sc,a1.hash[it][0],a1.hash[it][1]))
    ed=time.clock()
    outFile.flush()
    print("time consumption:%f",ed-st)
    #print(a1.hash)
    #a1.PlotWaveWithFingerPoint(1)
    

    """"""
    
    
    