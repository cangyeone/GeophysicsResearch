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
    def __init__(self,data,err=0.1,method='pca'):
        self.title=data[0]
        self.data_orig=np.abs(np.transpose(data[1:]))
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
            z1= np.polyfit(self.data_orig[itr],self.for_sta[itr], 1)
            
            plt.scatter(self.data_orig[itr],self.for_sta[itr])
            mi=min(self.data_orig[itr])
            ma=max(self.data_orig[itr])
            idtv=ma-mi
            x=np.arange(0,ma,0.01)
            plt.title("$"+str(self.title[itr])+"$")
            cof=self.pearson(self.data_orig[itr],self.for_sta[itr])
            plt.text(mi/6+ma/6,idtv*0.001,"$f(x)=%fx+%f;cof=%f$"%(z1[0],z1[1],cof))
            #plt.text(mi/1.9+ma/1.9,idtv*0.05,)
            
            plt.plot(x,x*z1[0]+z1[1])
        
        plt.show()

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

    def __init__(self,data,*args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        self.data=data
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        #pca=SourceMethod(data)
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.cla()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("application main window")

        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&File...', self.fileOpen,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtGui.QWidget(self)

        l = QtGui.QVBoxLayout(self.main_widget)
        sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        data=[1,2,3]
        dc = MyDynamicMplCanvas(data,self.main_widget, width=5, height=4, dpi=100)
        l.addWidget(sc)
        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileOpen(self):
        self.fileDir=QtGui.QFileDialog.getOpenFileName()

    def closeEvent(self, ce):
        self.fileQuit()
    def fileQuit(self):
        self.close()
    def about(self):
        QtGui.QMessageBox.about(self, "About",
                                """Made by Cangye\n
                                Contact me:\n
                                    Cangye@hotmail.com
                                """
                                )

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
qApp = QtGui.QApplication(sys.argv)
fileName="data.xlsx"
excel_file=GetExcel(fileName)
data=excel_file.get_data([1,9])
method=SourceMethod(data,0.02,'ica')
aw = ApplicationWindow(method)
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())