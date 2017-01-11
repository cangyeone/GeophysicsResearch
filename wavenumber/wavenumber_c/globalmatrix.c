/*
 * globalmatrix.c
 *
 *  Created on: 2015Äê10ÔÂ28ÈÕ
 *      Author: Cy
 */
#include "unionfunc.h"
static void MapM(cpxm A,int x1,int x2,int y1,int y2,cpxm B)
{
	int i,j;
	for(i=y1;i<y2;i++)
	{
		for(j=x1;j<x2;j++)
		{
			B[i][j]=A[i-y1][j-x1];
		}
	}
}
static void OppMs(int n,cpxm A)
{
	int i,j;
	for(i=0;i<n;i++)
	{
		for(j=0;j<n;j++)
		{
			A[i][j]=-A[i][j];
		}
	}
}

void golbalmatrix(cpxm *SH,cpxm *SV,poppar *dp,int n,cpxm GH,cpxm GV)
 {
	 int iLayer,i,j;
	 cpxm TV,TH,KV,KH;

	 TV=CpxMInit(4,4);
	 TH=CpxMInit(2,2);
	 KV=CpxMInit(4,4);
	 KH=CpxMInit(2,2);


	 GetK(dp,0,0,KH,KV);
	 CpxMMs(SH[0],KH,2,TH);
	 CpxMMs(SV[0],KV,4,TV);

	 for(i=0;i<2;i++)
	 {
		 GH[0][i]=TH[1][i];
	 }
	 for(i=0;i<2;i++)
	 {
		 for(j=0;j<4;j++)
		 {
			 GV[i][j]=TV[i+2][j];
		 }
	 }

	 for(iLayer=0;iLayer<n-2;iLayer++)
	 {
		 GetK(dp,iLayer,dp[iLayer].h,KH,KV);
		 CpxMMs(SH[iLayer],KH,2,TH);
		 CpxMMs(SV[iLayer],KV,4,TV);
		 MapM(TH,iLayer*2,iLayer*2+2,iLayer*2+1,iLayer*2+3,GH);
		 MapM(TV,iLayer*4,iLayer*4+4,iLayer*4+2,iLayer*4+6,GV);

		 GetK(dp,iLayer+1,0,KH,KV);
		 CpxMMs(SH[iLayer+1],KH,2,TH);
		 CpxMMs(SV[iLayer+1],KV,4,TV);
		 OppMs(2,TH);
		 OppMs(4,TV);
		 MapM(TH,iLayer*2+2,iLayer*2+4,iLayer*2+1,iLayer*2+3,GH);
		 MapM(TV,iLayer*4+4,iLayer*4+8,iLayer*4+2,iLayer*4+6,GV);
	 }
	 iLayer=n-2;
	 GetK(dp,iLayer,dp[iLayer].h,KH,KV);
	 CpxMMs(SH[iLayer],KH,2,TH);
	 CpxMMs(SV[iLayer],KV,4,TV);
	 MapM(TH,iLayer*2,iLayer*2+2,iLayer*2+1,iLayer*2+3,GH);
	 MapM(TV,iLayer*4,iLayer*4+4,iLayer*4+2,iLayer*4+6,GV);

	 GetK(dp,iLayer+1,0,KH,KV);
	 CpxMMs(SH[iLayer+1],KH,2,TH);
	 CpxMMs(SV[iLayer+1],KV,4,TV);
	 OppMs(2,TH);
	 OppMs(4,TV);
	 MapM(TH,iLayer*2+2,iLayer*2+3,iLayer*2+1,iLayer*2+3,GH);
	 MapM(TV,iLayer*4+4,iLayer*4+6,iLayer*4+2,iLayer*4+6,GV);

	 CpxMFree(TV);
	 CpxMFree(TH);
	 CpxMFree(KV);
	 CpxMFree(KH);
 }
