/*
 * main.c
 *
 *  Created on: 2015Äê10ÔÂ27ÈÕ
 *      Author: Cy
 */


#include "unionfunc.h"
#include <stdio.h>
#include <time.h>
#include <math.h>
#include <sys/types.h>
#include <unistd.h>
//pid_t fork(void);

void calst(int N,double per,cplx *st)
{
	int i;
	double t;
	double f0=4,Tc=1;
	for(i=per;i<N;i++)
	{
		t=((double)(i-per))/per;
		if(t<Tc)
		{
			st[i]=(1+cos(2.*Pi*(t-Tc/2.)/Tc))*cos(2.*Pi*f0*(t-Tc/2.))/2.+0.I;
		}
		else
		{
			st[i]=0.;
		}
	}
}

int main(void)
{

	cplx **outFrquency,**outTimeDomain;
	cplx *vct3;
	double m[3][3];

	int N=1000;

	int i,j;
	int start,end,sumclock=0;
	double og;
	double per=40;
	FILE *fp1,*fp2;
	fp1=fopen("seismic.txt","w");
	fp2=fopen("frquency.txt","w");

	outFrquency=CpxMInit(4,N);
	outTimeDomain=CpxMInit(4,N);

	vct3=CpxPInit(3);

	for(i=0;i<3;i++)
	{
		for(j=0;j<3;j++)
		{
			m[i][j]=0;
		}
	}
	m[1][2]=100;
	m[2][1]=100;
	//m[2][2]=100;

	calst(N,per,outTimeDomain[0]);
	mydft(outTimeDomain[0],N,outFrquency[0],0);
////////////////////////=================================///////////////////////////////
	//pid=fork();
	//if(pid==0)

	for(i=1;i<N;i++)
	{
		start=clock();
		og=(double)(i)*per/N;
		GetVect(m,outFrquency[0][i],og,6,vct3);
		for(j=1;j<4;j++)outFrquency[j][i]=vct3[j-1];
		end=clock();
		sumclock=sumclock+(end-start);
		printf("Dot:%d,timeuse:%6.3lf totaluse:%6.3lf           \n",i,(double)(end-start)/CLOCKS_PER_SEC,(double)sumclock/CLOCKS_PER_SEC);
	}

////////////////////////==================================////////////////////////////

	for(i=0;i<4;i++)
	{
		mydft(outFrquency[i],N,outTimeDomain[i],1);
	}

/////////////////////////////////////////////////////
	for(i=1;i<N;i++)
	{
		fprintf(fp1,"%e,",(double)i/per);
		for(j=0;j<4;j++)
		{
			fprintf(fp1,"%e,",creal(outTimeDomain[j][i]));
		}
		fprintf(fp1,"\n");
	}
/////////////////////////////////////////////////////////////
	for(i=1;i<N;i++)
	{
		fprintf(fp2,"%e,",(double)i/per);
		for(j=1;j<4;j++)
		{
			fprintf(fp2,"%e,",creal(outFrquency[j][i]));
		}
		fprintf(fp2,"\n");
	}


	CpxPFree(vct3);

	CpxMFree(outFrquency);
	CpxMFree(outTimeDomain);

	return 1;
}
