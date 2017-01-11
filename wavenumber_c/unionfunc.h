/*
 * unionfunc.h
 *
 *  Created on: 2015Äê10ÔÂ28ÈÕ
 *      Author: Cy
 */

#ifndef UNIONFUNC_H_
#define UNIONFUNC_H_
#include "scilib/mathematics.h"
#include "scilib/mydebug.h"

struct elasticpar
{
	double n;
	double u;
	double p;
	double h;
};

struct poppar
{
	double h;
	double a;
	double b;
	cplx u;
	cplx v;
	cplx x;
	cplx r;
};

typedef struct elasticpar elasticpar;
typedef struct poppar poppar;

elasticpar *GetPar(int n);
poppar *GetPoppar(elasticpar *epar,double k,double omega,int n);
void GetPopm(poppar *ppar,double k,double omega,int n,cpxm *EH,cpxm *EV);
void GetK(poppar *dp,int n,double h,cpxm KH,cpxm KV);
void GetSource(double m[3][3],cplx Mw,double k,double omega,poppar dp,cplx **SH,cplx **SV);
void GetVect(double tensm[3][3],cplx Mw,double omega,double r,cplx *vect);
void GetMRT(poppar *dp,cpxm *EH,cpxm *EV,int n,cpxm *MRTH,cpxm *MRTV);
void GetGRT(poppar dp,cpxm EH,cpxm EV,cpxm *MRTH,cpxm *MRTV,int n,int NS,cplx *GRH,cplx *GTH,cpxm *GTV,cpxm *GRV);
void GetMRT(poppar *dp,cpxm *EH,cpxm *EV,int n,cpxm *MRTH,cpxm *MRTV);
void GetGRT(poppar dp,cpxm EH,cpxm EV,cpxm *MRTH,cpxm *MRTV,int n,int NS,cplx *GRH,cplx *GTH,cpxm *GTV,cpxm *GRV);
void GetY(poppar *dp,cpxm *EH,cpxm *EV,cpxm sh,cpxm sv,int n,int NS,cplx *ut,cplx *us,cplx *ur);
void GetSpar(double k,double omega,poppar dp,cplx sSH[1],cplx s0[2],cplx s1[2],cplx s2[2]);
void GetQ(poppar *dp,cpxm *EH,cpxm *EV,double k,double omega,int n,int NS,cplx qSH[2],cplx qPS[3][2]);
void CalCoff(elasticpar *epar,double RPS[2],int SN,cplx Mw,double k,double omega,double r,int n,cplx *re);
#endif
