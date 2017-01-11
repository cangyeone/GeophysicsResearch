#include "../mathematics.h"
#include <stdlib.h>
dblspm DblMtoSpm(double **a,int m,int n)
{
	dblspm b;
	int i,j;
	int nZero;
	nZero=0;
	for(i=0;i<m;i++)
	{
		for(j=0;j<n;j++)
		{
			if(a[i][j]!=0)nZero++;
		}
	}
	b.data=(double *)malloc(sizeof(double)*nZero);
	b.idx=(int *)malloc(sizeof(int)*nZero);
	b.ptr=(int *)malloc(sizeof(int)*(m+1));
	b.nRow=m;
	b.ptr[m]=nZero;
	nZero=0;
	for(i=0;i<m;i++)
	{
		b.ptr[i]=nZero;
		for(j=0;j<n;j++)
		{
			if(a[i][j]!=0)
			{
				b.data[nZero]=a[i][j];
				b.idx[nZero]=j;
				nZero++;
			}
		}
	}
	return b;
}

void DblSpmMV(dblspm a,double *b,double *c)
{
	int i,j;
	int nRow;
	double tData;
	nRow=a.nRow;
	for(i=0;i<nRow;i++)
	{
		tData=0.;
		for(j=a.ptr[i];j<a.ptr[i+1];j++)
		{
			tData=tData+a.data[j]*b[a.idx[j]];
		}
		c[i]=tData;
	}
}

double DblSpmIdx(dblspm a,int i,int j)
{
	int ii;
	double re;
	for(ii=a.ptr[i];ii<a.ptr[i+1];ii++)
	{
		if(a.idx[ii]==j)re=a.data[ii];
	}
	//re=0;
	return re;
}


///////////////////////////////////////


cpxspm CpxMtoSpm(double _Complex **a,int m,int n)
{
	cpxspm b;
	int i,j;
	int nZero;
	nZero=0;
	for(i=0;i<m;i++)
	{
		for(j=0;j<n;j++)
		{
			if(a[i][j]!=0)nZero++;
		}
	}
	b.data=(cplx *)malloc(sizeof(cplx)*nZero);
	b.idx=(int *)malloc(sizeof(int)*nZero);
	b.ptr=(int *)malloc(sizeof(int)*(m+1));
	b.nRow=m;
	b.ptr[m]=nZero;
	nZero=0;
	for(i=0;i<m;i++)
	{
		b.ptr[i]=nZero;
		for(j=0;j<n;j++)
		{
			if(a[i][j]!=0)
			{
				b.data[nZero]=a[i][j];
				b.idx[nZero]=j;
				nZero++;
			}
		}
	}
	return b;
}

void CpxSpmMV(cpxspm a,cplx *b,cplx *c)
{
	int i,j;
	int nRow;
	cplx tData;
	nRow=a.nRow;
	for(i=0;i<nRow;i++)
	{
		tData=0.;
		for(j=a.ptr[i];j<a.ptr[i+1];j++)
		{
			tData=tData+a.data[j]*b[a.idx[j]];
		}
		c[i]=tData;
	}
}

double CpxSpmIdx(cpxspm a,int i,int j)
{
	int ii;
	cplx re;
	for(ii=a.ptr[i];ii<a.ptr[i+1];ii++)
	{
		if(a.idx[ii]==j)re=a.data[ii];
	}
	//re=0;
	return re;
}

