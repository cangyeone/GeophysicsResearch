# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:57:10 2017

@author:Cangye@hotmail.com
"""
import numpy as np
from sklearn.decomposition import PCA,FastICA,NMF


class SourceMethod():
    def __init__(self,data,method='pca'):
        self.data=data
        
        
        self.train()
    def func():
        None
    def train(self):
        for itr in range(1,len(self.data)):
            self.method=NMF(n_components=itr)
            self.array=self.method.fit_transform(data)
            print(np.mean(np.dot(self.array,self.method.components_)))
        
        
    def get_par(self):  
        return self.array,self.method.n_components_,self.method.components_
    def print_sta(self):
        print("Original data:")
        print(self.data)
        print("Source:")
        print(self.array)
        print("Source Number:")
        print(self.method.n_components_)
        print("Mixing matrix:")
        print(np.shape(self.method.components_))
    def plot_sta(self):
        import matplotlib.pyplot as plt
        plt.style.use('bmh')
        tick=np.arange(len(self.array))
        width=0.6/len(self.array[0])
        cont=0
        for dt in np.transpose(self.array):
            plt.bar(tick+width*cont,dt,width,alpha=0.2,color=list(plt.rcParams['axes.prop_cycle'])[cont]['color'])
            cont=cont+1
            #plt.hist(dt,histtype="stepfilled",bins=25,alpha=0.6,normed=True)
class GetExcel():
    def __init__(self,name):
        import xlrd
        wb=xlrd.open_workbook(name)
        st=wb.sheet_by_index(0)
        self.data=[]
        for itr in range(1,st.nrows-2):
            self.data.append((st.row_values(itr)[1:]))
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
    #print(data)

    data=np.transpose(data[:])
    data_max=np.transpose([np.max(np.abs(data),axis=1)])
#
    #print(data_max)
    data=np.divide(np.abs(data),data_max)
    
    #print(data)
    method=SourceMethod(data,'ica')
    method.print_sta()
    method.plot_sta()

    
