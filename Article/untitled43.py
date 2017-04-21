# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 08:48:49 2017

@author: Cangye@hotmail.com
"""

import urllib
from bs4 import BeautifulSoup
import xlwt
from selenium import webdriver
import os
import time
from selenium.webdriver.common.keys import Keys 
class Article():
    def __init__(self,inFile=None,outFile=None,driver=None,TestMode=False):
        if(TestMode==False):
            self.inFile=inFile
            self.outFile=outFile
            self.driver=driver
            self.autofill()
            
        else:
            self.driver=driver
            print('testmode')
    def getarticleinfo(self,soup_t):
        for itr in soup_t.find_all('div',class_='sc_quote_list_item_r'):
            return(itr.string)
                
    def autofill(self):
        #wd=urllib.request.quote(question_word).replace('%2B','+')
        url="http://weibo.com/1100856704/EFlle0mtg?filter=hot&root_comment_id=0&type=comment"
        
        if(0==0):
            self.driver.get(url)
            #self.driver.find_element_by_class_name('sc_q').click()
            #print(driver.page_source)
            #time.sleep(1)
            print(self.driver.page_source)
            soup=BeautifulSoup(self.driver.page_source,'html.parser')
            atinfo=self.getarticleinfo(soup)

        return atinfo
        
    def write2file(self,buf):
        file=open(self.outFile,"w")
        for itr in buf:
            try:
                file.write(itr+'\n')
            except:
                file.write('\n')
        file.close()
    def complete(self):
        file=open(self.inFile,"r")
        text=file.readlines()
        full_info=[]
        for at_name in text:
            name=at_name.strip()
            try:
                full_info.append(self.autofill())
                print("Finished:"+at_name)
            except:
                full_info.append(' ')
                print('File Err:'+at_name)
        self.write2file(full_info)
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#obj = webdriver.PhantomJS(executable_path='C:\Python27\Scripts\phantomjs.exe',desired_capabilities=dcap) 
        
if __name__ == '__main__':

    dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置userAgent
    dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:25.0) Gecko/20100101 Firefox/25.0 ")
 
    driv=webdriver.PhantomJS(executable_path='./bin/phantomjs.exe',desired_capabilities=dcap)
    driv.add_cookie({
    'name':     'some name here',   
    'value':    'some hash here',
    'domain':   'ea.some domain here.com',         
    'path':     './',
    'httponly': False,
    'secure':   False,
    'expires':  (10000 * 60 * 60) }
            )
    art=Article(driver=driv)

  