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
        self.Art=[]
        if(TestMode==False):
            self.inFile=inFile
            self.outFile=outFile
            self.driver=driver
            self.complete()

        else:
            self.driver=driver
            print('testmode')
    def getarticleinfo(self,newurl):
        self.driver.get(newurl)
        self.driver.find_element_by_class_name('sc_q').click()
        time.sleep(1)
        newsoup = BeautifulSoup(self.driver.page_source,'html.parser')
        tatinfo=self.getarticleinfo(newsoup)
        for itr in newsoup.find_all('div',class_='sc_quote_list_item_r'):
            print(itr.string)
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
        #print(soup)
        atinfo=[]
        if(len(sig)!=0):
            #atinfo.append(self.getarticleinfo(url))
            self.get_reference(0,url)
        else:
            for divs in soup.find_all('div',class_='sc_content'):
                for link in divs.find_all('a'):
                    newwd=link.get('href')
                    #print(newwd)
                    if(newwd[:14]=="/s?wd=paperuri"):
                        newurl="http://xueshu.baidu.com"+newwd.replace('amp;','')
                        self.get_reference(0,newurl)
        return atinfo
    def get_reference(self,deep,newurl):
        try:
            self.driver.get(newurl)
        except:
            print("err div")
            return
        if(deep>2):
            return
        time.sleep(0.1)
        try:
            self.driver.find_element_by_class_name('request_situ').click()
        except:
            self.driver.find_element_by_class_name('dl_more OP_LOG_BTN more_btn').click()
        time.sleep(1)
        newsoup = BeautifulSoup(self.driver.page_source,'html.parser')
        for itr in newsoup.find_all('ul',class_="citation_lists"):
            for itra in itr.find_all('a',class_="relative_title"):
                newwd=itra.get("href")
                nexturl="http://xueshu.baidu.com"+newwd.replace('amp;','')
                self.Art.append([deep,itra.string])
                try:
                    self.get_reference(deep+1,nexturl)
                except:
                    print("err")
                    return 
                if(deep==0):
                    print(itra.string)
                #artinfo=self.getarticleinfo(nexturl)
                #print(nexturl)
                #print(itra.string)
                #needed to be del
                #break
                       
    def write2file(self,buf):
        file=open(self.outFile,"w")
        for itr in self.Art:
            try:
                file.write("    "*itr[0]+itr[1]+'\n')
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
                full_info.append(self.autofill(name))
                print('File Err:'+at_name)
        self.write2file("None")

        
if __name__ == '__main__':
    inFile=input('输入文件名：')
    outFile=input('输出文件名：')
    #inFile='a.txt'
    #outFile='out.txt'
    driv=webdriver.PhantomJS(executable_path='./bin/phantomjs.exe')
    art=Article(inFile,outFile,driver=driv)
    from os import path  
    from scipy.misc import imread  
    import matplotlib.pyplot as plt  
    import jieba  
    
    from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator  
    
    stopwords = {}  
    def importStopword(filename=''):  
        global stopwords  
        f = open(filename, 'r')  
        line = f.readline().rstrip()  
    
        while line:  
            stopwords.setdefault(line, 0)  
            stopwords[line] = 1  
            line = f.readline().rstrip()  
    
        f.close()  
    
    def processChinese(text):  
        seg_generator = jieba.cut(text)  # 使用结巴分词，也可以不使用  
    
        seg_list = [i for i in seg_generator if i not in stopwords]  
    
        seg_list = [i for i in seg_list if i != u' ']  
    
        seg_list = r' '.join(seg_list)  
    
        return seg_list  
    d = path.dirname(__file__)  
    
    
    text = open(outFile,"r").read()  
    text=processChinese(text)
    wc = WordCloud( font_path='./font/叶立群几何体.ttf',#设置字体
                width=1980,
                height=1080,
                background_color="white", #背景颜色
                #max_words=2000,# 词云显示的最大词数
                #mask=back_coloring,#设置背景图片
                #max_font_size=100, #字体最大值
                random_state=42,
                )
    #WordCloud()
    wc.generate(text)  
    plt.figure() 
    print(wc)
    import numpy as np
    print(np.shape(wc))
    plt.imshow(wc)
    plt.axis("off")  
    plt.show()  
    wc.to_file(path.join(d, "名称.png")) 