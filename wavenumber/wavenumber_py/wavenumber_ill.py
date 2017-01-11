# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 09:16:54 2017

@author: Cangye
"""

import numpy as np
from scipy import special
from scipy import integrate
ctype='complex64'
class WaveNumber():
    def __init__(self):
        print("start:")
    def GetPar(self):
        self.par=[]
        for ii in range(10):
            self.par.append([2,2,1,1])
            #stands for lambda mu rho height
    def GetMatrixE(self,omega,k):
        def GetV(a):
            aa=np.sqrt(a[0]+2*a[1]/a[2],dtype=ctype)
            bb=np.sqrt(a[1]/a[2],dtype=ctype)
            r =np.sqrt(k*k-omega*omega/aa/aa,dtype=ctype)
            v =np.sqrt(k*k-omega*omega/bb/bb,dtype=ctype)
            return [aa,bb,r,v,k*k+v*v]
        self.par_v=list(map(GetV,self.par))
       
        self.E_SH=[]
        self.E_PV=[]
        self.K_rv=[]
        for itr in range(len(self.par_v)):
            a=self.par_v[itr][0]
            b=self.par_v[itr][1]
            r=self.par_v[itr][2]
            v=self.par_v[itr][3]
            x=self.par_v[itr][4]
            u=self.par[itr][1]
            self.E_SH.append(np.array( [[   1,  1]
                                       ,[-u*v,u*v]],dtype=ctype))
            self.E_PV.append(np.array( [[       a*k,       b*v,      a*k,       b*v]
                                       ,[       a*r,       b*k,     -a*r,      -b*k]
                                       ,[-2*a*u*k*r,    -b*u*x,2*a*u*k*r,     b*u*x]
                                       ,[    -a*u*x,-2*b*u*k*v,   -a*u*x,-2*b*u*k*v]],dtype=ctype))
            self.K_rv.append(np.array([r,v],dtype=ctype))
    def GetMRT(self):
        emh_z=np.zeros([2,2],dtype=ctype)
        emv_z=np.zeros([4,4],dtype=ctype)
        emh_c=np.zeros([2,2],dtype=ctype)
        emv_c=np.zeros([4,4],dtype=ctype)
        emh_k=np.zeros([2,2],dtype=ctype)
        emv_k=np.zeros([4,4],dtype=ctype)
        self.MRT_h=[]
        self.MRT_v=[]
        nlayer=len(self.par)
        for itr in range(nlayer-1):
            emh_z[:,0:1]=np.multiply(self.E_SH[itr+1][:,0:1], 1)
            emh_z[:,1:2]=np.multiply(self.E_SH[itr  ][:,1:2],-1)
            emv_z[:,0:2]=np.multiply(self.E_PV[itr+1][:,0:2], 1)
            emv_z[:,2:4]=np.multiply(self.E_PV[itr  ][:,2:4],-1)
            
            emh_c[:,0:1]=np.multiply(self.E_SH[itr  ][:,0:1], 1)
            emh_c[:,1:2]=np.multiply(self.E_SH[itr+1][:,1:2],-1)
            emv_c[:,0:2]=np.multiply(self.E_PV[itr  ][:,0:2], 1)
            emv_c[:,2:4]=np.multiply(self.E_PV[itr+1][:,2:4],-1)
            
            emh_k[0:1,0:1]=np.diag(np.exp([-self.K_rv[itr  ][1]*self.par[itr  ][3]]))
            emv_k[0:2,0:2]=np.diag(np.exp([-self.K_rv[itr  ][0]*self.par[itr  ][3],
                                           -self.K_rv[itr  ][1]*self.par[itr  ][3]]))
            
            if(itr!=nlayer-2):
                emh_k[1:2,1:2]=np.diag(np.exp([-self.K_rv[itr+1][1]*self.par[itr+1][3]]))
                emv_k[2:4,2:4]=np.diag(np.exp([-self.K_rv[itr+1][0]*self.par[itr+1][3],
                                               -self.K_rv[itr+1][1]*self.par[itr+1][3]]))
            else:
                emh_k[1:2,1:2]=np.diag([0])
                emv_k[2:4,2:4]=np.diag([0,0])
            
            emh_inv=np.linalg.inv(emh_z)
            emv_inv=np.linalg.inv(emv_z)
            
            if(np.abs(np.sum(np.dot(emv_inv,emv_z)))>5):
                print("Ill contidioned matrix!")
                #print(emv_z)
                print("line1/line4:")
                print(np.divide(emv_z[0,:],emv_z[3,:]))
                #print("-----------------")
                #print(np.dot(emv_inv,emv_z))

                
            self.MRT_h.append(np.dot(np.dot(emh_inv,emh_c),emh_k))
            self.MRT_v.append(np.dot(np.dot(emv_inv,emv_c),emv_k))


    def GetGRT(self,ns):
        self.Th=[]
        self.Rh=[]
        self.Tv=[]
        self.Rv=[]

        Eh21inv=np.multiply(np.linalg.inv(self.E_SH[0][1:2,0:1]),-1)
        Eh22=self.E_SH[0][1:2,1:2]
        Kh=np.diag(-np.exp([-self.K_rv[0][1]*self.par[0][3]]))
        Rh_t=np.dot(np.dot(Eh21inv,Eh22),Kh)
        Ev21inv=np.multiply(np.linalg.inv(self.E_PV[0][2:4,0:2]),-1)
        Ev22=self.E_PV[0][2:4,2:4]
        Kv=np.diag(-np.exp(np.exp([-self.K_rv[0][0]*self.par[0][3],
                                   -self.K_rv[0][1]*self.par[0][3]])))
        Rv_t=np.dot(np.dot(Ev21inv,Ev22),Kv)
        Th_t=np.zeros([1,1])
        Tv_t=np.zeros([2,2])
        self.Th.append(Th_t)
        self.Rh.append(Rh_t)
        self.Tv.append(Tv_t)
        self.Rv.append(Rv_t)
        for itr in range(ns):
            Th_d =self.MRT_h[itr][0:1,0:1]
            Th_u =self.MRT_h[itr][1:2,1:2]
            Rh_ud=self.MRT_h[itr][0:1,1:2]
            Rh_du=self.MRT_h[itr][1:2,0:1]
            Ih=np.diag([1])
            Tv_d =self.MRT_v[itr][0:2,0:2]
            Tv_u =self.MRT_v[itr][2:4,2:4]
            Rv_ud=self.MRT_v[itr][0:2,2:4]
            Rv_du=self.MRT_v[itr][2:4,0:2]
            Iv=np.diag([1,1])
            
            IRRhinv=np.linalg.inv(np.subtract(Ih,np.dot(Rh_du,Rh_t)))
            Th_t=np.dot(IRRhinv,Th_u)
            Rh_t=np.add(Rh_ud,np.dot(np.dot(Th_d,Rh_t),Th_t))
            
            IRRvinv=np.linalg.inv(np.subtract(Iv,np.dot(Rv_du,Rv_t)))
            Tv_t=np.dot(IRRvinv,Tv_u)
            Rv_t=np.add(Rv_ud,np.dot(np.dot(Tv_d,Rv_t),Tv_t))
            #print(IRRvinv)
            #print(self.MRT_v[itr])
            self.Th.append(Th_t)
            self.Rh.append(Rh_t)
            self.Tv.append(Tv_t)
            self.Rv.append(Rv_t)
        Th_t=np.zeros([1,1])
        Tv_t=np.zeros([2,2])
        Rh_t=np.zeros([1,1])
        Rv_t=np.zeros([2,2])
        #self.Th.append(Th_t)
        #self.Rh.append(Rh_t)
        #self.Tv.append(Tv_t)
        #self.Rv.append(Rv_t)
        for itr in range(len(self.MRT_h)-1,ns-1,-1):
            Th_d =self.MRT_h[itr][0:1,0:1]
            Th_u =self.MRT_h[itr][1:2,1:2]
            Rh_ud=self.MRT_h[itr][0:1,1:2]
            Rh_du=self.MRT_h[itr][1:2,0:1]
            Ih=np.diag([1])
            Tv_d =self.MRT_v[itr][0:2,0:2]
            Tv_u =self.MRT_v[itr][2:4,2:4]
            Rv_ud=self.MRT_v[itr][0:2,2:4]
            Rv_du=self.MRT_v[itr][2:4,0:2]
            Iv=np.diag([1,1])
            
            IRRhinv=np.linalg.inv(np.subtract(Ih,np.dot(Rh_ud,Rh_t)))
            Th_t=np.dot(IRRhinv,Th_d)
            Rh_t=np.add(Rh_du,np.dot(np.dot(Th_u,Rh_t),Th_t))
            
            IRRvinv=np.linalg.inv(np.subtract(Iv,np.dot(Rv_ud,Rv_t)))
            Tv_t=np.dot(IRRvinv,Tv_d)
            Rv_t=np.add(Rv_du,np.dot(np.dot(Tv_u,Rv_t),Tv_t))

            self.Th.append(Th_t)
            self.Rh.append(Rh_t)
            self.Tv.append(Tv_t)
            self.Rv.append(Rv_t)
        
    def GetK(self,j,z):
        rv=self.K_rv[j]
        h =self.par[j][3]
        z1=z
        z2=h-z
        Khu=np.diag(np.exp([-rv[1]*z1]))
        Khd=np.diag(np.exp([-rv[1]*z2]))
        Kvu=np.diag(np.exp([-rv[0]*z1,-rv[1]*z1]))
        Kvd=np.diag(np.exp([-rv[0]*z2,-rv[1]*z2]))
        return [Khu,Khd,Kvu,Kvd]
    def GetY(self,j,z,ns):
        Eh11=self.E_SH[j][0:1,0:1]
        Eh12=self.E_SH[j][0:1,1:2]
        Ev11=self.E_PV[j][0:2,0:2]
        Ev12=self.E_PV[j][0:2,2:4]
        K=self.GetK(j,z)
        TPh1=np.dot(np.dot(Eh11,K[1]),self.Rh[j-1])
        TPh2=np.dot(Eh12,K[0])
        TPv1=np.dot(np.dot(Ev11,K[3]),self.Rv[j-1])
        TPv2=np.dot(Ev12,K[2])
        TPh=np.add(TPh1,TPh2)
        TPv=np.add(TPv1,TPv2)
        
        for itr in range(j,ns,1):
            TPh=np.dot(TPh,self.Th[itr])
            TPv=np.dot(TPv,self.Tv[itr])
        Ehu=np.diag(np.exp([-self.K_rv[ns][1]*self.par[ns][3]/2]))
        Ehd=np.diag(np.exp([-self.K_rv[ns][1]*self.par[ns][3]/2]))
        Evd=np.diag(np.exp([-self.K_rv[ns][0]*self.par[ns][3]/2,
                            -self.K_rv[ns][1]*self.par[ns][3]/2]))
        Evu=np.diag(np.exp([-self.K_rv[ns][0]*self.par[ns][3]/2,
                            -self.K_rv[ns][1]*self.par[ns][3]/2]))
        sp=len(self.Rh)-1
        ERERh1=np.dot(Ehu,self.Rh[sp])
        ERERh2=np.dot(Ehd,self.Rh[ns-1])
        ERERh= np.subtract(np.diag([  1]),np.dot(ERERh1,ERERh2))
        ERERv1=np.dot(Evu,self.Rv[sp])
        ERERv2=np.dot(Evd,self.Rv[ns-1])
        ERERv= np.subtract(np.diag([1,1]),np.dot(ERERv1,ERERv2))
        TPh=np.dot(TPh,np.linalg.inv(ERERh))
        TPv=np.dot(TPv,np.linalg.inv(ERERv))
        return (TPh,TPv,Ehu,Ehd,Evu,Evd)
    def GetQ(self,j,z,ns,omega,k,mt):
        a=self.par_v[ns][0]
        b=self.par_v[ns][1]
        r=self.par_v[ns][2]
        v=self.par_v[ns][3]
        #x=self.par_v[ns][4]
        u=self.par[ns][1]
        fSH=1/(2*u*v)
        buaw=b/(2*u*a*omega)
        #f1=np.multiply(buaw/r,np.array([k*b,-a*r],dtype=ctype))
        #f0=np.multiply(buaw/v,np.array([b*v,-a*k],dtype=ctype))
        sSH=fSH
        s2=np.multiply(buaw*k/r,np.array([     k*b,       -a*r],dtype=ctype))
        s1=np.multiply(buaw/v,np.array(  [-2*k*v*b,(k*k+v*v)*a],dtype=ctype))
        s0=np.multiply(buaw,np.array(    [     r*b,       -k*a],dtype=ctype))
        """
        x=0
        y=1
        z=2
        FSH2=[0,0]
        FSH1=[0,0]
        FPS2=[0,0]
        FPS1=[0,0]
        FSH2[0]=(( mt[y][y]-mt[x][x])*1j-2*mt[x][y])/4
        FSH2[1]=(-(mt[y][y]-mt[x][x])*1j-2*mt[x][y])/4
        FSH1[0]=(  mt[y][z]+mt[x][z]*1j)/2
        FSH1[1]=( -mt[y][z]+mt[x][z]*1j)/2
        FPS2[0]=(( mt[x][x]-mt[y][y])-mt[x][y]*2j)/4
        FPS2[1]=(( mt[x][x]-mt[y][y])+mt[x][y]*2j)/4
        FPS1[0]=(  mt[y][z]*1j-mt[x][z])/2
        FPS1[0]=(  mt[y][z]*1j+mt[x][z])/2
        FPS01  =(  mt[x][x]+mt[y][y])/2
        FPS02  =   mt[z][z]
        """
        Yh,Yv,Ehu,Ehd,Evu,Evd=self.GetY(j,z,ns)
        ERh =np.dot(Ehu,self.Rh[ns])
        Ih=np.diag([1])
        Iv=np.diag([1,1])
        qSH2=np.dot(np.dot(Yh,np.add(Ih,ERh)),k*sSH)
        qSH1=np.dot(np.dot(Yh,np.subtract(Ih,ERh)),v*sSH)
      
        ERv =np.dot(Evu,self.Rv[ns])
        qPS2=np.dot(np.dot(Yv,np.add(ERv,Iv)),     np.transpose(s2))
        qPS1=np.dot(np.dot(Yv,np.subtract(ERv,Iv)),np.transpose(s1))
        qPS0=np.dot(np.dot(Yv,np.add(ERv,Iv)),     np.transpose(s0))
        return (qSH2,qSH1,qPS2,qPS1,qPS0)
    def GetR(self,theta,m):
        o=theta
        x=0
        y=1
        z=2
        RSH2= (m[y][y]-m[x][x])/2*np.sin(2*o)+m[x][y]*np.cos(2*o)
        RSH1=m[x][z]*np.sin(o)-m[y][z]*np.cos(o)
        RPS2=-(m[y][y]-m[x][x])/2*np.cos(2*o)+m[x][y]*np.sin(2*o)
        RPS1=m[x][z]*np.cos(o)+m[y][z]*np.sin(o)
        RPS01=(m[x][x]+m[y][y])/2
        RPS02=m[z][z]
        return (RSH2,RSH1,RPS2,RPS1,RPS01,RPS02)
    def IntKernel(self,j,z,ns,omega,k,r,mt):
        qSH2,qSH1,qPS2,qPS1,qPS0=self.GetQ(j,z,ns,omega,k,mt)
        x=k*r
        j2=special.jn(2,x)
        j2p=(special.jn(1,x)-special.jn(3,x))/2
        j1=special.jn(1,x)
        j1p=(special.jn(0,x)-special.jn(2,x))/2
        j0=special.jn(0,x)
        j0p=special.jn(-1,x)
        #print(self.GetQ(j,z,ns,omega,k,mt))
        kr1=2*qSH2*j2/r+qPS2[0]*k*j2p
        kr2=1/r*qSH1*j1+qPS1[0]*k*j1p
        kr3=-qPS2[0]*j0p*k
        kr4=qPS0[0]*j0p*k

        ko1=qSH2*k*j2p+2/r*qPS2[0]*j2
        ko2=qSH1*k*j1p+1/r*qPS1[0]*j1
        
        kz1=qPS2[1]*k*j2
        kz2=qPS1[1]*k*j1
        kz3=qPS0[1]*k*j0
        kz4=-qPS2[1]*k*j0
        return (kr1,kr2,kr3,kr4,ko1,ko2,kz1,kz2,kz3,kz4)
    def IntInK(self,j,z,ns,omega,theta,r,mt,amp):
        def FormLine(k):
            
            self.GetPar()
            self.GetMatrixE(omega,k)
            self.GetMRT()
            self.GetGRT(ns)
            self.GetY(j,z,ns)
            kr1,kr2,kr3,kr4,ko1,ko2,kz1,kz2,kz3,kz4=self.IntKernel(j,z,ns,omega,k,r,mt)
            #except:
                #print(k,omega)
                #kr1,kr2,kr3,kr4,ko1,ko2,kz1,kz2,kz3,kz4=(0j,0j,0j,0j,0j,0j,0j,0j,0j,0j)
            return [kr1[0,0],kr2[0,0],kr3,kr4,ko1[0,0],ko2[0,0],kz1,kz2,kz3,kz4]
        kint=np.linspace(0.001,20*np.sqrt(1.5),2000,dtype=ctype)

        kl=np.array(list(map(FormLine,kint)),dtype=ctype)
      
        kl=np.transpose(kl)
        ksm=np.multiply(np.sum(kl,axis=1),20/2000)

        RSH2,RSH1,RPS2,RPS1,RPS01,RPS02=self.GetR(theta,mt)
        ur=amp*(RPS2*ksm[0]-RPS1*ksm[1]+RPS01*ksm[2]+RPS02*ksm[3])
        uo=amp*(RSH2*ksm[4]+RSH1*ksm[5])
        uz=amp*(RPS2*ksm[6]+RPS1*ksm[7]+RPS02*ksm[8]+RPS01*ksm[9])
        return (ur,uo,uz)
    def FourTrans(self,wave,j,z,ns,theta,r,mt):
        fm=np.fft.fft(wave)
        omega=np.linspace(0.001,1/0.01,len(wave),dtype=ctype)
        def FDget(w):
            if(w%10==0):
                print("omega dot %6d/%6d"%(w,len(wave)))
            ur,uo,uz=self.IntInK(j,z,ns,omega[w],theta,r,mt,fm[w])
            return [ur,uo,uz]
        ary=list(map(FDget,range(len(wave))))
        return np.abs(np.fft.ifft(np.transpose(ary),axis=1))
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    aa=WaveNumber()
    mt=[[1,1,1],[1,1,1],[1,1,1]]
    wave=np.linspace(0,0,20)
    wave[10]=100
    ls=aa.FourTrans(wave,1,0.5,4,1,1,mt)
    plt.subplot(4,1,1)
    plt.plot(wave)
    plt.text(0,max(wave)*0.5,r"Wave")
    plt.subplot(4,1,2)
    plt.plot(ls[0])
    plt.text(0,ls[0][0],r"Component:r")
    plt.subplot(4,1,3)
    plt.plot(ls[1])
    plt.text(0,ls[1][0],r"Component:$\theta$")
    plt.subplot(4,1,4)
    plt.plot(ls[2])
    plt.text(0,ls[2][0],r"Component:z")
