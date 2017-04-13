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
            self.complete()
            
        else:
            self.driver=driver
            print('testmode')
    def getarticleinfo(self,soup_t):
        for itr in soup_t.find_all('div',class_='sc_quote_list_item_r'):
            return(itr.string)
                
    def autofill(self,question_word):
        wd=urllib.request.quote(question_word).replace('%2B','+')
        url="http://xueshu.baidu.com/s?wd=%s"%(wd)
        url=url+"&tn=SE_baiduxueshu_c1gjeupa&cl=3&ie=utf-8&bs=seismic+%E5%AD%A6%E6%9C%AF&f=8&rsv_bp=1&rsv_sug2=0&sc_f_para=sc_tasktype%3D%7BfirstSimpleSearch%7D&rsv_spt=3"
        
        opener = urllib.request.build_opener()
        headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        opener.addheaders = [headers]
        htmlpage =opener.open(url).read()
        #print(htmlpage)
        soup = BeautifulSoup(htmlpage,'html.parser')
        sig=soup.find_all('div',id='top_hint')
        
        if(len(sig)!=0):
            self.driver.get(url)
            self.driver.find_element_by_class_name('sc_q').click()
            #print(driver.page_source)
            time.sleep(1)
            soup=BeautifulSoup(self.driver.page_source,'html.parser')
            atinfo=self.getarticleinfo(soup)
        else:
            for link in soup.find_all('a'):
                newwd=link.get('href')
                if(newwd[:14]=="/s?wd=paperuri"):
                    newurl="http://xueshu.baidu.com"+newwd.replace('amp;','')
                    self.driver.get(newurl)
                    self.driver.find_element_by_class_name('sc_q').click()
                    time.sleep(1)
                    newsoup = BeautifulSoup(self.driver.page_source,'html.parser')
                    atinfo=self.getarticleinfo(newsoup)
                    break
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
                full_info.append(self.autofill(name))
                print("Finished:"+at_name)
            except:
                full_info.append(' ')
                print('File Err:'+at_name)
        self.write2file(full_info)

        
if __name__ == '__main__':
    inFile=input('输入文件名：')
    outFile=input('输出文件名：')
    driv=webdriver.PhantomJS(executable_path='./bin/phantomjs.exe')
    art=Article(inFile,outFile,driver=driv)

  