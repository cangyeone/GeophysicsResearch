/*
 * dblspmcg.c
 *
 *  Created on: 2015Äê9ÔÂ2ÈÕ
 *      Author: Cy
 */
#include "../mathematics.h"
#include <memory.h>
#include <math.h>
static inline void DblPmSpMP(double *a,dblspm b,double *c,double *d)
{
	int i;
	DblSpmMV(b,c,d);
	for(i=0;i<b.nRow;i++)
	{
		d[i]=a[i]-d[i];
	}
}

static inline void DblCPpP(double *a,double cst,double *b,int n,double *c)
{
	int i;
	for(i=0;i<n;i++)
	{
		c[i]=a[i]+cst*b[i];
	}

}
void DblSpmCG(dblspm A,double *f,int n,double *c)
{
	double *r,*pOld,*rOld,*Ap;
	double q,e;
	int i;

	r=DblPInit(n);
	pOld=DblPInit(n);
	rOld=DblPInit(n);
	Ap=DblPInit(n);

	for(i=0;i<n;i++)c[i]=1.;
	DblPmSpMP(f,A,c,rOld);
	DblPmSpMP(f,A,c,pOld);

	for(i=0;i<n*n;i++)
	{
		DblSpmMV(A,pOld,Ap);
		q=DblPP(rOld,rOld,n)/DblPP(pOld,Ap,n);
		DblCPpP(c,q,pOld,n,c);
		DblCPpP(rOld,-q,Ap,n,r);
		e=DblPP(r,r,n)/DblPP(rOld,rOld,n);
		if(fabs(e)<PRECISION)break;
		DblCPpP(r,e,pOld,n,pOld);
		memcpy(rOld,r,sizeof(double)*n);
	}


	DblPFree(r);
	DblPFree(pOld);
	DblPFree(rOld);
	DblPFree(Ap);
}

/////////////////////////////////////////////////
static inline void CpxPmSpMP(cplx *a,cpxspm b,cplx *c,cplx *d)
{
	int i;
	CpxSpmMV(b,c,d);
	for(i=0;i<b.nRow;i++)
	{
		d[i]=a[i]-d[i];
	}
}

static inline void CpxCPpP(cplx *a,cplx cst,cplx *b,int n,cplx *c)
{
	int i;
	for(i=0;i<n;i++)
	{
		c[i]=a[i]+cst*b[i];
	}

}
void CpxSpmCG(cpxspm A,cplx *f,int n,cplx *c)
{
	cplx *r,*pOld,*rOld,*Ap;
	cplx q,e;
	int i;//,j;

	r=CpxPInit(n);
	pOld=CpxPInit(n);
	rOld=CpxPInit(n);
	Ap=CpxPInit(n);

	for(i=0;i<n;i++)c[i]=1.;
	CpxPmSpMP(f,A,c,rOld);
	CpxPmSpMP(f,A,c,pOld);

	for(i=0;i<n*n;i++)
	{
		CpxSpmMV(A,pOld,Ap);
		q=CpxPP(rOld,rOld,n)/CpxPP(pOld,Ap,n);
		q=q*0.8;
		CpxCPpP(c,q,pOld,n,c);
		//for(j=0;j<n;j++)printf("(%lf,%lf)",creal(c[j]),cimag(c[j]));printf("\n");
		CpxCPpP(rOld,-q,Ap,n,r);
		e=CpxPP(r,r,n)/CpxPP(rOld,rOld,n);
		if((fabs(creal(e))+fabs(cimag(e)))<PRECISION)break;
		CpxCPpP(r,e,pOld,n,pOld);
		memcpy(rOld,r,sizeof(cplx)*n);
	}


	CpxPFree(r);
	CpxPFree(pOld);
	CpxPFree(rOld);
	CpxPFree(Ap);
}
