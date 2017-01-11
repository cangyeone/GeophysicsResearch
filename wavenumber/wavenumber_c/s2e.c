/*
 * s2e.c
 *
 *  Created on: 2015Äê7ÔÂ20ÈÕ
 *      Author: Cy
 */

#include "unionfunc.h"
#include "scilib/mathematics.h"
#include <math.h>
#include "scilib/mydebug.h"
/*
static void GetEsr(empar dp,cplx us[3][5],cplx ur[3][5],cplx te[4][5],double k,double w,cplx *es,cplx *er)
{
	int i;
	double kk,ww;
	cplx pd,L,M,C,pf;
	cplx pr1,pr2,pr3,pr4,pr5;
	M=dp.M;
	pd=dp.pd;
	L=dp.L;
	C=dp.C;
	pf=dp.pf;
	kk=k*k;ww=w*w;

	pr1=I*(kk*M-pd*ww);
	pr2=L*dp.u*pd*ww*w*C;
	pr3=L*dp.u*pd*ww*ww*w*pf;
	pr4=I*M;
	pr5=I*L*L*dp.u*pd*pd*ww*ww;
	for(i=0;i<5;i++)
	{
		es[i]=(pr1*k*te[0][i]-pr2*kk*us[0][i]+pr3*us[0][i]-pr2*k*ur[1][i]-k*pr4*te[2][i])/pr5;
		er[i]=(pr3*ur[0][i]-pr1*te[1][i]+pr2*k*us[1][i]+pr2*ur[2][i]+te[3][i]*pr4)/pr5;
	}
}

static void GetEta(cplx a,cplx b,cplx c,cplx eta[2])
{
	cplx sqbac,sqa1,sqa2;
	sqbac=csqrt(b*b-4*a*c);
	sqa1=csqrt((-b-sqbac)/(2*a));
	sqa2=csqrt((-b+sqbac)/(2*a));

	if(creal(sqa1)>=0) eta[0]=sqa1;
	else               eta[0]=-sqa1;

	if(creal(sqa2)>=0) eta[1]=sqa2;
	else               eta[1]=-sqa2;

}

static void GetCpEm(empar dp,poppar ppar,cplx Pu[5],cplx Pd[5],cplx eta[4],cplx aa[5][4],\
		cplx usu[3][5],cplx uru[3][5],cplx usd[3][5],cplx urd[3][5],\
		cplx cf,double w,double k,cplx A[5][4])
{
	int i;
	cplx Mt[4][4],invMt[4][4],B[5][4];
	cplx par1;
	double kk;
	double h;
	cplx r,rr;
	h=ppar.h;
	r=ppar.r;
	rr=r*r;
	kk=k*k;
	par1=I*kk*dp.M/(dp.L*dp.u*dp.pd*w*w*w);
	for(i=0;i<2;i++)
	{
		Mt[0][i]=1;
		Mt[0][i+2]=cexp(-eta[i]*h);
		Mt[1][i]=cexp(-eta[i]*h);
		Mt[1][i+2]=1;
		Mt[2][i]=par1*(kk*Mt[0][i]-eta[i]*eta[i]*Mt[0][i]);
		Mt[2][i+2]=par1*(kk*Mt[0][i+2]-eta[i]*eta[i]*Mt[0][i+2]);
		Mt[3][i]=par1*(kk*Mt[1][i]-eta[i]*eta[i]*Mt[1][i]);
		Mt[3][i+2]=par1*(kk*Mt[1][i+2]-eta[i]*eta[i]*Mt[1][i+2]);
	}
	for(i=0;i<5;i++)
	{
		B[i][0]=cf*aa[i][0]+cf*aa[i][2]*cexp(-r*h);
		B[i][1]=cf*aa[i][0]*cexp(-r*h)+cf*aa[i][2];
		B[i][2]=-par1*(B[i][0]-r*r*B[i][0])+dp.C*k*(k*usu[0][i]+uru[1][i])-0.1*k*Pu[i];
		B[i][3]=-par1*(B[i][1]-r*r*B[i][1])+dp.C*k*(k*usd[0][i]+urd[1][i])-0.1*k*Pd[i];
	}
	CpxM4inv(Mt,invMt);
	for(i=0;i<5;i++)
	{
		CpxM4P4(invMt,B[i],A[i]);
	}
}


static void GetTe(cplx A[5][4],cplx aa[5][4],cplx eta[2],cplx cf,cplx r,double h,double z,cplx te[4][5])
{
	int i,j;
	cplx rr;
	rr=r*r;
	for(i=0;i<5;i++)
	{
		te[0][i]=0;
		for(j=0;j<2;j++)
		{
			te[0][i]=te[0][i]+A[i][j]*cexp(-eta[j]*z);
			te[0][i]=te[0][i]+A[i][j+2]*cexp(-eta[j]*(h-z));
		}
		te[0][i]=te[0][i]-cf*aa[i][0]*cexp(-r*(z))-cf*aa[i][2]*cexp(-r*(h-z));
	}
	/////////////
	for(i=0;i<5;i++)
	{
		te[1][i]=0;
		for(j=0;j<2;j++)
		{
			te[1][i]=te[1][i]+A[i][j]*cexp(-eta[j]*z)*(-eta[j]);
			te[1][i]=te[1][i]+A[i][j+2]*cexp(-eta[j]*(h-z))*(eta[j]);
		}
		te[1][i]=te[1][i]-cf*aa[i][0]*cexp(-r*(z))*(-r)-cf*aa[i][2]*cexp(-r*(h-z))*(r);
	}
	for(i=0;i<5;i++)
	{
		te[2][i]=0;
		for(j=0;j<2;j++)
		{
			te[2][i]=te[2][i]+A[i][j]*cexp(-eta[j]*z)*(eta[j]*eta[j]);
			te[2][i]=te[2][i]+A[i][j+2]*cexp(-eta[j]*(h-z))*(eta[j]*eta[j]);
		}
		te[2][i]=te[2][i]-cf*aa[i][0]*cexp(-r*(z))*(rr)-cf*aa[i][2]*cexp(-r*(h-z))*(r);
	}
	for(i=0;i<5;i++)
	{
		te[3][i]=0;
		for(j=0;j<2;j++)
		{
			te[3][i]=te[3][i]+A[i][j]*cexp(-eta[j]*z)*(-eta[j]*eta[j]*eta[j]);
			te[3][i]=te[3][i]+A[i][j+2]*cexp(-eta[j]*(h-z))*(eta[j]*eta[j]*eta[j]);
		}
		te[3][i]=te[3][i]-cf*aa[i][0]*cexp(-r*(z))*(-r*rr)-cf*aa[i][2]*cexp(-r*(h-z))*(r*rr);
	}
}


void GetE(empar *epar,poppar *ppar,cpxm *EH,cpxm *EV,cplx *GRH,cpxm *GRV,cplx ah[5],cplx av[5][2],int n,int Nlayer,double k,double w,cplx *et,cplx *es,cplx *er)
{
	int i,j;
	double apha;
	cplx a,b,c,d;
	cplx r,rr,kr,v;
	cplx pd,L,M,C;
	cplx aa[5][4];

	cplx A[5][4],eta[4],egv[4];
	cplx te[4][5],cf;
	cplx E11[2][2],E12[2][2],E21[2][2],E22[2][2],Mu[2][2],Md[2][2];

	cplx Pu[5],Pd[5];
	cplx utd[3][5],usd[3][5],urd[3][5],utu[3][5],usu[3][5],uru[3][5];
	apha=sqrt(epar[Nlayer].H/epar[Nlayer].p);
	M=epar[Nlayer].M;
	pd=epar[Nlayer].pd;
	L=epar[Nlayer].L;
	C=epar[Nlayer].C;
	r=ppar[Nlayer].r;
	v=ppar[Nlayer].v;
	rr=r*r;
	kr=k*k-r*r;
	double kk,ww;
	kk=k*k;
	ww=w*w;
	a=M;
	b=(pd*w*w-2*kk*M);
	c=kk*kk*a-kk*pd*ww-L*L*epar[Nlayer].u*pd*pd*ww*ww;
	d=apha*L*pd*I*ww*w*epar[Nlayer].u*(C*kr*kr-epar[Nlayer].pf*ww*kr);
	cf=d/(a*rr*rr+b*rr+c);
	egv[0]=-r;egv[1]=-v;egv[2]=r;egv[3]=v;

	GetEta(a,b,c,eta);
	GetYn(ppar,EH,EV,GRH,GRV,ah,av,n,Nlayer,utd,usd,urd,utu,usu,uru);

	CpxMquard2(EV[Nlayer],E11,E12,E21,E22);
	CpxEKREK(ppar[Nlayer],E21,GRV[Nlayer],E22,Mu,0);
	CpxEKREKd(ppar[Nlayer],E21,GRV[Nlayer],E22,Md,0);
	for(i=0;i<5;i++)
	{
		Pu[i]=av[i][0]*Mu[1][0]+av[i][1]*Mu[1][1];
		Pd[i]=av[i][0]*Md[1][0]+av[i][1]*Md[1][1];
	}
	for(i=0;i<5;i++)
	{
		for(j=0;j<2;j++)
		{
			aa[i][j]=av[i][j];
			aa[i][j+2]=GRV[Nlayer-1][j][0]*av[i][0]+GRV[Nlayer-1][j][1]*av[i][1];
		}

	}
	GetCpEm(epar[Nlayer],ppar[Nlayer],Pu,Pd,eta,aa,\
			usu,uru,usd,urd,\
			cf,w,k,A);
	GetTe(A,aa,eta,cf,ppar[Nlayer].r,ppar[Nlayer].h,0,te);
	for(i=0;i<5;i++)
	{

		et[i]=I*epar[Nlayer].pf*w*utu[0][i]/(L*pd);
	}
	GetEsr(epar[Nlayer],usd,urd,te,k,w,es,er);
}

*/
