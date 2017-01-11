/*
 * gettsr.c
 *
 *  Created on: 2015Äê11ÔÂ4ÈÕ
 *      Author: Cy
 */


#include "unionfunc.h"
#include <stdlib.h>
//void GetMRT(poppar *dp,cpxm *EH,cpxm *EV,int n,cpxm *MRTH,cpxm *MRTV);
//void GetGRT(poppar dp,cpxm EH,cpxm EV,cpxm *MRTH,cpxm *MRTV,int n,int NS,cplx *GRH,cplx *GTH,cpxm *GTV,cpxm *GRV);

void CpxEKREK(poppar dp,cplx A[2][2],cpxm B,cplx C[2][2],cplx D[2][2])
{
	cplx Kd[2][2],Ku[2][2],M1[2][2],M2[2][2],M3[2][2];

	CpxM2toI(Kd);
	CpxM2toI(Ku);

	Ku[0][0]=cexp(-dp.r*dp.h);
	Ku[1][1]=cexp(-dp.v*dp.h);

	M1[0][0]=A[0][0]*Kd[0][0]+A[0][1]*Kd[1][0];
	M1[0][1]=A[0][0]*Kd[0][1]+A[0][1]*Kd[1][1];
	M1[1][0]=A[1][0]*Kd[0][0]+A[1][1]*Kd[1][0];
	M1[1][1]=A[1][0]*Kd[0][1]+A[1][1]*Kd[1][1];

	M2[0][0]=M1[0][0]*B[0][0]+M1[0][1]*B[1][0];
	M2[0][1]=M1[0][0]*B[0][1]+M1[0][1]*B[1][1];
	M2[1][0]=M1[1][0]*B[0][0]+M1[1][1]*B[1][0];
	M2[1][1]=M1[1][0]*B[0][1]+M1[1][1]*B[1][1];

	M3[0][0]=C[0][0]*Ku[0][0]+C[0][1]*Ku[1][0];
	M3[0][1]=C[0][0]*Ku[0][1]+C[0][1]*Ku[1][1];
	M3[1][0]=C[1][0]*Ku[0][0]+C[1][1]*Ku[1][0];
	M3[1][1]=C[1][0]*Ku[0][1]+C[1][1]*Ku[1][1];

	D[0][0]=M2[0][0]+M3[0][0];
	D[0][1]=M2[0][1]+M3[0][1];
	D[1][0]=M2[1][0]+M3[1][0];
	D[1][1]=M2[1][1]+M3[1][1];
}

void GetERER(poppar *dp,cpxm *GRV,int NS,cplx M[2][2])
{
	cplx Eu[2][2],Ed[2][2],M1[2][2],M2[2][2];
	CpxM2toI(Eu);
	CpxM2toI(Ed);

	Eu[0][0]=cexp(-dp[NS].r*dp[NS].h/2);
	Eu[1][1]=cexp(-dp[NS].v*dp[NS].h/2);
	Ed[0][0]=cexp(-dp[NS].r*dp[NS].h/2);
	Ed[1][1]=cexp(-dp[NS].v*dp[NS].h/2);


	CpxMM2c(GRV[NS],Ed);
	CpCpxMM2(GRV[NS-1],M1);
	CpxM2M2c(Eu,Ed);
	CpxM2M2(Ed,M1,M2);
	M2[0][0]=1-M2[0][0];
	M2[0][1]=-M2[0][1];
	M2[1][0]=-M2[1][0];
	M2[1][1]=1-M2[1][1];
	CpxM2inv(M2,M);
}

void CpxM2Mc(cplx A[2][2],cpxm B)
{
	int i,j;
	cplx C[2][2];
	C[0][0]=A[0][0]*B[0][0]+A[0][1]*B[1][0];
	C[0][1]=A[0][0]*B[0][1]+A[0][1]*B[1][1];
	C[1][0]=A[1][0]*B[0][0]+A[1][1]*B[1][0];
	C[1][1]=A[1][0]*B[0][1]+A[1][1]*B[1][1];
	for(i=0;i<2;i++)
	{
		for(j=0;j<2;j++)
		{
			A[i][j]=C[i][j];
		}
	}
}

