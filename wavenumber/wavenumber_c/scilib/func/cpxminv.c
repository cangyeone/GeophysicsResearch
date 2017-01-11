#include "../mathematics.h"
#include "../const.h"
#include <string.h>
#include <stdlib.h>
cplx *cge;

static inline void lineAdd(cplx *a,cplx *b,cplx cst,int n)
		{
			int i;
			for(i=0;i<n;i++)
			{
				a[i]=a[i]+b[i]*cst;
			}

		}
static inline void lineDevide(cplx *a,cplx b,int n)
		{
			int i;
			for(i=0;i<n;i++)
			{
				a[i]=a[i]/b;
			}
		}
static void lineChange(cplx *a,cplx *b,int n)
{
	int ct;
	ct=sizeof(cplx)*n;
	memcpy(cge,b,ct);
	memcpy(b,a,ct);
	memcpy(a,cge,ct);
}

int CpxMinv(cplx **aa2,int n,cplx **c2)
{
	cplx diag,lineHead;
	cplx **a2;
	int i,j,k,n2;
	n2=n*n;
	a2=CpxMInit(n,n);
	cge=(cplx *)malloc(sizeof(cplx)*n);
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
		while(cabs(diag)<PRECISION)
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
	CpxMFree(a2);
	return 1;
}
