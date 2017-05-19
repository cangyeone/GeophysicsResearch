# -*- coding: utf-8 -*-
"""
Created on Thu May 18 15:51:51 2017

@author: LLL
"""
import sys


file=open("test.txt","w")
print(sys.argv)
file.write(sys.argv[1])
file.close()