# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 08:48:49 2017

@author: Cangye@hotmail.com
"""

#import urllib2
from bs4 import BeautifulSoup
import xlwt
from selenium import webdriver
import os
import imghdr
import time
import urllib
from selenium.webdriver.common.keys import Keys 
class Article():
    def __init__(self,inFile=None,outFile=None,driver=None,TestMode=False):
        self.file=open("test.txt","w")
        self.autofill()
        print("finish")
    def getarticleinfo(self,soup_t):
        for itr in soup_t.find_all('div',class_='sc_quote_list_item_r'):
            return(itr.string)
    
    def get_article(self,soup):
        for ctc in soup.find_all(['h1','h2','h3','h4','p','li','img']):
            if(ctc.string!=None):
                if(ctc.name=='h2'):
                    try:
                        #self.file.write("#### "+ctc.string+"\n")
                        self.file.write('\n')
                    except:
                        None
                if(ctc.name=='h4'):
                    try:
                        self.file.write(ctc.string+"\n")
                        self.file.write(":"*len(ctc.string)+"\n")
                    except:
                        None
                if(ctc.name=='p'):
                    try:
                        self.file.write(ctc.string+"\n")
                    except:
                        None
                if(ctc.name=='li'):
                    try:
                        self.file.write("* "+ctc.string+"\n")
                    except:
                        None
                if(ctc.name=='img'):
                    src=ctc.get('src')
                    cc=src.find("images")
                    name=src.split('/')[-1]
                    #print(name)
                    content=self.opener.open(self.url+src[cc:]).read()
                    #imgtype = imghdr.what('', h=content)
                    tag='pic/'+name
                    imgf=open(tag,'wb')
                    imgf.write(content)
                    imgf.close()
                    #self.file.write("("+tag+")\n")
                    self.file.write(".. image:: ./"+tag+'\n')
            else:
                if(ctc.name=='img'):
                    src=ctc.get('src')
                    cc=src.find("images")
                    name=src.split('/')[-1]
                    #print(name)
                    content=self.opener.open(self.url+src[cc:]).read()
                    #imgtype = imghdr.what('', h=content)
                    tag='pic/'+name
                    imgf=open(tag,'wb')
                    imgf.write(content)
                    imgf.close()
                    self.file.write(".. image:: ./"+tag+'\n')
                None
    def digui(self,soup,itrn):
        #print(soup.name)
        #print(itrn)
        
        #if(soup.name=='li'):
         #   for itr in soup.children:
          #      if(itr.name=='a'):
           #         self.article.append([itrn,itr.string,itr.get('href')])
            #        return
        #print(soup.get('href'))            
        if(soup.name=='a'):
            self.article.append([itrn,soup.string,soup.get('href')])
            return
        if(soup.name==None):
            self.article.append([itrn,soup.string,''])
            return
        #if(soup.string!=None):
            #self.article.append([itrn,soup.string,''])
            #return
        for itr in soup.children:
            if(itr.string!=None):
                self.digui(itr,itrn+1)
            else:
                self.digui(itr,itrn+1)
        return
            
    def get_aside(self,soup):
        self.article=[]
        divs=soup.find_all(['div'],id='catelog')
        self.digui(divs[0],0)
        #print(self.article)

    def autofill(self):
        #wd=urllib.request.quote(question_word).replace('%2B','+')
        self.url="http://jiba.niu.bi/"
        
        self.opener = urllib.request.build_opener()
        headers = ('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')
        self.opener.addheaders = [headers]
        htmlpage =self.opener.open(self.url).read()
        #print(htmlpage)
        soup = BeautifulSoup(htmlpage,'html.parser')
        #article=soup.find(['article'])
        aside=soup.find(['aside'])
        #sig.
        #self.get_article(article)
        
        self.get_aside(aside)
        self.gen_article()
        #print(self.article)
    def gen_article(self):
        for art in self.article:
            print(art)
            if(art[0]==4):
                self.file.write(art[1]+"\n")
                self.file.write("^"*len(art[1])+"\n")
            elif(art[0]==6):
                self.file.write(art[1]+"\n")
                self.file.write("-"*len(art[1])+"\n")
            elif(art[0]==7):
                self.file.write(art[1]+"\n")
                self.file.write(">"*len(art[1])+"\n")
            else:
                continue
            htmlpage =self.opener.open(self.url+art[2]).read()
            soup = BeautifulSoup(htmlpage,'html.parser')
            article=soup.find(['article'])
            self.get_article(article)
    def get_next(self):
        None
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

    art=Article()

  

