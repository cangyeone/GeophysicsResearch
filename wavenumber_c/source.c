/*
 * source.c
 *
 *  Created on: 2015Äê10ÔÂ28ÈÕ
 *      Author: Cy
 */

#include "unionfunc.h"
#include "scilib/mathematics.h"

void GetSpar(double k,double omega,poppar dp,cplx sSH[1],cplx s0[2],cplx s1[2],cplx s2[2])
{
	cplx cpx1,cpx2;

	sSH[0]=1/(2*dp.u*dp.v);

	cpx1=dp.b/(2*dp.u*dp.a*omega);

	cpx2=cpx1*k/dp.r;
	s2[0]=cpx2*k*dp.b;
	s2[1]=-cpx2*dp.a*dp.r;
	cpx2=cpx1/dp.v;
	s1[0]=-2*cpx2*k*dp.v*dp.b;
	s1[1]=cpx2*(k*k+dp.v*dp.v)*dp.a;

	s0[0]=cpx1*dp.r*dp.b;
	s0[1]=-cpx1*k*dp.a;

}

void GetSource(double m[3][3],cplx Mw,double k,double omega,poppar dp,cplx **SH,cplx **SV)
{
	int i;
	int x,y,z;

	cplx FSH2[5],FSH1[5],FPS2[5];
	cplx FPS1[5],FPS01[5],FPS02[5];
	cplx  sSH,s0[2],s1[2],s2[2],cpx1,cpx2;

	x=0;y=1;z=2;

	for(i=0;i<5;i++)
	{
		FSH2[i]=FSH1[i]=FPS2[i]=0.;
		FPS1[i]=FPS01[i]=FPS02[i]=0.;
	}

	FSH2[3]=(I*(m[y][y]-m[x][x])-2.*m[x][y])/4.;
	FSH2[4]=(-I*(m[y][y]-m[x][x])-2.*m[x][y])/4.;
	FSH1[1]=(m[y][z]+I*m[x][z])/2.;
	FSH1[2]=(-m[y][z]+I*m[x][z])/2.;
	FPS2[3]=((m[x][x]-m[y][y])-2.*I*m[x][y])/4.;
	FPS2[4]=((m[x][x]-m[y][y])+2.*I*m[x][y])/4.;

	FPS1[1]=(I*m[y][z]-m[x][z])/2.;
	FPS1[2]=(I*m[y][z]+m[x][z])/2.;
	FPS01[0]=(m[x][x]+m[y][y])/2.;
	FPS02[0]=m[z][z];

	sSH=1/(2*dp.u*dp.v);
	cpx1=dp.b/(2*dp.u*dp.a*omega);

	cpx2=cpx1*k/dp.r;
	s2[0]=cpx2*k*dp.b;
	s2[1]=-cpx2*dp.a*dp.r;
	cpx2=cpx1/dp.v;
	s1[0]=-2*cpx2*k*dp.v*dp.b;
	s1[1]=cpx2*(k*k+dp.v*dp.v)*dp.a;

	s0[0]=cpx1*dp.r*dp.b;
	s0[1]=-cpx1*k*dp.a;

	for(i=0;i<5;i++)
	{
		SH[i][0]=Mw*(FSH2[i]*k+FSH1[i]*dp.v)*sSH;

		SV[i][0]=Mw*((FPS2[i]-FPS01[i])*s2[0]+FPS1[i]*s1[0]+FPS02[i]*s0[0]);
		SV[i][1]=Mw*((FPS2[i]-FPS01[i])*s2[1]+FPS1[i]*s1[1]+FPS02[i]*s0[1]);
	}

}
