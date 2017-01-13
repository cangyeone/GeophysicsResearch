/*
 * mprint.c
 *
 *  Created on: 2015Äê5ÔÂ14ÈÕ
 *      Author: Cy
 */

#include <stdio.h>
#include "../mathematics.h"

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
void CpxPPt(cplx *a,int n)
{
	int i;
	for(i=0;i<n;i++)
	{
		printf("%d:(%e,%e)\n",i,creal(a[i]),cimag(a[i]));
	}
}
