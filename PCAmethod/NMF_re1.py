#!/usr/bin/env python

import random

from PyQt5.QtCore import (QLineF, QPointF, QRectF, Qt, QTimer)
from PyQt5.QtGui import (QBrush, QColor, QPainter, QIntValidator)
from PyQt5.QtWidgets import (QApplication, QWidget, QGraphicsView, QGraphicsScene, QGraphicsItem,
                             QGridLayout, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QPushButton,QFileDialog)

from PyQt5.QtWidgets import (QWidget, QTableWidget, QHBoxLayout, QApplication, QDesktopWidget, QTableWidgetItem, QHeaderView)
import os
import sys
import random
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from sklearn.decomposition import PCA,FastICA,NMF
class NavToolbar(NavigationToolbar):
    toolitems = [('Save', 'Save the figure', 'filesave', 'save_figure')]

                 
def mynmf(V, r, k, e):
    m, n = np.shape(V)
    W = np.random.random([m, r])
    H = np.random.random([r, n])
    H_sum=np.sum(H,axis=0)
    H = np.divide(H,H_sum)
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
        """
        for i_2 in range(m):
            for j_2 in range(r):
                if d[i_2, j_2] != 0:
                    W[i_2,j_2] = W[i_2,j_2] * c[i_2,j_2] / d[i_2, j_2]
        """
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
        self.data_orig=np.abs(np.transpose(self.rdata[1:]))
        self.orig_data=(np.transpose(self.rdata[1:]))
        self.dest_err=err
        self.data_max=np.transpose([np.max(np.abs(self.data_orig),axis=1)])
        self.data=np.divide(self.data_orig,self.data_max)
        self.minus=np.transpose([np.divide(self.orig_data[:,10],np.abs(self.data_orig[:,10]))])
        self.itrN=itrN
        self.train()       
    def func():
        None
    def train(self):
        data_avg=np.average(self.data)
        data_min=np.transpose([np.min(np.abs(self.data),axis=1)])
        data_sub=np.subtract(self.data,0.5*data_min)
        for itr in range(1,len(self.data)):
            self.method=NMF(n_components=itr)
            self.array=self.method.fit_transform(data_sub)
            self.array=np.add(self.array,data_min*0.5/itr)
            err=np.mean(np.abs(self.data-np.dot(self.array,self.method.components_)))
            if(err<data_avg*self.dest_err):
                break
            if(itr>self.itrN):
                break
        self.for_sta=np.multiply(np.abs(np.dot(self.array,self.method.components_)),self.data_max)
        self.array=np.multiply(self.array,self.data_max)
        self.data_orig=np.multiply(self.data_orig,self.minus)
        self.for_sta=np.multiply(self.for_sta,self.minus)
        self.array=np.multiply(self.array,self.minus)
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
    def plot_sta(self,ct):
        #plt.style.use('bmh')

        None

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)


        self.main_widget = QWidget(self)

        fig = Figure(figsize=(5, 4), dpi=100,facecolor='none')
        self.axes = fig.add_subplot(111)
        self.canvas=FigureCanvas(fig)
        self.scntb = NavigationToolbar(self.canvas,self.main_widget)

        
        fumlaLayout = QHBoxLayout()
        fumlaLayout.addWidget(QLabel("Element:"))
        self.element=QLineEdit()
        fumlaLayout.addWidget(self.element)
        fumlaLayout.addWidget(QLabel("Formula:"))
        self.fumla=QLineEdit()
        fumlaLayout.addWidget(self.fumla)
        fumlaLayout.addWidget(QLabel("err:"))
        self.err=QLineEdit()
        fumlaLayout.addWidget(self.err)



        rule10Layout = QVBoxLayout()
        #rule10Layout.addWidget(QLabel("Set Source"))
        self.rule10Edit = QLineEdit()
        self.rule10Edit.setText("6")
        #rule10Layout.addWidget(self.rule10Edit)
        rule10Layout.addWidget(QLabel("Set err"))
        self.rule11Edit = QLineEdit()
        self.rule11Edit.setText("0.1")
        rule10Layout.addWidget(self.rule11Edit)


        
        self.resetButton = QPushButton("&GetFile")
        self.resetButton.clicked.connect(self.get_file)
        self.randomInitButton = QPushButton("&Plot")
        self.randomInitButton.clicked.connect(self.plot)
        self.calButton = QPushButton("&Calcaute")
        self.calButton.clicked.connect(self.calcaute)
        self.nextButton = QPushButton("&Polt Box")
        self.nextButton.clicked.connect(self.plot_box)
        self.prevButton = QPushButton("&Save Excel")
        self.prevButton.clicked.connect(self.save_file)
        self.polarButton = QPushButton("&Plot Polar")
        self.polarButton.clicked.connect(self.plot_polar)
        self.stopButton = QPushButton("&Stop")
        #self.stopButton.clicked.connect(self.stop)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.resetButton)
        buttonLayout.addLayout(rule10Layout)
        buttonLayout.addWidget(self.calButton)
        buttonLayout.addWidget(self.randomInitButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.prevButton)
        #buttonLayout.addWidget(self.polarButton)
        #buttonLayout.addWidget(self.stopButton)

        propertyLayout = QVBoxLayout()
        propertyLayout.setAlignment(Qt.AlignTop)
        #propertyLayout.addLayout(conLayout)
        #propertyLayout.addLayout(rule10Layout)
        propertyLayout.addLayout(buttonLayout)
        graphLayer = QVBoxLayout()
        graphLayer.addWidget(self.canvas)
        graphLayer.addLayout(fumlaLayout)
        graphLayer.addWidget(self.scntb)
        mainLayout = QHBoxLayout()
        mainLayout.setAlignment(Qt.AlignTop)
        mainLayout.addLayout(graphLayer)
        mainLayout.addLayout(propertyLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("NMFMethod")
        #self.updating_rule = False
        #self.rule10Edit.setText("90")
        #self.update_rule10()
        #self.timer = None

    def save_file(self):
        fileName, ok2=QFileDialog.getSaveFileName(self,
                                    "文件保存",  
                                    os.getcwd(),  
                                    "All Files (*);;Excel Files (*.xls)")
        try:
            import xlwt
            f=xlwt.Workbook()
            sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
            row0=self.title
            sheet1.write(0,0,"sources:")
            sheet1.write(0,1,len(self.array[0]))

            out_data1=np.transpose(self.array)
            out_data2=np.transpose(self.for_sta)

            for i in range(len(row0)):
                sheet1.write(2,i,row0[i])
            for itry in range(len(out_data1)):
                sheet1.write(itry+4,0,"source"+str(itry)+":")
                for itrx in range(len(out_data1[0])):
                    sheet1.write(itry+4,itrx+1,out_data1[itry,itrx])
            for itry in range(len(out_data2)):
                sheet1.write(itry+len(out_data1)+6,0,self.sample[itrx])
                for itrx in range(len(out_data2[2])):
                    sheet1.write(itry+len(out_data1)+6,itrx+1,out_data2[itry,itrx])
            f.save(fileName)
        except:
            self.no_data()
    def calcaute(self):
        try:
            self.my_nmf=SourceMethod(self.fileName,int(100),err=float(self.rule11Edit.text()))
            self.data_orig=self.my_nmf.data_orig
            self.for_sta=self.my_nmf.for_sta
            self.title=self.my_nmf.title
            self.array=self.my_nmf.array
            self.odt=self.my_nmf.method.components_
            self.sample=self.my_nmf.sample
            self.count=0
        except:
            self.no_data
    def get_file(self):
        self.fileName, filetype = QFileDialog.getOpenFileName(self,  
                                    "选取文件",  
                                    os.getcwd(),  
                                  "All Files (*);;Excle Files (*.xlsx)")

        self.count=0
    def do_next(self):
        self.count=self.count+1
        itr=self.count%(len(self.data_orig))
        self.up_date(self.data_orig[itr],self.for_sta[itr],self.title[itr])
    def plot(self):
        try:
            if(self.count==0):
                self.up_date(self.data_orig[0],self.for_sta[0],self.title[1])
                self.count +=1
            else:
                itr=self.count%len(self.data_orig)
                self.up_date(self.data_orig[itr],self.for_sta[itr],self.title[itr+1])
                self.count +=1
        except:
            self.no_data()
        #self.scntb
    def plot_polar(self):
        try:
            import matplotlib.pyplot as plt
            self.axes.clear()
            data=self.array
            N=len(data[0])
            theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
            radii = 10*np.random.rand(N)
            width = np.pi / 4 * np.random.rand(N)
            #self.axes.set_projection("polar")
            for itrn,itr in zip(range(len(data)),data):
                ax=self.axes.bar(theta,itr/np.max(itr),width=itr/np.max(itr)*0.76,alpha=0.5)
            self.canvas.draw()
        except:
            self.no_data()
    def plot_box(self):
        try:
            self.up_date_box()
        except:
            self.no_data()
    def up_date(self,data_orig,for_sta,title):
        self.axes.clear()
        z1= np.polyfit(data_orig,for_sta,1)        
        
        mi=min(data_orig)
        ma=max(data_orig)
        idtv=ma-mi
        x=np.arange(0,ma,0.01)
        #self.axes.title("$"+str(self.title)+"$")
        cof=self.pearson(data_orig,for_sta)

            #plt.text(mi/1.9+ma/1.9,idtv*0.05,)   
        self.axes.plot(x,x*z1[0]+z1[1],alpha=0.5)
        self.axes.scatter(data_orig,for_sta,alpha=0.5)
        self.axes.text(mi/1.8+ma/1.8,idtv*0.8,"$"+str(title)+"$")
        #self.axes.text(mi/6+ma/6,idtv*0.001,"$f(x)=%fx+%f;cof=%f$"%(z1[0],z1[1],cof))
        self.fumla.setText("%fx+%f"%(z1[0],z1[1]))
        self.element.setText(str(title))
        self.err.setText(str(cof))
        self.canvas.draw()
    def up_date_box(self):
        try:
            self.axes.clear()
            #plt.text(mi/1.9+ma/1.9,idtv*0.05,)   
            self.axes.boxplot(np.transpose(self.data_orig-self.for_sta))
            self.fumla.setText("None")
            self.element.setText("None")
            self.err.setText("None")
            self.canvas.draw()
        except:
            self.no_data()
    def no_data(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
        self.axes.grid(True)
        self.canvas.draw()  
    #def keyPressEvent(self, event):
    #    key = event.key()
    #    super(MainWindow, self).keyPressEvent(event)
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
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    mainWindow = MainWindow()

    mainWindow.show()
    sys.exit(app.exec_())