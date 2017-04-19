# embedding_in_qt4.py --- Simple Qt4 application embedding matplotlib canvases
#
# Copyright (C) 2005 Florent Rougon
#               2006 Darren Dale
#
# This file is an example program for matplotlib. It may be used and
# modified with no restriction; raw copies as well as modified versions
# may be distributed without limitation.

from __future__ import unicode_literals
import sys
import os
import random
from matplotlib.backends import qt_compat
use_pyside = qt_compat.QT_API == qt_compat.QT_API_PYSIDE
if use_pyside:
    from PySide import QtGui, QtCore
else:
    from PyQt4 import QtGui, QtCore

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

progname = os.path.basename(sys.argv[0])
progversion = "0.1"
import numpy as np
from sklearn.decomposition import PCA,FastICA,NMF

class SourceMethod():
    def __init__(self, name, rg=[1,8], err=0.1, method='pca'):
        import xlrd
        #print(name)
        wb = xlrd.open_workbook(name)
        st = wb.sheet_by_index(0)
        self.xlsdata = []
        for itr in range(st.nrows-2):
            self.xlsdata.append((st.row_values(itr)[0:]))
        self.rdata = []
        for itr in self.xlsdata:
            self.rdata.append(itr[rg[0]:rg[1]])
        self.title=self.rdata[0]
        self.data_orig=np.abs(np.transpose(self.rdata[1:]))
        self.dest_err=err
        self.data_max=np.transpose([np.max(np.abs(self.data_orig),axis=1)])
        self.data=np.divide(self.data_orig,self.data_max)
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
        self.for_sta=np.multiply(np.abs(np.dot(self.array,self.method.components_)),self.data_max)
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

        
        itr=ct%len(self.data)
        #print(itr)
        z1= np.polyfit(self.data_orig[itr],self.for_sta[itr],1)        
        self.axes.scatter(self.data_orig[itr],self.for_sta[itr])
        mi=min(self.data_orig[itr])
        ma=max(self.data_orig[itr])
        idtv=ma-mi
        x=np.arange(0,ma,0.01)
        #self.axes.title("$"+str(self.title[itr])+"$")
        cof=self.pearson(self.data_orig[itr],self.for_sta[itr])
        self.axes.text(mi/1.8+ma/1.8,idtv*0.8,"$"+str(self.title[itr])+"$")
        self.axes.text(mi/6+ma/6,idtv*0.001,"$f(x)=%fx+%f;cof=%f$"%(z1[0],z1[1],cof))
            #plt.text(mi/1.9+ma/1.9,idtv*0.05,)
            
        self.axes.plot(x,x*z1[0]+z1[1])
        self.cont=self.cont+1

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self,data, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.data=data
        self.cont=0
        self.update_figure()


    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        if(self.data==None):
            self.axes.cla()
            self.axes.plot([0, 1, 2, 3], l, 'r')
            self.draw()

class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Open', self.fileOpen,
                                 QtCore.Qt.CTRL)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtGui.QWidget(self)
        self.data=None
        l = QtGui.QVBoxLayout(self.main_widget)
        #sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.dc = MyDynamicMplCanvas(self.data,self.main_widget, width=5, height=4, dpi=100)
        self.MyTable=QtGui.QTableWidget(5,30)
        l.addWidget(self.MyTable)
        l.addWidget(self.dc)
        
        #self.l.addWidget(self.MyTable)
        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)
    

        
    def fileQuit(self):
        self.close()
    def fileOpen(self):
        self.fileDir=QtGui.QFileDialog.getOpenFileName()
        self.fileGet(self.fileDir)
        for itr in range(len(self.title)):
            newItem =QtGui.QTableWidgetItem(self.title[itr])
            self.MyTable.setItem(0,itr,newItem)
            
        for itry in range(len(self.data[:4])):
            for itrx in range(len(self.data)):
                newItem =QtGui.QTableWidgetItem(str(self.data[itry][itrx]))
                self.MyTable.setItem(itry+1,itrx,newItem)
        self.dc.axes.cla()
        self.dc.axes.plot([1,2,3,4])
        self.show()
    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About",
                                """Cangye@hotmail.com"""
                                )
    def fileGet(self,name,rg=[1,8],err=0.1,method='pca'):
        import xlrd
        #print(name)
        wb=xlrd.open_workbook(name)
        st=wb.sheet_by_index(0)
        self.xlsdata=[]
        for itr in range(st.nrows-2):
            self.xlsdata.append((st.row_values(itr)[0:]))
        self.rdata=[]
        for itr in self.xlsdata:
            self.rdata.append(itr[rg[0]:rg[1]])
        self.title=self.rdata[0]
        self.data_orig=np.abs(np.transpose(self.rdata[1:]))
        self.dest_err=err
        self.data_max=np.transpose([np.max(np.abs(self.data_orig),axis=1)])
        self.data=np.divide(self.data_orig,self.data_max)
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
        self.for_sta=np.multiply(np.abs(np.dot(self.array,self.method.components_)),self.data_max)
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
    def my_fig(self,data, *args, **kwargs):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    def plot_sta(self,ct):
        #plt.style.use('bmh')

        
        itr=ct%len(self.data)
        #print(itr)
        z1= np.polyfit(self.data_orig[itr],self.for_sta[itr],1)        
        self.axes.scatter(self.data_orig[itr],self.for_sta[itr])
        mi=min(self.data_orig[itr])
        ma=max(self.data_orig[itr])
        idtv=ma-mi
        x=np.arange(0,ma,0.01)
        #self.axes.title("$"+str(self.title[itr])+"$")
        cof=self.pearson(self.data_orig[itr],self.for_sta[itr])
        self.axes.text(mi/1.8+ma/1.8,idtv*0.8,"$"+str(self.title[itr])+"$")
        self.axes.text(mi/6+ma/6,idtv*0.001,"$f(x)=%fx+%f;cof=%f$"%(z1[0],z1[1],cof))
            #plt.text(mi/1.9+ma/1.9,idtv*0.05,)
            
        self.axes.plot(x,x*z1[0]+z1[1])
        self.cont=self.cont+1
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
qApp = QtGui.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()