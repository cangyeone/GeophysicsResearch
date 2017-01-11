/*
 * calcoff.c
 *
 *  Created on: 2015Äê10ÔÂ29ÈÕ
 *      Author: Cy
 */


#include "unionfunc.h"
#include "stdlib.h"
#include "scilib/mathematics.h"

void CalCoff(elasticpar *epar,double RPS[2],int SN,cplx Mw,double k,double omega,double r,int n,cplx *re)
{
	int i;

	poppar *ppar;
	cpxm *EH,*EV;
	cplx qSH[2],qPS[3][2];

	double j0,j1,j2;
	double dj0,dj1,dj2;

	j0=besselj(k*r,0);
	j1=besselj(k*r,1);
	j2=besselj(k*r,2);
	dj0=dBesselj(k*r,0);
	dj1=dBesselj(k*r,1);
	dj2=dBesselj(k*r,2);




	EH=(cpxm *)malloc(sizeof(cpxm)*n);
	EV=(cpxm *)malloc(sizeof(cpxm)*n);


	for(i=0;i<n;i++)
	{
		EH[i]=CpxMInit(2,2);
		EV[i]=CpxMInit(4,4);
	}

	ppar=GetPoppar(epar,k,omega,n);

	GetPopm(ppar,k,omega,n,EH,EV);

	GetQ(ppar,EH,EV,k,omega,n,SN,qSH,qPS);

	re[0]=2/r*qSH[1]*j2+qPS[2][0]*k*dj2;
	re[1]=1/r*qSH[0]*j1+qPS[1][0]*k*dj1;
	re[2]=(-RPS[0]*qPS[2][0]+RPS[1]*qPS[0][0])*k*dj0;

	re[3]=qSH[1]*k*dj2+2/r*qPS[2][0]*j2;
	re[4]=qSH[0]*k*dj1+1/r*qPS[1][0]*j1;

	re[5]=qPS[2][1]*k*j2;
	re[6]=qPS[1][1]*k*j1;
	re[7]=(RPS[1]*qPS[0][1]-RPS[0]*qPS[2][1])*k*j0;

	for(i=0;i<n;i++)
	{
		CpxMFree(EH[i]);
		CpxMFree(EV[i]);
	}
	free(EH);
	free(EV);

	free(ppar);
}
