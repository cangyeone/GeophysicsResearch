<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:07:05 2017

@author: LLL
"""

try:
    import tensorflow as tf
except:
    import os
    os.system('pip install tensorflow')
finally:
    import xlrd
    import tensorflow as tf
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import time

    
class Classfication():
    def ReadExcelFile(self,fileName,classIdx):
        workBook=xlrd.open_workbook(fileName)
        sheet=workBook.sheet_by_index(0)
        nrows=sheet.nrows
        val=[]
        self.attri=sheet.row_values(0)

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
        self.NormCnt=0
        if(self.NormCnt==0):
            self.mini=np.min(data,axis=0)
        sc=np.subtract(data,self.mini)
        if(self.NormCnt==0):
            self.maxa=np.max(sc,axis=0)
        mx=np.multiply(np.divide(sc,self.maxa),0.8)
        mx=np.add(mx,0.1)
        self.NormCnt=self.NormCnt+1
        return mx,self.maxa,self.mini
        
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
        #init=tf.truncated_normal(shape,stddev=0.1)
        init=tf.constant(0.1,shape=shape)
        return tf.Variable(init)
    def my_bias(self,shape):
        init=tf.constant(0.1,shape=shape)
        return tf.Variable(init) 
    def my_actv(self,aa):
        return tf.nn.sigmoid(aa)
    def LayerToFcl(self,data):
        re=[]
        for itr in range(len(data)-1):
            re.append([data[itr],data[itr+1]])
        return re
    def FitFunc(self,x,a,b,c,d,e,f):
        re=a*np.exp(b*x*x+c*x+d)+e
        return re
    def __init__(self,fileName,valiName,layer=[2,2]):
        
        fcl=self.LayerToFcl(layer)
        
        x=tf.placeholder(tf.float32,[None,fcl[0][0]])
        y=tf.placeholder(tf.float32,[None, 2])
        kp1=tf.placeholder(tf.float32)
        kp2=tf.placeholder(tf.float32)
        kp3=tf.placeholder(tf.float32)
        fc_w=[]
        fc_b=[]
        fc_fn=[]
        fc=[]
        for itr in range(len(fcl)):
            fc_w.append(self.my_weigh(fcl[itr]))
            fc_b.append(self.my_bias([fcl[itr][1]]))
            if(itr==0):
                fc_fn.append(tf.matmul(x,fc_w[itr])+fc_b[itr])
            else:
                fc_fn.append(tf.matmul(fc[itr-1],fc_w[itr])+fc_b[itr])
            fc.append(self.my_actv(fc_fn[itr]))
        nFcl=len(fcl)

        ce=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=fc[nFcl-1]))
        #ce=-tf.reduce_mean(fc2*y)
        ts=tf.train.AdamOptimizer(1e-2).minimize(ce)
        
        correct_prediction = tf.equal(tf.argmax(fc[nFcl-1],1), tf.argmax(y,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        
        
        sess=tf.Session()
        sess.run(tf.global_variables_initializer())
        
        train_data_t,train_vali,train_idx,train_clr=self.ReadExcelFile(fileName,classIdx=fcl[0][0])
        data_t,vali,idx,clr=self.ReadExcelFile(valiName,classIdx=fcl[0][0])
        
        tdata=np.transpose(data_t)
        data,maxa,mini=self.Norm(data_t)
        train_data,tmaxa,tmini=self.Norm(train_data_t)
        st=time.clock()
        for itr in range(3000):
            rd,rv=self.GenTrainData(train_data,train_vali,train_idx,30)
            sess.run(ts,feed_dict={x:rd,y:rv,kp1:1,kp2:1,kp3:1})
            if(itr%100==0):
                self.acc=sess.run(accuracy,feed_dict={x:data,y:vali,kp1:1,kp2:1,kp3:1})
                ed=time.clock()
                print("file:%s  迭代次数:%5d   准确率:%7.3f%%  用时%7.3fs"%(fileName,itr,self.acc*100,ed-st))
        
        try:
                
            mat=[]    
            for aa in [[x*0.01,y*0.01] for x in range(10,90) for y in range(10,90)]:
                mat.append(aa)   
            rmat=sess.run(fc[nFcl-1],feed_dict={x:mat,kp1:1,kp2:1,kp3:1})
            rmat=np.transpose(rmat)
    
            X,Y=np.meshgrid([(float(x)*0.01-0.1)/0.8*tmaxa[0]+tmini[0] for x in range(10,90)],[((x*0.01)-0.1)/0.8*tmaxa[1]+tmini[1] for x in range(10,90)])
            Z1=np.transpose(np.reshape(rmat[1],[len(X),len(Y)]))
            Z0=np.transpose(np.reshape(rmat[0],[len(X),len(Y)]))
            Z=Z1/(Z1+Z0)
            plydata=[]
            x = np.linspace(0,(float(90)*0.01-0.1)/0.8*tmaxa[0]+tmini[0],100)
            for ity in range(len(X)):
                for itx in range(len(X[0])):
                    if(np.abs(Z[ity][itx]-0.5)<0.02):
                        plydata.append([X[ity][itx],Y[ity][itx]])
            plydata=np.transpose(plydata)
            
            import scipy.optimize as opt
            self.fita,fitb=opt.curve_fit(self.FitFunc,plydata[0],plydata[1],[0.01,0.01,0.0,0.01,0,0.0])
            
            self.cof = np.polyfit(plydata[0],plydata[1],3)
            func=np.poly1d(self.cof)
        except:
            print("Not 2d data!")
        try:
            plt.figure(1)
            ax1=plt.subplot()
            ax1.contourf(X,Y,Z,cmap=plt.get_cmap('seismic'))
            for idx in range(len(tdata[0])):
                ax1.scatter(data_t[idx][0],data_t[idx][1],marker=clr[idx][0])
            ax1.plot(x,func(x),lw=1)
            ax1.text(0,1,'$f(x)=%20.15f+%20.15fx+%20.15fx^2$'%(self.cof[2],self.cof[1],self.cof[0]))
            ax1.text(0,0.8,'$f(x)=%fe^{%fx^2+%fx+%f}+%f+%fx$'%(self.fita[0],self.fita[1],self.fita[2],self.fita[3],self.fita[4],self.fita[5]))
                     
            ax1.plot(x,self.FitFunc(x,self.fita[0],self.fita[1],self.fita[2],self.fita[3],self.fita[4],self.fita[5]),lw=1)
        except:
            print("can not plot matrix")
            
        try:
            plt.figure(2)
            wv=[]
            for itr in range(nFcl):
                wv.append(sess.run(fc_w[itr].value()))
            self.outwv=wv
            ii=0
            for lb in self.attri[:-1]:
                plt.text(-0,ii,str(lb),horizontalalignment='right')
                ii=ii+1
            def PlotWeigh(www,layer):
                www=np.abs(www)
                mx=np.max(www)
                for idy in range(len(www)):
                    for idx in range(len(www[0])):
                        plt.plot([layer-1,layer],[idx,idy],c='b',lw=www[idy][idx]*3/mx)
                        plt.scatter([layer-1],[idx])
                        plt.scatter([layer],[idy])
                    plt.plot([layer,layer],[idx,idy],c='y',linestyle='--',lw=3)
            for itr in range(nFcl):
                #print(np.shape(wv[itr]))
                PlotWeigh(np.transpose(wv[itr]),itr+1)
        except:
            print('can not plot weigh')


        plt.show()    
    
    
    
if __name__ == '__main__':
    
    #节点数目
    #[输入层数目，隐藏层节点数，.....，隐藏层节点数，输出层节点数]
    layer=[10,8,4,2]
    #读取文件名
    fileName=r'index.xlsx'
    valiFileName=r'index.xlsx'
    #训练
    aa=Classfication(fileName,valiFileName,layer=layer)
    outFile=open('out.txt','w')
    outFile.write('Function is:\n')
    outFile.write('f(x)=%f+%f*x+%f*x^2(err:%f)\n'%(aa.cof[2],aa.cof[1],aa.cof[0],aa.acc))
    outFile.write('f(x)=%fe^{%fx+%f}+%fe^{%fx+%f}\n'%(aa.fita[0],aa.fita[1],aa.fita[2],aa.fita[3],aa.fita[4],aa.fita[5]))
    outFile.write('Weigh is:\n')
    for ity in aa.outwv:
        for it in ity:
            outFile.write(str(it)+' ')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
=======
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 10:07:05 2017

@author: LLL
"""

