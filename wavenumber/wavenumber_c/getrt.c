/*
 * getrt.c
 *
 *  Created on: 2015Äê11ÔÂ3ÈÕ
 *      Author: Cy
 */


#include "unionfunc.h"

static void ChageRows(cpxm *EH,cpxm *EV,int n,cpxm MMH,cpxm MMV)
{
	int i,j;
	cpxm EH1,EH2,EV1,EV2,invEV,invEH;
	EH1=CpxMInit(2,2);
	EH2=CpxMInit(2,2);
	EV1=CpxMInit(4,4);
	EV2=CpxMInit(4,4);
	invEH=CpxMInit(2,2);
	invEV=CpxMInit(4,4);

	for(i=0;i<2;i++)
	{
		EH1[i][0]=EH[n+1][i][0];
		EH1[i][1]=-EH[n][i][1];

		EH2[i][0]=EH[n][i][0];
		EH2[i][1]=-EH[n+1][i][1];
	}

	for(i=0;i<4;i++)
	{
		for(j=0;j<2;j++)
		{
			EV1[i][j]=EV[n+1][i][j];
			EV1[i][j+2]=-EV[n][i][j+2];

			EV2[i][j]=EV[n][i][j];
			EV2[i][j+2]=-EV[n+1][i][j+2];
		}
	}

	CpxMinv(EH1,2,invEH);
	CpxMinv(EV1,4,invEV);

	CpxMMs(invEH,EH1,2,MMH);
	CpxMMs(invEV,EV1,4,MMV);

	CpxMFree(EH1);
	CpxMFree(EH2);
	CpxMFree(EV1);
	CpxMFree(EV2);
	CpxMFree(invEV);
	CpxMFree(invEH);
}

static void GetRTK(poppar *dp,int n,cpxm KH,cpxm KV)
{
	int i;
	for(i=0;i<4;i++)KH[0][i]=0;
	for(i=0;i<16;i++)KV[0][i]=0;
	KH[0][0]=cexp(-dp[n].v*dp[n].h);
	KH[1][1]=cexp(-dp[n+1].v*dp[n+1].h);

	KV[0][0]=cexp(-dp[n].r*dp[n].h);
	KV[1][1]=cexp(-dp[n].v*dp[n].h);
	KV[2][2]=cexp(-dp[n+1].r*dp[n+1].h);
	KV[3][3]=cexp(-dp[n+1].v*dp[n+1].h);
}

void GetMRT(poppar *dp,cpxm *EH,cpxm *EV,int n,cpxm *MRTH,cpxm *MRTV)
{
	int i;
	cpxm MMH,MMV,KH,KV;
	MMH=CpxMInit(2,2);
	MMV=CpxMInit(4,4);
	KH=CpxMInit(2,2);
	KV=CpxMInit(4,4);

	for(i=0;i<n-2;i++)
	{
		ChageRows(EH,EV,i,MMH,MMV);
		GetRTK(dp,i,KH,KV);
		CpxMMs(MMH,KH,2,MRTH[i]);
		CpxMMs(MMV,KV,4,MRTV[i]);
	}

	ChageRows(EH,EV,n-2,MMH,MMV);
	GetRTK(dp,n-2,KH,KV);
	KH[1][1]=0;
	for(i=0;i<2;i++)KV[i+2][i+2]=0;

	CpxMMs(MMH,KH,2,MRTH[n-2]);
	CpxMMs(MMV,KV,4,MRTV[n-2]);/**/
	CpxMFree(MMH);
	CpxMFree(MMV);
	CpxMFree(KV);
	CpxMFree(KH);
}

void GetRTpart(cpxm A,cplx Td[2][2],cplx Rud[2][2],cplx Rdu[2][2],cplx Tu[2][2])
{
	int i,j;
	for(i=0;i<2;i++)
	{
		for(j=0;j<2;j++)
		{
			Td[i][j]=A[i][j];
			Rud[i][j]=A[i][j+2];
			Rdu[i][j]=A[i+2][j];
			Tu[i][j]=A[i+2][j+2];
		}
	}
}

