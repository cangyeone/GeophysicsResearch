# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:07:05 2017

@author: LLL
"""

import xlrd
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
insNum=2


    
class Classfication():
    def ReadExcelFile(self,fileName,classIdx=insNum):
        workBook=xlrd.open_workbook(fileName)
        sheet=workBook.sheet_by_index(0)
        nrows=sheet.nrows
        val=[]
        for it in range(1,nrows):
            val.append(sheet.row_values(it))
        def Replace(x):
            if(x[classIdx]=='是' or x[classIdx]==1):
                rt=[1.,0.]
                sp=['+']
            else:
                rt=[0.,1.]
                sp=['o']
            return [x[:classIdx],rt,sp]
        val=list(map(Replace,val))
        dt=[]
        cor=[]
        clr=[]
        for itr in val:
            dt.append(itr[0])
            cor.append(itr[1])
            clr.append(itr[2])
        return dt,cor,list(range(len(dt))),clr
    def Norm(self,data):
        mini=np.min(data,axis=0)
        sc=np.subtract(data,mini)
        maxa=np.max(sc,axis=0)
        mx=np.multiply(np.divide(sc,maxa),0.8)
        mx=np.add(mx,0.1)
        return mx
        
    def GenTrainData(self,data,vali,idx,num=10):
        sel=np.random.choice(idx,num)
        rdt=[]
        rval=[]
        for itr in sel:
            rdt.append(data[itr])
            rval.append(vali[itr])
        return np.array(rdt),np.array(rval)
    
    def GenDataFromExcel(self,fileName=r'index.xlsx',num=10):
        data,vali,idx=self.ReadExcelFile(fileName)
        data=self.Norm(data)
        rd,rv=self.GenTrainData(data,vali,idx,num)
        return rd,rv
    
    def my_weigh(self,shape):
        init=tf.truncated_normal(shape,stddev=0.1)
        #init=tf.constant(0.1,shape=shape)
        return tf.Variable(init)
    def my_bias(self,shape):
        init=tf.constant(0.1,shape=shape)
        return tf.Variable(init) 
    def my_actv(self,aa):
        return tf.nn.relu(aa)
    def __init__(self,fileName=r'美国数据.xlsx',fcl):
        fcl[0]=[insNum,4]
        fcl[1]=[4,4]
        fcl[2]=[4,3]
        fcl[3]=[3,2]
        
        x=tf.placeholder(tf.float32,[None,insNum])
        y=tf.placeholder(tf.float32,[None, 2])
        kp1=tf.placeholder(tf.float32)
        kp2=tf.placeholder(tf.float32)
        kp3=tf.placeholder(tf.float32)
        
        for itr in fcl:
            fc_w1=self.my_weigh(fcl[0])
            fc_b1=self.my_bias([fcl[0][1]])
            fc_fn1=tf.matmul(x,fc_w1)+fc_b1
            fc1=self.my_actv(fc_fn1)
        
        fc1_d=tf.nn.dropout(fc1,kp3)
        
        fc_w2=self.my_weigh(fcl2)
        fc_b2=self.my_bias([fcl2[1]])
        fc_fn2=tf.matmul(fc1_d,fc_w2)+fc_b2
        fc2=self.my_actv(fc_fn2)
        
        fc2_d=tf.nn.dropout(fc2,kp3)
        
        fc_w3=self.my_weigh(fcl3)
        fc_b3=self.my_bias([fcl3[1]])
        fc_fn3=tf.matmul(fc2_d,fc_w3)+fc_b3
        fc3=self.my_actv(fc_fn3)
        
        fc3_d=tf.nn.dropout(fc3,kp3)
        
        fc_w4=self.my_weigh(fcl4)
        fc_b4=self.my_bias([fcl4[1]])
        fc_fn4=tf.matmul(fc3_d,fc_w4)+fc_b4
        fc4=self.my_actv(fc_fn4)
        
        ce=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=fc4))
        #ce=-tf.reduce_mean(fc2*y)
        ts=tf.train.AdamOptimizer(1e-2).minimize(ce)
        
        correct_prediction = tf.equal(tf.argmax(fc4,1), tf.argmax(y,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        
        
        sess=tf.Session()
        sess.run(tf.global_variables_initializer())
        
        
        data,vali,idx,clr=self.ReadExcelFile(fileName)
        
        tdata=np.transpose(data)
        
        data=Norm(data)
        outdata=np.transpose(data)
        st=time.clock()
        for itr in range(3000):
            rd,rv=GenTrainData(data,vali,idx,80)
        
            sess.run(ts,feed_dict={x:rd,y:rv,kp1:1,kp2:1,kp3:1})
            if(itr%100==0):
                acc=sess.run(accuracy,feed_dict={x:data,y:vali,kp1:1,kp2:1,kp3:1})
                ed=time.clock()
                print("file:%s  迭代次数:%5d   准确率:%7.3f%%  用时%7.3fs"%(fileName,itr,acc*100,ed-st))
        mat=[]
        for aa in [[x*0.01,y*0.01] for x in range(10,90) for y in range(10,90)]:
            mat.append(aa)
            
        
        rmat=sess.run(fc4,feed_dict={x:mat,kp1:1,kp2:1,kp3:1})
        rmat=np.transpose(rmat)
        
        w1v=np.transpose(sess.run(fc_w1.value()))
        w2v=np.transpose(sess.run(fc_w2.value()))
        w3v=np.transpose(sess.run(fc_w3.value()))
        w4v=np.transpose(sess.run(fc_w4.value()))
        
        X,Y=np.meshgrid([x*0.01 for x in range(10,90)],[x*0.01 for x in range(10,90)])
        print(np.shape(rmat))
        Z1=np.transpose(np.reshape(rmat[1],[len(X),len(Y)]))
        Z0=np.transpose(np.reshape(rmat[0],[len(X),len(Y)]))
        Z=Z1/(Z1+Z0)
        plt.figure(1)
        ax1=plt.subplot()
        ax1.contourf(X,Y,Z,cmap=plt.get_cmap('seismic'))
        for idx in range(len(tdata[0])):
            ax1.scatter(data[idx][0],data[idx][1],marker=clr[idx][0])
        plt.figure(2)
        def PlotWeigh(www,layer):
            www=np.abs(www)
            for idy in range(len(www)):
                for idx in range(len(www[0])):
                    plt.plot([layer-1,layer],[idx,idy],c='b',lw=www[idy][idx]*2)
                    plt.scatter([layer-1],[idx])
                    plt.scatter([layer],[idy])
                plt.plot([layer,layer],[idx,idy],c='y',linestyle='--',lw=3)
        PlotWeigh(w1v,1)
        PlotWeigh(w2v,2)
        PlotWeigh(w3v,3)
        PlotWeigh(w4v,4)
        """
        fig=plt.figure(2)
        ax=fig.gca(projection='3d')
        x1=tdata[1]
        x2=tdata[2]
        x3=tdata[3]
        ax.scatter(x1,x2,c=clr)
        """
        plt.show()    
    
    
    
if __name__ == '__main__':
    aa=Classfication()

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    