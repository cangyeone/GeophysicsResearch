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
# customize navigation toolbar
class NavToolbar(NavigationToolbar):
    toolitems = [('Save', 'Save the figure', 'filesave', 'save_figure')]

class SourceMethod():
    def __init__(self, name,itrN, rg=[1,8], err=0.1, method='pca'):
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
        self.itrN=itrN
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
            if(itr>self.itrN):
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

        None

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=5, height=4, dpi=100, title='title'):
        self.title = title
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.suptitle(title)

        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        self.compute_initial_figure()


        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
        self.axes.set_ylabel('label1')
        self.axes.set_xlabel('label')
        self.axes.grid(True)
        #self.axes.set_ylim(0, 0.5)
    def up_date(self,data_orig,for_sta,title):
        self.axes.clear()
        z1= np.polyfit(data_orig,for_sta,1)        
        self.axes.scatter(data_orig,for_sta)
        mi=min(data_orig)
        ma=max(data_orig)
        idtv=ma-mi
        x=np.arange(0,ma,0.01)
        self.axes.title("$"+str(self.title)+"$")
        cof=self.pearson(data_orig,self.for_sta)
        self.axes.text(mi/1.8+ma/1.8,idtv*0.8,"$"+str(title)+"$")
        self.axes.text(mi/6+ma/6,idtv*0.001,"$f(x)=%fx+%f;cof=%f$"%(z1[0],z1[1],cof))
            #plt.text(mi/1.9+ma/1.9,idtv*0.05,)
            
        self.axes.plot(x,x*z1[0]+z1[1])
        self.axes.update()
        self.axes.draw()
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
class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
        self.axes.set_ylabel('label1')
        self.axes.set_xlabel('label')
        self.axes.grid(True)

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.axes.set_ylabel('label y din plot')
        self.axes.set_xlabel('label x din plot')
        self.axes.grid(True)
        self.draw()
        #self.show()