void GetGRV0(cpxm EV,poppar dp,cpxm GRV0)
{
	cplx E21[2][2],E22[2][2],invE21[2][2],K[2][2];
	CpxMquard2(EV,invE21,invE21,E21,E22);
	CpxM2inv(E21,invE21);
	CpxM2Sc(-1.,invE21);
	CpxM2to0(K);
	K[0][0]=cexp(-dp.h*dp.r);
	K[1][1]=cexp(-dp.h*dp.v);
	CpxM2M2M2(invE21,E22,K,E21);
	CpCpxM2M(E21,GRV0);
}

static void GetIRR(cplx A[2][2],cpxm B,cplx C[2][2],cpxm D)
{
	cplx C1[2][2],invC1[2][2];
	C1[0][0]=1-A[0][0]*B[0][0]+A[0][1]*B[1][0];
	C1[0][1]=-A[0][0]*B[0][1]+A[0][1]*B[1][1];
	C1[1][0]=-A[1][0]*B[0][0]+A[1][1]*B[1][0];
	C1[1][1]=1-A[1][0]*B[0][1]+A[1][1]*B[1][1];
	CpxM2inv(C1,invC1);
	D[0][0]=invC1[0][0]*C[0][0]+invC1[0][1]*C[1][0];
	D[0][1]=invC1[0][0]*C[0][1]+invC1[0][1]*C[1][1];
	D[1][0]=invC1[1][0]*C[0][0]+invC1[1][1]*C[1][0];
	D[1][1]=invC1[1][0]*C[0][1]+invC1[1][1]*C[1][1];

}

static void GetRTRT(cplx A[2][2],cplx B[2][2],cpxm C,cpxm D,cpxm E)
{
	cplx M1[2][2],M2[2][2];

	M1[0][0]=B[0][0]*C[0][0]+B[0][1]*C[1][0];
	M1[0][1]=B[0][0]*C[0][1]+B[0][1]*C[1][1];
	M1[1][0]=B[1][0]*C[0][0]+B[1][1]*C[1][0];
	M1[1][1]=B[1][0]*C[0][1]+B[1][1]*C[1][1];

	M2[0][0]=M1[0][0]*D[0][0]+M1[0][1]*D[1][0];
	M2[0][1]=M1[0][0]*D[0][1]+M1[0][1]*D[1][1];
	M2[1][0]=M1[1][0]*D[0][0]+M1[1][1]*D[1][0];
	M2[1][1]=M1[1][0]*D[0][1]+M1[1][1]*D[1][1];

	E[0][0]=A[0][0]+M2[0][0];
	E[0][1]=A[0][1]+M2[0][1];
	E[1][0]=A[1][0]+M2[1][0];
	E[1][1]=A[1][1]+M2[1][1];
}

void GetGRT(poppar dp,cpxm EH,cpxm EV,cpxm *MRTH,cpxm *MRTV,int n,int NS,cplx *GRH,cplx *GTH,cpxm *GTV,cpxm *GRV)
{
	int i;

	cplx Rdu[2][2],Rud[2][2],Tu[2][2],Td[2][2];

	GetGRV0(EV,dp,GRV[0]);
	GRH[0]=-1/EH[1][0]*EH[1][1]*cexp(-dp.h*dp.v);

	for(i=1;i<=NS-1;i++)
	{
		GTH[i]=1/(1-MRTH[i-1][1][0]*GRH[i-1])*MRTH[i-1][1][1];
		GRH[i]=MRTH[i-1][0][1]+MRTH[i-1][0][0]*GRH[i-1]*GTH[i];

		GetRTpart(MRTV[i-1],Td,Rud,Rdu,Tu);
		GetIRR(Rdu,GRV[i-1],Tu,GTV[i]);
		GetRTRT(Rud,Td,GRV[i-1],GTV[i],GRV[i]);

	}

	GRH[n]=0;
	GRV[n][0][0]=GRV[n][0][1]=GRV[n][1][0]=GRV[n][1][1]=0.;
	for(i=n-1;i>=NS;i--)
	{

		GTH[i]=1/(1-MRTH[i-1][0][1]*GRH[i+1])*MRTH[i-1][0][0];
		GRH[i]=MRTH[i-1][0][1]+MRTH[i-1][1][1]*GRH[i+1]*GTH[i];

		GetRTpart(MRTV[i-1],Td,Rud,Rdu,Tu);
		GetIRR(Rud,GRV[i+1],Td,GTV[i]);
		GetRTRT(Rdu,Tu,GRV[i+1],GTV[i],GRV[i]);

	}
}



