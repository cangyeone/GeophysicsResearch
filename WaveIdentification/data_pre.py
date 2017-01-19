# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 13:42:23 2017

@author: Cangye
"""


from pysac import SacStreamIO
import os
import struct
import numpy as np

def get_dir_list(cdir,suffix='.z'):
    lst=os.walk(cdir)
    for item in lst:
        print("File dir %s is processing...(file total number:%d)"%(item[0],len(item[2])))
        for file in item[2]:
            fdir=os.path.join(item[0],file)
            if(fdir[-2:]==suffix):
                yield fdir

class SacFilePre(SacStreamIO):
    def __init__(self,cdir=os.getcwd(),out_file_name='name',trim_data_len=1024,jitter=10):
        self.cdir=cdir
        self.data_dir=cdir
        self.out_file_name=out_file_name
        self.trim_data_len=trim_data_len
        self.jitter=jitter
        self.pre=100
        self.win_len=700
    def get_pos(self):
        for t in self.tn:
            jit=np.random.randint(self.jitter)
            if(abs(t)<100000 or abs(t)>1000):
                for ii in range(jit):
                    yield t-self.pre+np.random.randint(self.win_len)
    def get_wave_patch(self):
        dfile=os.path.join(self.cdir,self.out_file_name)
        outfile=open(dfile,'w')
        for file in get_dir_list(cdir=self.data_dir):
            SacStreamIO.__init__(self,fileName=file)
            for ps in self.get_pos():
                for dt in self.data:
                    outfile.write(str(dt[ps:ps+self.trim_data_len]))
                outfile.write('\n')
        outfile.close()
        
        
if __name__ == '__main__':
    aa=SacFilePre()
    aa.get_wave_patch()