try:
    import tensorflow as tf
except:
    import os
    os.system('pip install tensorflow')
finally:
    import xlrd
    import tensorflow as tf
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import time

    
class Classfication():
    def ReadExcelFile(self,fileName,classIdx):
        workBook=xlrd.open_workbook(fileName)
        sheet=workBook.sheet_by_index(0)
        nrows=sheet.nrows
        val=[]
        self.attri=sheet.row_values(0)

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
        self.NormCnt=0
        if(self.NormCnt==0):
            self.mini=np.min(data,axis=0)
        sc=np.subtract(data,self.mini)
        if(self.NormCnt==0):
            self.maxa=np.max(sc,axis=0)
        mx=np.multiply(np.divide(sc,self.maxa),0.8)
        mx=np.add(mx,0.1)
        self.NormCnt=self.NormCnt+1
        return mx,self.maxa,self.mini
        
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
        #init=tf.truncated_normal(shape,stddev=0.1)
        init=tf.constant(0.1,shape=shape)
        return tf.Variable(init)
    def my_bias(self,shape):
        init=tf.constant(0.1,shape=shape)
        return tf.Variable(init) 
    def my_actv(self,aa):
        return tf.nn.sigmoid(aa)
    def LayerToFcl(self,data):
        re=[]
        for itr in range(len(data)-1):
            re.append([data[itr],data[itr+1]])
        return re
    def FitFunc(self,x,a,b,c,d,e,f):
        re=a*np.exp(b*x*x+c*x+d)+e
        return re
    def __init__(self,fileName,valiName,layer=[2,2]):
        
        fcl=self.LayerToFcl(layer)
        
        x=tf.placeholder(tf.float32,[None,fcl[0][0]])
        y=tf.placeholder(tf.float32,[None, 2])
        kp1=tf.placeholder(tf.float32)
        kp2=tf.placeholder(tf.float32)
        kp3=tf.placeholder(tf.float32)
        fc_w=[]
        fc_b=[]
        fc_fn=[]
        fc=[]
        for itr in range(len(fcl)):
            fc_w.append(self.my_weigh(fcl[itr]))
            fc_b.append(self.my_bias([fcl[itr][1]]))
            if(itr==0):
                fc_fn.append(tf.matmul(x,fc_w[itr])+fc_b[itr])
            else:
                fc_fn.append(tf.matmul(fc[itr-1],fc_w[itr])+fc_b[itr])
            fc.append(self.my_actv(fc_fn[itr]))
        nFcl=len(fcl)

        ce=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y,logits=fc[nFcl-1]))
        #ce=-tf.reduce_mean(fc2*y)
        ts=tf.train.AdamOptimizer(1e-2).minimize(ce)
        
        correct_prediction = tf.equal(tf.argmax(fc[nFcl-1],1), tf.argmax(y,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        
        
        sess=tf.Session()
        sess.run(tf.global_variables_initializer())
        
        train_data_t,train_vali,train_idx,train_clr=self.ReadExcelFile(fileName,classIdx=fcl[0][0])
        data_t,vali,idx,clr=self.ReadExcelFile(valiName,classIdx=fcl[0][0])
        
        tdata=np.transpose(data_t)
        data,maxa,mini=self.Norm(data_t)
        train_data,tmaxa,tmini=self.Norm(train_data_t)
        st=time.clock()
        for itr in range(3000):
            rd,rv=self.GenTrainData(train_data,train_vali,train_idx,30)
            sess.run(ts,feed_dict={x:rd,y:rv,kp1:1,kp2:1,kp3:1})
            if(itr%100==0):
                self.acc=sess.run(accuracy,feed_dict={x:data,y:vali,kp1:1,kp2:1,kp3:1})
                ed=time.clock()
                print("file:%s  迭代次数:%5d   准确率:%7.3f%%  用时%7.3fs"%(fileName,itr,self.acc*100,ed-st))
        
        try:
                
            mat=[]    
            for aa in [[x*0.01,y*0.01] for x in range(10,90) for y in range(10,90)]:
                mat.append(aa)   
            rmat=sess.run(fc[nFcl-1],feed_dict={x:mat,kp1:1,kp2:1,kp3:1})
            rmat=np.transpose(rmat)
    
            X,Y=np.meshgrid([(float(x)*0.01-0.1)/0.8*tmaxa[0]+tmini[0] for x in range(10,90)],[((x*0.01)-0.1)/0.8*tmaxa[1]+tmini[1] for x in range(10,90)])
            Z1=np.transpose(np.reshape(rmat[1],[len(X),len(Y)]))
            Z0=np.transpose(np.reshape(rmat[0],[len(X),len(Y)]))
            Z=Z1/(Z1+Z0)
            plydata=[]
            x = np.linspace(0,(float(90)*0.01-0.1)/0.8*tmaxa[0]+tmini[0],100)
            for ity in range(len(X)):
                for itx in range(len(X[0])):
                    if(np.abs(Z[ity][itx]-0.5)<0.02):
                        plydata.append([X[ity][itx],Y[ity][itx]])
            plydata=np.transpose(plydata)
            
            import scipy.optimize as opt
            self.fita,fitb=opt.curve_fit(self.FitFunc,plydata[0],plydata[1],[0.01,0.01,0.0,0.01,0,0.0])
            
            self.cof = np.polyfit(plydata[0],plydata[1],3)
            func=np.poly1d(self.cof)
        except:
            print("Not 2d data!")
        try:
            plt.figure(1)
            ax1=plt.subplot()
            ax1.contourf(X,Y,Z,cmap=plt.get_cmap('seismic'))
            for idx in range(len(tdata[0])):
                ax1.scatter(data_t[idx][0],data_t[idx][1],marker=clr[idx][0])
            ax1.plot(x,func(x),lw=1)
            ax1.text(0,1,'$f(x)=%20.15f+%20.15fx+%20.15fx^2$'%(self.cof[2],self.cof[1],self.cof[0]))
            ax1.text(0,0.8,'$f(x)=%fe^{%fx^2+%fx+%f}+%f+%fx$'%(self.fita[0],self.fita[1],self.fita[2],self.fita[3],self.fita[4],self.fita[5]))
                     
            ax1.plot(x,self.FitFunc(x,self.fita[0],self.fita[1],self.fita[2],self.fita[3],self.fita[4],self.fita[5]),lw=1)
        except:
            print("can not plot matrix")
            
        try:
            plt.figure(2)
            wv=[]
            for itr in range(nFcl):
                wv.append(sess.run(fc_w[itr].value()))
            self.outwv=wv
            ii=0
            for lb in self.attri[:-1]:
                plt.text(-0,ii,str(lb),horizontalalignment='right')
                ii=ii+1
            def PlotWeigh(www,layer):
                www=np.abs(www)
                mx=np.max(www)
                for idy in range(len(www)):
                    for idx in range(len(www[0])):
                        plt.plot([layer-1,layer],[idx,idy],c='b',lw=www[idy][idx]*3/mx)
                        plt.scatter([layer-1],[idx])
                        plt.scatter([layer],[idy])
                    plt.plot([layer,layer],[idx,idy],c='y',linestyle='--',lw=3)
            for itr in range(nFcl):
                #print(np.shape(wv[itr]))
                PlotWeigh(np.transpose(wv[itr]),itr+1)
        except:
            print('can not plot weigh')


        plt.show()    
    
    
    
if __name__ == '__main__':
    
    #节点数目
    #[输入层数目，隐藏层节点数，.....，隐藏层节点数，输出层节点数]
    layer=[10,8,4,2]
    #读取文件名
    fileName=r'index.xlsx'
    valiFileName=r'index.xlsx'
    #训练
    aa=Classfication(fileName,valiFileName,layer=layer)
    outFile=open('out.txt','w')
    outFile.write('Function is:\n')
    outFile.write('f(x)=%f+%f*x+%f*x^2(err:%f)\n'%(aa.cof[2],aa.cof[1],aa.cof[0],aa.acc))
    outFile.write('f(x)=%fe^{%fx+%f}+%fe^{%fx+%f}\n'%(aa.fita[0],aa.fita[1],aa.fita[2],aa.fita[3],aa.fita[4],aa.fita[5]))
    outFile.write('Weigh is:\n')
    for ity in aa.outwv:
        for it in ity:
            outFile.write(str(it)+' ')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
>>>>>>> origin/master
    