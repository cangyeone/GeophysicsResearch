
from getdir import *
import os
import matplotlib.pyplot as plt
import numpy as np

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

gtf=GetTempFiles()
st=Stream()
for itr in gtf:
        #print(itr)
        st+=pread(itr[1])
        break
plt.plot(st[0].data)
plt.show()
#st.plot()