void GetQ(poppar *dp,cpxm *EH,cpxm *EV,double k,double omega,int n,int NS,cplx qSH[2],cplx qPS[3][2])
{
	int i;

	cplx E11[2][2],E12[2][2],E21[2][2],E22[2][2];
	cplx M1[2][2],YV[2][2];
	cplx YH,YH1,YH2;
	cplx Eu[2][2],ERPI[2][2],ERMI[2][2];

	cplx sSH[1],s0[2],s1[2],s2[2];

	cpxm *MRTH,*MRTV,*GTV,*GRV;
	cplx *GRH,*GTH;

	MRTH=(cpxm *)malloc(sizeof(cpxm)*(n-1));
	MRTV=(cpxm *)malloc(sizeof(cpxm)*(n-1));
	GTV=(cpxm *)malloc(sizeof(cpxm)*(n+1));
	GRV=(cpxm *)malloc(sizeof(cpxm)*(n+1));

	for(i=0;i<n-1;i++)
	{
		MRTH[i]=CpxMInit(2,2);
		MRTV[i]=CpxMInit(4,4);
	}
	for(i=0;i<n+1;i++)
	{
		GTV[i]=CpxMInit(2,2);
		GRV[i]=CpxMInit(2,2);
	}

	GRH=CpxPInit(n+1);
	GTH=CpxPInit(n+1);

	GetMRT(dp,EH,EV,n,MRTH,MRTV);
	GetGRT(dp[0],EH[0],EV[0],MRTH,MRTV,n,NS,GRH,GTH,GTV,GRV);

	CpxMquard2(EV[0],E11,E12,E21,E22);
	CpxEKREK(dp[0],E11,GRV[0],E12,M1);

	CpxM2toI(YV);
	CpxM2M2c(M1,YV);

	YH=(EH[0][0][0]*GRH[0]+EH[0][0][1]*cexp(-dp[0].v*dp[0].h));

	for(i=1;i<=NS-1;i++)
	{
		CpxMM2c(GTV[i],YV);
		YH=GTH[i]*YH;
	}

	GetERER(dp,GRV,NS,M1);
	CpxM2M2c(M1,YV);
	//PR(================);
	//CpxM2pt(M1);
	YH=YH/(1-cexp(-dp[NS].v*dp[NS].h/2)*cexp(-dp[NS].v*dp[NS].h/2)*GRH[NS]*GRH[NS-1]);

	CpxM2toI(Eu);
	Eu[0][0]=cexp(-dp[NS].r*dp[NS].h/2);
	Eu[1][1]=cexp(-dp[NS].v*dp[NS].h/2);

	YH1=YH*(1+Eu[1][1]*GRH[NS]);
	YH2=YH*(1-Eu[1][1]*GRH[NS]);

	CpxM2Mc(Eu,GRV[NS]);

	ERPI[0][0]=Eu[0][0]+1;
	ERPI[1][1]=Eu[1][1]+1;
	ERPI[1][0]=Eu[1][0];
	ERPI[0][1]=Eu[0][1];

	ERMI[0][0]=Eu[0][0]-1;
	ERMI[1][1]=Eu[1][1]-1;
	ERMI[1][0]=Eu[1][0];
	ERMI[0][1]=Eu[0][1];

	CpxM2M2c(YV,ERPI);
	CpxM2M2c(YV,ERMI);

	GetSpar(k,omega,dp[NS],sSH,s0,s1,s2);


	qSH[1]=YH1*k*sSH[0];
	qSH[0]=YH2*dp[NS].v*sSH[0];

	qPS[2][0]=ERPI[0][0]*s2[0]+ERPI[0][1]*s2[1];
	qPS[2][1]=ERPI[1][0]*s2[0]+ERPI[1][1]*s2[1];

	qPS[1][0]=ERMI[0][0]*s1[0]+ERMI[0][1]*s1[1];
	qPS[1][1]=ERMI[1][0]*s1[0]+ERMI[1][1]*s1[1];

	qPS[0][0]=ERPI[0][0]*s0[0]+ERPI[0][1]*s0[1];
	qPS[0][1]=ERPI[1][0]*s0[0]+ERPI[1][1]*s0[1];



	for(i=0;i<n-1;i++)
	{
		CpxMFree(MRTH[i]);
		CpxMFree(MRTV[i]);
	}
	for(i=0;i<n+1;i++)
	{
		CpxMFree(GTV[i]);
		CpxMFree(GRV[i]);
	}

	free(MRTH);
	free(MRTV);
	free(GTV);
	free(GRV);

	CpxPFree(GRH);
	CpxPFree(GTH);


}