class CelllarAutomaton(QGraphicsItem):
    def __init__(self, width=500, height=500, size=5):
        super(CelllarAutomaton, self).__init__()
        self.width = width
        self.height = height
        self.size = size
        self.NH = self.height//size
        self.NW = self.width//size
        self.board = []
        for y in range(self.NH):
            self.board.append([0] * self.NW)
        self.board[0][self.NW//2] = 1
        self.pos = 0

    def reset(self):
        for y in range(self.NH):
            for x in range(self.NW):
                self.board[y][x] = 0
        self.board[0][self.NW//2] = 1
        self.pos = 0
        self.update()

    def randomInit(self):
        for y in range(self.NH):
            for x in range(self.NW):
                self.board[y][x] = 0
        for x in range(self.NW):
            self.board[0][x] = int(random.random() < 0.2)
        self.pos = 0
        self.update()

    def paint(self, painter, option, widget):
        painter.setPen(QColor(220,220,220))
        for y in range(self.NH):
            painter.drawLine(0, y*self.size, self.width, y*self.size)
        for x in range(self.NW):
            painter.drawLine(x*self.size, 0, x*self.size, self.height)

        painter.setBrush(Qt.black)
        for y in range(self.NH):
            for x in range(self.NW):
                if self.board[y][x] == 1:
                    painter.drawRect(self.size*x, self.size*y, self.size, self.size)

    def do_prev(self):
        if self.pos == 0:
            return
        for x in range(self.NW):
            self.board[self.pos][x] = 0
        self.pos -= 1
        self.update()

    def do_next(self, n):
        if self.pos+1 >= self.NH:
            return False
        p = []
        for i in range(8):
            p.append(n & 0b1) 
            n >>= 1

        self.board[self.pos+1][0] = p[(self.board[self.pos][0]<<1) + self.board[self.pos][1]]
        self.board[self.pos+1][self.NW-1] = p[(self.board[self.pos][self.NW-2]<<1) + self.board[self.pos][self.NW-1]]
        for x in range(1,self.NW-1):
            self.board[self.pos+1][x] = p[(self.board[self.pos][x-1]<<2)
                                            + (self.board[self.pos][x]<<1)
                                            + (self.board[self.pos][x+1])]
        self.pos += 1
        self.update()
        return True

    def boundingRect(self):
        return QRectF(0,0,self.width,self.height)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.graphicsView = QGraphicsView()
        scene = QGraphicsScene(self.graphicsView)
        scene.setSceneRect(0, 0, 400, 400)
        self.graphicsView.setScene(scene)
        self.celluarAutomaton = CelllarAutomaton(400,400)
        scene.addItem(self.celluarAutomaton)

        self.main_widget = QWidget(self)
        #self.sc = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100, title='Title 1')
        #dc = MyDynamicMplCanvas(self.main_widget, width=5, height=4, dpi=100, title='Title 2')
         # full toolbar

        fig = Figure(figsize=(5, 4), dpi=100,facecolor='none')
        self.axes = fig.add_subplot(111)
        self.axes.hold(False)
        self.canvas=FigureCanvas(fig)
        self.scntb = NavigationToolbar(self.canvas,self.main_widget)


        validator = QIntValidator(0,1)
        ruleLayout = QGridLayout()
        ruleLayout.setAlignment(Qt.AlignTop)
        self.ruleEdits = []
        for i in range(7,-1,-1):
            ruleEdit = QLineEdit()
            ruleEdit.setValidator(validator)
            ruleEdit.setText("0")
            ruleEdit.setFixedWidth(30)
            #ruleEdit.textEdited.connect(self.update_rule)
            ruleLayout.addWidget(QLabel("{0:03b}".format(i)), 0, 7-i)
            ruleLayout.addWidget(ruleEdit, 1,7-i)
            self.ruleEdits.append(ruleEdit)
        self.fumla=QLineEdit()

        fumlaLayout = QHBoxLayout()
        fumlaLayout.addWidget(QLabel("Formula:"))
        fumlaLayout.addWidget(self.fumla)


        validator2 = QIntValidator(0,255)
        self.rule10Edit = QLineEdit()
        self.rule10Edit.setText("6")
        self.rule10Edit.setValidator(validator2)
        rule10Layout = QHBoxLayout()
        rule10Layout.addWidget(QLabel("Number"))
        rule10Layout.addWidget(self.rule10Edit)

        conLayout = QHBoxLayout()
        self.tableWidget=QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(3)
        conLayout.addWidget(self.tableWidget )
        
        self.resetButton = QPushButton("&GetFile")
        self.resetButton.clicked.connect(self.get_file)
        self.randomInitButton = QPushButton("&Plot")
        self.randomInitButton.clicked.connect(self.plot)
        self.calButton = QPushButton("&Calcaute")
        self.calButton.clicked.connect(self.calcaute)
        self.nextButton = QPushButton("&Next")
        self.nextButton.clicked.connect(self.do_next)
        self.prevButton = QPushButton("&Save Excel")
        self.prevButton.clicked.connect(self.save_file)
        self.autoButton = QPushButton("&Auto")
        #self.autoButton.clicked.connect(self.auto)
        self.stopButton = QPushButton("&Stop")
        #self.stopButton.clicked.connect(self.stop)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.resetButton)
        buttonLayout.addLayout(rule10Layout)
        buttonLayout.addWidget(self.calButton)
        buttonLayout.addWidget(self.randomInitButton)
        buttonLayout.addWidget(self.nextButton)
        buttonLayout.addWidget(self.prevButton)
        #buttonLayout.addWidget(self.autoButton)
        #buttonLayout.addWidget(self.stopButton)


        


        propertyLayout = QVBoxLayout()
        propertyLayout.setAlignment(Qt.AlignTop)
        propertyLayout.addLayout(conLayout)
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
        self.setWindowTitle("FastICA")
        #self.updating_rule = False
        #self.rule10Edit.setText("90")
        #self.update_rule10()
        #self.timer = None

    def save_file(self):
        fileName, ok2=QFileDialog.getSaveFileName(self,
                                    "文件保存",  
                                    os.getcwd(),  
                                    "All Files (*);;Excel Files (*.xls)")
        import xlwt
        f=xlwt.Workbook()
        sheet1=f.add_sheet(u'sheet1',cell_overwrite_ok=True)
        row0=self.title
        sheet1.write(0,0,"sources:")
        sheet1.write(0,1,len(self.array[0]))
        for i in range(2,len(row0)):
            sheet1.write(2,i,row0[i])
        for itrx in range(len(self.array)):
            for itry in range(len(self.array[0])):
                sheet1.write(itry+4,itrx,self.array[itrx,itry])
        for itrx in range(len(self.odt)):
            for itry in range(len(self.odt[0])):
                sheet1.write(itry+len(self.array[0])+6,itrx,self.odt[itrx,itry])
        f.save(fileName)
    def calcaute(self):
        self.my_nmf=SourceMethod(self.fileName,int(self.rule10Edit.text()))
        self.data_orig=self.my_nmf.data_orig
        self.for_sta=self.my_nmf.for_sta
        self.title=self.my_nmf.title
        self.array=self.my_nmf.array
        self.odt=self.my_nmf.method.components_
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
            self.up_date(self.data_orig[0],self.for_sta[0],self.title[0])
        except:
            self.no_data()
        #self.scntb
    def do_prev(self):
        self.celluarAutomaton.do_prev()

    def reset(self):
        self.celluarAutomaton.reset()

    def randomInit(self):
        self.celluarAutomaton.randomInit()

    def auto(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()

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
        self.fumla.setText("f(x)=%fx+%f;cof=%f"%(z1[0],z1[1],cof))
        self.canvas.draw()
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
