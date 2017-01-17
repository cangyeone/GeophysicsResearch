# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 13:42:23 2017

@author: Cangye
"""


from pysac import SacStreamIO
import os
import struct


def get_dir_list(cdir,suffix='.z'):
    lst=os.walk(cdir)
    for item in lst:
        print("File dir %s is processing...(file total number:%d)"%(item[0],len(item[2])))
        for file in item[2]:
            fdir=os.path.join(item[0],file)
            if(fdir[-2:]==suffix):
                yield fdir

class SacFilePre(SacStreamIO):
    def __init__(self,cdir=os.getcwd(),out_file_name='name'):
        self.cdir=cdir
        self.data_dir=cdir
        self.out_file_name=out_file_name
    def get_pos(self):
        for t in self.tn:
            yield 100
    def get_wave_patch(self,out_file_name):
        dfile=os.path.join(self.cdir,out_file_name)
        outfile=open(dfile,'w')
        for file in get_dir_list(cdir=self.data_dir):
            SacStreamIO.__init__(self,fileName=file)
            for ps in self.get_pos():
                for dt in self.data:
                    outfile.write(str(dt[ps:ps+100]))
                outfile.write('\n')
        outfile.close()

aa=SacFilePre()
aa.get_wave_patch('out')











