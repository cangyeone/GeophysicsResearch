# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:57:10 2017

@author:Cangye@hotmail.com
"""
import numpy as np
from sklearn.decomposition import PCA,FastICA,NMF


class SourceMethod():
    def __init__(self,data,err=0.1,method='pca',norm=False):
        self.title=data[0]
        self.data=np.abs(np.transpose(data[1:]))
        self.dest_err=err
        if(norm==True):
            data_max=np.transpose([np.max(np.abs(self.data),axis=1)])
            self.data=np.divide(self.data,data_max)
        self.train()
    def func():
        None
    def train(self):
        data_avg=np.average(self.data)
        for itr in range(1,len(self.data)):
            self.method=NMF(n_components=itr)
            self.array=self.method.fit_transform(self.data)
            err=np.mean(np.abs(self.data-np.dot(self.array,self.method.components_)))
            if(err<data_avg*self.dest_err):
                break
        self.for_sta=np.abs(np.dot(self.array,self.method.components_))
    def get_par(self):  
        return self.array,self.method.n_components_,self.method.components_
    def print_sta(self):
        print("Source Number:")
        print(self.method.n_components_)
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
            plt.plot(tick+width*cont,dt,alpha=0.4,color=list(plt.rcParams['axes.prop_cycle'])[cont]['color'])
            plt.bar(tick+width*cont,dt,width,alpha=0.2,color=list(plt.rcParams['axes.prop_cycle'])[cont]['color'])
            cont=cont+1
            
        plt.figure(2)
        cont=0
        for dt in np.transpose(self.array):
            plt.plot(dt,alpha=0.4,color=list(plt.rcParams['axes.prop_cycle'])[cont]['color'])
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
            plt.text(mi/6+ma/6,idtv*0.001,"$f(x)=%fx+%f;cof=%f$"%(z1[0],z1[1],cof))
            #plt.text(mi/1.9+ma/1.9,idtv*0.05,)
            
            plt.plot(x,x*z1[0]+z1[1])
        
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
if __name__=="__main__":
    data1=np.array([[157,179,117],[49,-237,210],[19504,19503,19971],[2946,3002,2837]])
    data2=np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    excel_file=GetExcel("data.xlsx")
    data=excel_file.get_data([1,9])

    method=SourceMethod(data,0.02,'ica',norm=True)
    method.print_sta()
    method.plot_sta()

    
