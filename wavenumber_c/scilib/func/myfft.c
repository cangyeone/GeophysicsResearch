/*
 * myfft.c
 *
 *  Created on: 30/03/2015
 *      Author: Cangye
 */
#include "../mathematics.h"
#include "../const.h"
#include <stdlib.h>
#include <string.h>


unsigned int getN(unsigned int dotN)
{
	unsigned int N,i=0;
	while(1)
	{
		i++;
		N=(1<<i);
		if(N>dotN)
			{
				break;
			}
	}
	return N;
}


void myfft(cplx *tA,unsigned int dotN,cplx *B,int sel)
{
	unsigned int N=0,NPlace,N2;
	unsigned int i=0;
	unsigned int idx,j,k,gpc,gpn,gpn2;
	cplx *Wn,*A;
	N2=(dotN>>1);
	Wn=malloc(N2*sizeof(cplx));
	A=malloc(dotN*sizeof(cplx));
	memcpy(A,tA,sizeof(cplx)*dotN);
	for(i=0;i<N2;i++)
	{
		Wn[i]=cexp(I*2*Pi*i/dotN);
	}
	i=0;
	while(1)
	{
		i++;
		N=(1<<i);
		if(N>=dotN)
			{
				NPlace=i;
				break;
			}
	}
	for(i=0;i<N;i++)
	{
		idx=0;
		for(j=0;j<NPlace;j++)
		{
			idx=idx+((((1<<j)&i)>>(j))<<(NPlace-j-1));
		}
		B[idx]=A[i];
	}


	for(i=0;i<(NPlace);i++)
	{
		gpc=(N>>(i+1));
		gpn=(1<<(i+1));
		gpn2=(1<<(i));
		for(j=0;j<gpc;j++)
		{
			for(k=0;k<gpn2;k++)
			{
				A[j*gpn+k]=B[j*gpn+k]+B[j*gpn+k+gpn2]*Wn[gpc*k];
				A[j*gpn+gpn2+k]=B[j*gpn+k]-B[j*gpn+k+gpn2]*Wn[gpc*k];
			}
		}
		memcpy(B,A,sizeof(cplx)*N);
	}
	free(Wn);
	free(A);
}

void mydft(cplx *A,int N,cplx *B,int sel)
{
	int i,j;
	cplx temp;

	switch(sel)
	{
	case 0:
		for(i=0;i<N;i++)
		{
			temp=0.+0.I;

			for(j=0;j<N;j++)
			{
				temp=temp+A[j]*cexp(-I*2.*Pi*((double)j)*((double)i)/((double)(N)));
			}

			B[i]=temp;
		}
		break;
	case 1:
		for(i=0;i<N;i++)
		{
			temp=0.+0.I;
			for(j=0;j<N;j++)
			{
				temp=temp+A[j]*cexp(I*2.*Pi*((double)j)*((double)i)/((double)(N)));
			}
			B[i]=temp/((double)N);
		}
		break;
	}
}


