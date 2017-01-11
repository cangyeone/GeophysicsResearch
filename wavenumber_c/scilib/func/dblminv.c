/*
 * dblminv.c
 *
 *  Created on: 2015Äê8ÔÂ13ÈÕ
 *      Author: Cy
 */


#include "../mathematics.h"
#include "../const.h"
#include <string.h>
#include <stdlib.h>
#include <math.h>
double *cge;

static inline void lineAdd(double *a,double *b,double cst,int n)
		{
			int i;
			for(i=0;i<n;i++)
			{
				a[i]=a[i]+b[i]*cst;
			}

		}
static inline void lineDevide(double *a,double b,int n)
		{
			int i;
			for(i=0;i<n;i++)
			{
				a[i]=a[i]/b;
			}
		}
static void lineChange(double *a,double *b,int n)
{
	int ct;
	ct=sizeof(double)*n;
	memcpy(cge,b,ct);
	memcpy(b,a,ct);
	memcpy(a,cge,ct);
}

int DblMinv(double **aa2,int n,double **c2)
{
	double diag,lineHead;
	double **a2;
	int i,j,k,n2;
	n2=n*n;
	a2=DblMInit(n,n);
	cge=(double *)malloc(sizeof(double)*n);
	for(i=0;i<n*n;i++)a2[0][i]=aa2[0][i];
	for(i=0;i<n2;i++)
	{
		c2[0][i]=0.+0.I;
	}
	for(i=0;i<n;i++)
	{
		c2[i][i]=1.+0.I;
	}


	for(i=0;i<n;i++)
	{
		diag=a2[i][i];
		k=0;
		while(fabs(diag)<PRECISION)
		{
			k++;
			if((i+k)<(n))
			{
				lineChange(a2[i],a2[i+k],n);
				lineChange(c2[i],c2[i+k],n);
			}
			else
			{
				return 0;
			}
			diag=a2[i][i];
		}
		lineDevide(a2[i],diag,n);
		lineDevide(c2[i],diag,n);
		for(j=i+1;j<n;j++)
		{
			lineHead=-a2[j][i];
			lineAdd(a2[j],a2[i],lineHead,n);
			lineAdd(c2[j],c2[i],lineHead,n);
		}
	}

	for(i=n-1;i>0;i--)
	{
		for(j=0;j<i;j++)
		{
			lineHead=-a2[j][i];
			lineAdd(a2[j],a2[i],lineHead,n);
			lineAdd(c2[j],c2[i],lineHead,n);
		}
	}
	free(cge);
	DblMFree(a2);
	return 1;
}
