import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

from sklearn.decomposition import FastICA, PCA


class ReadFile():
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
    def __init__(self):
        #self.GetFileData()
        data=[]
        cont=0
        for aa in self.get_dir_list(os.getcwd(),suffix='.sec'):
            data.append(self.GetFileData(aa)[2])
            if(cont>10):
                break
            cont += 1
        data=np.transpose(np.array(data))
        print(data)
        ica = PCA(n_components=3)
        source = ica.fit_transform(data)  # Reconstruct signals
        #A_ = ica.mixing_
        plt.figure(1)
        plt.plot((data))
        plt.figure(2)
        plt.plot((source))
        plt.show()
        #print(np.shape(data))
        #print(np.shape(S_))
    def get_dir_list(self,cdir,suffix='.z'):
        lst=os.walk(cdir)
        sfn=len(suffix)
        for item in lst:
            #print("File dir %s is processing...(file total number:%d)"%(item[0],len(item[2])))
            for file in item[2]:
                fdir=os.path.join(item[0],file)
                if(fdir[-sfn:]==suffix):
                    yield fdir
tt=ReadFile()