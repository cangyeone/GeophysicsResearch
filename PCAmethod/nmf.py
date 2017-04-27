# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:57:10 2017

@author:Cangye@hotmail.com
"""
import numpy as np
from sklearn.decomposition import PCA,FastICA,NMF

#!/bin/python


def mynmf(V, r, k, e):
    m, n = np.shape(V)
    W = np.random.random([m, r])
    H = np.random.random([r, n])
    W_sum=np.transpose([np.sum(W,axis=1)])
    W = np.divide(W,W_sum)
    
    for x in range(k):
        #error 
        V_pre = np.dot(W,H)
        E =np.subtract(V,V_pre)
        #print E
        err = np.sum(np.square(E))
        
        if err < e:
            break
        a = np.dot(np.transpose(W),V)
        b = np.dot(np.dot(np.transpose(W),W),H)
        #c = V * H.T
        #d = W * H * H.T
        
        H=np.divide((H*a),b)
        H_sum=np.sum(H,axis=0)
        H = np.divide(H,H_sum)

        #for i_1 in range(r):
         #   for j_1 in range(n):
          #      if b[i_1,j_1] != 0:
           #         H[i_1,j_1] = H[i_1,j_1] * a[i_1,j_1] / b[i_1,j_1]
        c = np.dot(V,np.transpose(H))
        d = np.dot(W,np.dot(H,np.transpose(H)))
        W=np.divide(W*c,d)
        W_sum=np.transpose([np.sum(W,axis=1)])
        W = np.divide(W,W_sum)

    return W,H

class SourceMethod():
    def __init__(self, name,itrN, rg=[1,8], err=0.1, method='pca'):
        import xlrd
        #print(name)
        wb = xlrd.open_workbook(name)
        st = wb.sheet_by_index(0)
        self.xlsdata = []
        for itr in range(st.nrows):
            self.xlsdata.append((st.row_values(itr)))
        self.rdata = []
        self.sample=[]
        for itr in self.xlsdata:
            self.rdata.append(itr[rg[0]:])
            self.sample.append(itr[0])
        self.title=self.xlsdata[0]
        self.data_orig=np.abs(self.rdata[1:])
        self.orig_data=np.array(self.rdata[1:])
        self.dest_err=err
        self.data_max=np.max(np.abs(self.data_orig),axis=0)
        self.data=np.divide(self.data_orig,self.data_max)
        self.minus=np.divide(self.orig_data[1,:],np.abs(self.data_orig[1,:]))
        self.itrN=itrN
        self.train()       
    def func():
        None
    def train(self):
        #data_avg=np.average(self.data)
        data_min=np.min(np.abs(self.data),axis=0)
        base=0.5
        data_sub=np.subtract(self.data,base*data_min)
        #print(np.shape(data_min))
        for itr in range(1,len(self.data)):
            itr=3
            self.components_,self.array=mynmf(data_sub,itr,self.itrN,self.dest_err)
            self.method=FastICA(n_components=itr)
            self.array=np.transpose(self.method.fit_transform(np.transpose(data_sub)))
            self.components_=self.method.mixing_
            self.array=np.add(self.array,data_min*base/itr)
            #err=np.mean(np.abs(self.data-np.dot(self.components_,self.array)))
            self.for_sta=np.multiply(np.abs(np.dot(self.components_,self.array)),self.data_max)
            
            sum_cof=0

            for itra in range(len(self.data[0])):
                sum_cof += self.pearson(np.transpose(self.data)[itra],np.transpose(self.for_sta)[itra])
            sum_cof=sum_cof/len(self.data[0])
            print(sum_cof)
            if(self.dest_err>1-sum_cof):
                break
            if(itr>10):
                break
        #self.for_sta=np.multiply(np.abs(np.dot(self.components_,self.array)),self.data_max)
        self.array=np.multiply(self.array,self.data_max)
        
        self.data_orig=np.multiply(self.data_orig,self.minus)
        self.for_sta=np.multiply(self.for_sta,self.minus)
        self.array=np.multiply(self.array,self.minus)
        
        self.data_orig=np.transpose(self.data_orig)
        self.for_sta=np.transpose(self.for_sta)
        self.array=np.transpose(self.array)
        self.data=np.transpose(self.data)
        self.orig_data=np.transpose(self.orig_data)
    def get_par(self):  
        return self.array,self.method.n_components_,self.method.components_
    def print_sta(self):
        print("Source Number:")
        print(self.components_)
        ratio_sum=np.transpose([np.sum(self.method.components_,axis=1)])
        print("Mixing ratio matrix:")
        print(np.divide(self.method.components_,ratio_sum))
    def pearson(self,x,y):
        x_avg=np.average(x)
        y_avg=np.average(y)
        xv=x-x_avg
        yv=y-y_avg
        cof1=np.sum(xv*yv)
        
        x2=np.sum(np.square(xv))
        y2=np.sum(np.square(yv))
        if(y2==0):
            cof=0
        else:
            cof=cof1/np.sqrt(x2*y2)
        return cof
    def plot_sta(self):
        import matplotlib.pyplot as plt
        #plt.style.use('bmh')
        plt.figure(1)
        tick=np.arange(len(self.array))
        width=0.6/len(self.array[0])
        cont=0
        for dt in np.transpose(self.array):
            #plt.plot(tick+width*cont,dt,alpha=0.4,color=list(plt.rcParams['axes.prop_cycle'])[cont]['color'])
            #plt.bar(tick+width*cont,dt,width,alpha=0.2,color=list(plt.rcParams['axes.prop_cycle'])[cont]['color'])
            cont=cont+1
            
        plt.figure(2)
        cont=0
        for dt in np.transpose(self.array):
            #plt.plot(dt,alpha=0.4,color=list(plt.rcParams['axes.prop_cycle'])[cont]['color'])
            cont=cont+1
            
        plt.figure(3)
        plt.plot(np.average(self.for_sta,axis=0))
        
        for itr in range(len(self.data)):
            plt.figure(4+itr)
            z1= np.polyfit(self.data[itr],self.for_sta[itr], 1)
            
            plt.scatter(self.data[itr],self.for_sta[itr])
            mi=min(self.data[itr])
            ma=max(self.data[itr])
            idtv=ma-mi
            x=np.arange(0,ma,0.01)
            plt.title("$"+str(self.title[itr])+"$")
            cof=self.pearson(self.data[itr],self.for_sta[itr])
            #plt.text(mi/6+ma/6,idtv*0.001,"$f(x)=%fx+%f;cof=%f$"%(z1[0],z1[1],cof))
            #plt.text(mi/1.9+ma/1.9,idtv*0.05,)
            
            plt.plot(x,x*z1[0]+z1[1])
        plt.boxplot(np.transpose(self.data_orig-self.for_sta))
        plt.show()
            #plt.hist(dt,histtype="stepfilled",bins=25,alpha=0.6,normed=True)
class GetExcel():
    def __init__(self,name):
        import xlrd
        wb=xlrd.open_workbook(name)
        st=wb.sheet_by_index(0)
        self.data=[]
        for itr in range(st.nrows-2):
            self.data.append((st.row_values(itr)[0:]))
    def get_data(self,rg):
        rtdata=[]
        for itr in self.data:
            rtdata.append(itr[rg[0]:rg[1]])
        return rtdata
        
class test():
    def save_file(self):
            import xlwt
            f=xlwt.Workbook()
            sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
            sheet2=f.add_sheet(u'sheet2',cell_overwrite_ok=True)
            row0=self.title
            sheet1.write(0,0,"sources:")
            sheet1.write(0,1,len(self.array[0]))

            out_data1=np.transpose(self.array)
            out_data2=np.transpose(self.for_sta)
            out_data3=self.odt
            for i in range(len(row0)):
                sheet1.write(2,i,row0[i])
            for itry in range(len(out_data1)):
                sheet1.write(itry+4,0,"source"+str(itry)+":")
                for itrx in range(len(out_data1[0])):
                    sheet1.write(itry+4,itrx+1,out_data1[itry,itrx])
            for itry in range(len(out_data2)):
                sheet1.write(itry+len(out_data1)+6,0,self.sample[itry+1])
                for itrx in range(len(out_data2[2])):
                    sheet1.write(itry+len(out_data1)+6,itrx+1,out_data2[itry,itrx])
                    
            for itry in range(len(out_data3)):
                sheet2.write(itry,0,self.sample[itry+1])
                for itrx in range(len(out_data3[0])):
                    sheet2.write(itry,itrx+1,out_data3[itry,itrx])
            f.save("aa.xls")
    def calcaute(self):
            self.my_nmf=SourceMethod("data1.xls",int(500),err=1)
            self.data_orig=self.my_nmf.data_orig
            self.for_sta=self.my_nmf.for_sta
            self.title=self.my_nmf.title
            self.array=self.my_nmf.array
            self.odt=self.my_nmf.components_
            self.sample=self.my_nmf.sample
            self.my_nmf.plot_sta()
            print(len(self.array[0]))
if __name__=="__main__":
    data1=np.array([[157,179,117],[49,-237,210],[19504,19503,19971],[2946,3002,2837]])
    data2=np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    excel_file=GetExcel("data1.xls")
    data=excel_file.get_data([1,9])
    data=np.abs(np.transpose(data[1:]))
    #re=np.dot(W,H)
    #print(np.average(re-data))
    method=test()
    #method.print_sta()
    method.calcaute()
    method.save_file()

    
