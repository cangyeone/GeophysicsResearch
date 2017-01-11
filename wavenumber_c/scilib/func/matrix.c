/*
 * matrix.c
 *
 *  Created on: 2015Äê5ÔÂ9ÈÕ
 *      Author: Cy
 */
#include "../mathematics.h"

void CpxMMs(cplx **a,cplx **b,int n,cplx **c)
{
	int i,j,k;
	register cplx temp;
	for(k=0;k<n;k++)
	{
		for(i=0;i<n;i++)
		{
			temp=a[i][k];
			for(j=0;j<n;j++)
			{
				c[i][j]+=temp*b[k][j];
			}
		}
	}
}
void CpxMPs(cplx **a,cplx *b,int n,cplx *c)
{
	int i,j;
	cplx temp;
	for(i=0;i<n;i++)
	{
		temp=0;
		for(j=0;j<n;j++)
		{
			temp=temp+a[i][j]*b[j];
		}
		c[i]=temp;
	}
}
void CpxMTs(cplx **a,int n,cplx **c)
{
	int i,j;
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			c[i][j]=a[j][i];
		}
	}
}
void CpxMTsc(cplx **a,int n)
{
	int i,j;
	cplx temp;
	for(i=0;i<n-1;i++)
	{
		for(j=i+1;j<n;j++)
		{
			temp=a[i][j];
			a[i][j]=a[j][i];
			a[j][i]=temp;
		}
	}
}
cplx CpxPP(cplx *a,cplx *b,int n)
{
	int i;
	cplx re;
	re=0;
	for(i=0;i<n;i++)
	{
		re=re+a[i]*b[i];
	}
	return re;
}
void CpxCMsc(double b,int n,cplx **a)
{
	int i,j;
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			a[i][j]=a[i][j]*b;
		}
	}
}



void DblMMs(double **a,double **b,int n,double **c)
{
	int i,j,k;
	double temp;
	for(k=0;k<n;k++)
	{
		for(i=0;i<n;i++)
		{
			temp=a[i][k];
			for(j=0;j<n;j++)
			{
				c[i][j]+=temp*b[k][j];
			}
		}
	}
}
void DblMPs(double **a,double *b,int n,double *c)
{
	int i,j;
	double temp;
	for(i=0;i<n;i++)
	{
		temp=0;
		for(j=0;j<n;j++)
		{
			temp=temp+a[i][j]*b[j];
		}
		c[i]=temp;
	}
}
void DblMTs(double **a,int n,double **c)
{
	int i,j;
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			c[i][j]=a[j][i];
		}
	}
}
void DblMTsc(double **a,int n)
{
	int i,j;
	double temp;
	for(i=0;i<n-1;i++)
	{
		for(j=i+1;j<n;j++)
		{
			temp=a[i][j];
			a[i][j]=a[j][i];
			a[j][i]=temp;
		}
	}
}
double DblPP(double *a,double *b,int n)
{
	int i;
	double re;
	re=0;
	for(i=0;i<n;i++)
	{
		re=re+a[i]*b[i];
	}
	return re;
}
void DblCMsc(double b,int n,double **a)
{
	int i,j;
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			a[i][j]=a[i][j]*b;
		}
	}
}
void DblCP(double *a,double b,int n,double *c)
{
	int i;
	for(i=0;i<n;i++)
	{
		a[i]=c[i]*b;
	}
}
void DblCPc(double b,int n,double *a)
{
	int i;
	for(i=0;i<n;i++)
	{
		a[i]=a[i]*b;
	}
}
