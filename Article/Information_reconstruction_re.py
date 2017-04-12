# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 08:48:49 2017

@author: Cangye@hotmail.com
"""

import urllib
from bs4 import BeautifulSoup
import xlwt
class Article():
    def __init__(self,inFile=None,outFile=None,TestMode=False):
        if(TestMode==False):
            self.inFile=inFile
            self.outFile=outFile
            self.complete()
        else:
            print('testmode')
    def getarticleinfo(self,soup_t):
        for itr in soup_t.find_all('h3'):
            for itrst in itr.find_all('a'):
                title=itrst.string
        for itr in soup_t.find_all('p',class_=['abstract']):
            abstract=itr.string
        author=[]
        for itr in soup_t.find_all('p',class_=['author_text']):
            for itrst in itr.find_all(['a']):
                athr=urllib.parse.unquote(itrst.get('href'))
                st=athr.find("author:(")
                nd=athr[st:].find(")")
                author.append(athr[st+8:st+nd])
        publish=[]
        for itr in soup_t.find_all('p',class_=['publish_text']):
            for itrst in itr.find_all(['a','span']):
                publish.append(itrst.string)
        return title,abstract,author,publish
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
            rra,rrb,rrc,rrd=self.getarticleinfo(soup)
        else:
            for link in soup.find_all('a'):
                newwd=link.get('href')
                if(newwd[:14]=="/s?wd=paperuri"):
                    newurl="http://xueshu.baidu.com"+newwd.replace('amp;','')
                    newhtmlpage = opener.open(newurl).read()
                    #newhtmlpage1 = opener.open(newurl).read()
                    newsoup = BeautifulSoup(newhtmlpage,'html.parser')
                    #print(newhtmlpage)
                    #print(newsoup)
                    rra,rrb,rrc,rrd=self.getarticleinfo(newsoup)
                        #print(itr.attrs)
                    break
        return [rra,rrb,rrc,rrd]
        
    def write2excel(self,buf):
        wb=xlwt.Workbook()
        st=wb.add_sheet('name')
        for aa in range(len(buf)):
            athct=0
            try:
                for ath in buf[aa][2]:
                    st.write(aa,athct,ath)
                    athct=athct+1
                    if(athct>3):
                        break
            except:
                print(buf[aa][0]+" no author")
            st.write(aa,5,buf[aa][0])
            try:
                st.write(aa,6,buf[aa][3][0])
                st.write(aa,7,buf[aa][3][1])
                st.write(aa,8,''.join(buf[aa][3][2:-1]))
                st.write(aa,9,buf[aa][3][-1])
            except:
                print(buf[aa][0]+" no info")
        wb.save(self.outFile)
    def complete(self):
        file=open(self.inFile)
        text=file.readlines()
        full_info=[]
        for at_name in text:
            name=at_name.strip()
            try:
                full_info.append(self.autofill(name))
                print("Finished:"+at_name)
            except:
                full_info.append(['','',['','',''],['','','']])
                print('File Err:'+at_name)
        self.write2excel(full_info)

        
if __name__ == '__main__':
    #inFile=input('输入文件名：')
    #outFile=input('输出excel文件名：')
    inFile='a.txt'
    outFile='out.xls'
    art=Article(inFile,outFile)
    #art=Article(TestMode=True)
    #print(art.autofill('3D高阶抛物Radon变换地震数据保幅重建'))
    #print(art.autofill('Twin enigmatic microseismic sources in the Gulf of Guinea observed on intercontinental seismic stations'))


