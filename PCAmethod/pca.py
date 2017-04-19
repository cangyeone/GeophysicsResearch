# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 11:57:10 2017

@author:Cangye@hotmail.com
"""
import numpy as np
from sklearn.decomposition import PCA,FastICA


class SourceMethod():
    def __init__(self,data,method='pca'):
        self.data=data
        self.for_cal=PCA(n_components='mle',whiten=True)
        self.for_cal.fit(data)
        if(method=='pca'):
            self.method=PCA(n_components='mle',whiten=True)
            self.array=self.method.fit_transform(data)
        elif(method=='ica'):
            self.method=FastICA(n_components=self.for_cal.n_components_)
            self.array=self.method.fit_transform(data)
        else:
            None
    def get_par(self):  
        return self.array,self.method.n_components_,self.method.components_
    def print_sta(self):
        print("Original data:")
        print(self.data)
        print("Number of source:")
        print(self.for_cal.n_components_)
        print("Source:")
        print(self.array)
        print("ratio")
        print(self.method.mixing_)
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
    print(data)
    method=SourceMethod(data,'ica')
    method.print_sta()
    #method.plot_sta()

    