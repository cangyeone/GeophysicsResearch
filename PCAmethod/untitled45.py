# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 18:11:05 2017

@author: LLL
"""

import numpy as np
import xlwt
f=xlwt.Workbook()
sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
sheet2=f.add_sheet(u'sheet2',cell_overwrite_ok=True)

comp=np.random.random([100,3])
source=np.random.random([3,7])*100

out_data=np.dot(comp,source)


for itry in range(len(out_data)):
    sheet1.write(itry,0,"sp"+str(itry))
    for itrx in range(len(out_data[0])):
        sheet1.write(itry,itrx+1,out_data[itry,itrx])
for itry in range(len(source)):
    sheet2.write(itry,0,"source"+str(itry))
    for itrx in range(len(source[0])):
        sheet2.write(itry,itrx+1,source[itry,itrx])
f.save("data1.xls")        
        
        
        
        
        
        
        
        
        
        
        
        
        