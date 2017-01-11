/*
 * popm.c
 *
 *  Created on: 2015Äê10ÔÂ28ÈÕ
 *      Author: Cy
 */


#include "unionfunc.h"
#include "scilib/mathematics.h"
#include "scilib/mydebug.h"
#include <stdlib.h>
#include <math.h>
poppar *GetPoppar(elasticpar *epar,double k,double omega,int n)
{
	int i;
	cplx a,b,v,r;

	poppar *repar;


	repar=(poppar *)malloc(sizeof(poppar)*n);
	for(i=0;i<n;i++)
	{
		a=repar[i].a=sqrt((epar[i].n+epar[i].u*2)/epar[i].p);
		b=repar[i].b=sqrt((epar[i].u)/epar[i].p);
		v=repar[i].v=csqrt(k*k-(omega/b)*(omega/b));
		r=repar[i].r=csqrt(k*k-(omega/a)*(omega/a));
		repar[i].x=2*k*k-(omega/b)*(omega/b);
		repar[i].u=epar[i].u;
		repar[i].h=epar[i].h;
		//if(creal(v)<0)repar[i].v=-v;
		//if(creal(r)<0)repar[i].r=-r;
	}
	return repar;
}

void GetPopm(poppar *ppar,double k,double omega,int n,cpxm *EH,cpxm *EV)
{
	int i;
	for(i=0;i<n;i++)
	{
		EV[i][0][0]=ppar[i].a*k/omega;
		EV[i][1][0]=ppar[i].a*ppar[i].r/omega;
		EV[i][2][0]=-2*ppar[i].a*ppar[i].u*ppar[i].r*k/omega;
		EV[i][3][0]=-ppar[i].a*ppar[i].u*ppar[i].x/omega;


		EV[i][0][1]=ppar[i].b*ppar[i].v/omega;
		EV[i][1][1]=ppar[i].b*k/omega;
		EV[i][2][1]=-ppar[i].b*ppar[i].u*ppar[i].x/omega;
		EV[i][3][1]=-2*ppar[i].b*ppar[i].u*ppar[i].v*k/omega;


		EV[i][0][2]=EV[i][0][0];
		EV[i][1][2]=-EV[i][1][0];
		EV[i][2][2]=-EV[i][2][0];
		EV[i][3][2]=EV[i][3][0];

		EV[i][0][3]=EV[i][0][1];
		EV[i][1][3]=-EV[i][1][1];
		EV[i][2][3]=-EV[i][2][1];
		EV[i][3][3]=EV[i][3][1];
		//CpxMsSetI(EV[i],4);

		EH[i][0][0]=EH[i][0][1]=1.;
		EH[i][1][0]=-ppar[i].u*ppar[i].v;
		EH[i][1][1]=-EH[i][1][0];
		//CpxMsSetI(EH[i],2);

	}
}
