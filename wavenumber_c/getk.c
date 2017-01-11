/*
 * getk.c
 *
 *  Created on: 2015Äê10ÔÂ28ÈÕ
 *      Author: Cy
 */


#include "unionfunc.h"
/*
void GetK(poppar *dp,int n,double z,cpxm KH,cpxm KV)
{
	cplx r,v;
	double h;
	int i;
	r=dp[n].r;
	v=dp[n].v;
	h=dp[n].h;

	//PRC(r)
	//PRC(v)
	for(i=0;i<4;i++)KH[0][i]=0.;
	for(i=0;i<16;i++)KV[0][i]=0.;

	KH[0][0]=cexp(v*(h-z));
	KH[1][1]=cexp(v*z);

	KV[0][0]=cexp(r*(h-z));
	KV[1][1]=cexp(v*(h-z));
	KV[2][2]=cexp(r*z);
	KV[3][3]=cexp(v*z);

	//PR(KV)
	//CpxMsPt(KV,4);
}

*/
void GetK(poppar *dp,int n,double z,cpxm KH,cpxm KV)
{
	cplx r,v;
	double h;
	int i;
	r=dp[n].r;
	v=dp[n].v;
	h=dp[n].h;

	//PRC(r)
	//PRC(v)
	for(i=0;i<4;i++)KH[0][i]=0.;
	for(i=0;i<16;i++)KV[0][i]=0.;

	KH[0][0]=cexp(-v*z);
	KH[1][1]=cexp(-v*(h-z));

	KV[0][0]=cexp(-r*z);
	KV[1][1]=cexp(-v*z);
	KV[2][2]=cexp(-r*(h-z));
	KV[3][3]=cexp(-v*(h-z));

	//PR(KV)
	//CpxMsPt(KV,4);
}
