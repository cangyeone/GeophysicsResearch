/*
 * initmatrix.c
 *
 *  Created on: 2015Äê5ÔÂ9ÈÕ
 *      Author: Cy
 */
#include "../mathematics.h"
#include <stdlib.h>
cplx **CpxMInit(int m,int n)
{
	cplx **re;
	int i;
	cplx *tm;
	tm=(cplx *)calloc(sizeof(cplx),m*n);
	re=(cplx **)malloc(sizeof(cplx *)*m);
	for(i=0;i<m;i++)
	{
		re[i]=&tm[i*n];
	}
	return re;
}

void CpxMFree(cplx **a)
{
	free(a[0]);
	free(a);
}

cplx *CpxPInit(int n)
{
	cplx *re;
	re=(cplx *)calloc(sizeof(cplx),n);
	return re;
}

void CpxPFree(cplx *a)
{
	free(a);
}



double **DblMInit(int m,int n)
{
	double **re;
	int i;
	double *tm;
	tm=(double *)calloc(sizeof(double),m*n);
	re=(double **)malloc(sizeof(double *)*m);
	for(i=0;i<m;i++)
	{
		re[i]=&tm[i*n];
	}
	return re;
}

void DblMFree(double **a)
{
	free(a[0]);
	free(a);
}

double *DblPInit(int n)
{
	double *re;
	re=(double *)calloc(sizeof(double),n);
	return re;
}

void DblPFree(double *a)
{
	free(a);
}

vect2 **Vect2MInit(int m,int n)
{
	vect2 **re;
	int i;
	vect2 *tm;
	tm=(vect2 *)calloc(sizeof(vect2),m*n);
	re=(vect2 **)malloc(sizeof(vect2 *)*m);
	for(i=0;i<m;i++)
	{
		re[i]=&tm[i*n];
	}
	return re;
}

void Vect2MFree(vect2 **a)
{
	free(a[0]);
	free(a);
}

