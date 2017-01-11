/*
 * mprint.c
 *
 *  Created on: 2015Äê5ÔÂ14ÈÕ
 *      Author: Cy
 */

#include <stdio.h>
#include "../mathematics.h"
#include "../mydebug.h"
#include <math.h>
void CpxMsPt(cplx **a,int n)
{
	int i,j;
	for(i=0;i<n;i++)
	{
		printf("%d:",i+1);
		for(j=0;j<n;j++)
		{
			printf("(%lf,%lf) ",(creal(a[i][j])),(cimag(a[i][j])));
		}
		printf("\n");
	}
}

void CpxMsSumPt(cplx **a,int n)
{
	int i,j;
	cplx sum=0;
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			sum=sum+fabs(creal(a[i][j]))+fabs(cimag(a[i][j]))*I;
		}
	}
	printf("Sum is (%18.13e,%18.13e)\n",(creal(sum)),(cimag(sum)));
}

void CpxPPt(cplx *a,int n)
{
	int i;
	for(i=0;i<n;i++)
	{
		printf("%d:(%lf,%lf)\n",i,creal(a[i]),cimag(a[i]));
	}
}
void DblMsPt(double **a,int n)
{
	int i,j;
	for(i=0;i<n;i++)
	{
		printf("%d:",i+1);
		for(j=0;j<n;j++)
		{
			printf("(%lf) ",(a[i][j]));
		}
		printf("\n");
	}
}
void DblPPt(double *a,int n)
{
	int i;
	for(i=0;i<n;i++)
	{
		printf("%d:%lf\n",i,(a[i]));
	}
}
void DblSpmPt(dblspm a)
{
	int i,j;
	int N,nZ;
	N=a.nRow;
	for(i=0;i<N;i++)
	{
		nZ=0;
		for(j=0;j<N;j++)
		{
			if(a.idx[a.ptr[i]+nZ]==j&&a.ptr[i]+nZ<a.ptr[i+1])
			{
				printf("%7.3lf",a.data[a.ptr[i]+nZ]);
				nZ++;
			}
			else
			{
				printf("%7.3lf",0.);
			}
		}
		printf("\n");
	}
}
void CpxSpmPt(cpxspm a)
{
	int i,j;
	int N,nZ;
	N=a.nRow;
	for(i=0;i<N;i++)
	{
		nZ=0;
		for(j=0;j<N;j++)
		{
			if(a.idx[a.ptr[i]+nZ]==j&&a.ptr[i]+nZ<a.ptr[i+1])
			{
				printf("(%7.3lf,%7.3lf)",creal(a.data[a.ptr[i]+nZ]),cimag(a.data[a.ptr[i]+nZ]));
				nZ++;
			}
			else
			{
				printf("(%7.3lf,%7.3lf)",0.,0.);
			}
		}
		printf("\n");
	}
}
