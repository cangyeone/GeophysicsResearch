# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 10:00:37 2017

@author: LLL
"""

import os
dirs=os.walk(os.getcwd())
strs=""
for itrx in dirs:
    for itry in itrx[2]:
        if(itry[-1]=="g"):
           strs+="\'<img src=\"fgpictures/%s\" />\',"%(itry)
print(strs)