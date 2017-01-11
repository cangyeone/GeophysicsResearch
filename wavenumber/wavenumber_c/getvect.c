/*
 * getvect.c
 *
 *  Created on: 2015Äê10ÔÂ29ÈÕ
 *      Author: Cy
 */


#include "unionfunc.h"
#include <math.h>

void GetVect(double m[3][3],cplx Mw,double omega,double r,cplx *vect)
{
	elasticpar *epar;

	cplx *vct,*vct1,*sumv;

	double RPS[2],RSH[2],RPS0[2];

	double dx,dbli;
	int i,j;
	int N=2000;
	double upper=20,lower=0.001;
	int Nlayer=5;
	const int x=0,y=1,z=2;
	double theta=Pi/6;

	vct=CpxPInit(8);
	vct1=CpxPInit(8);
	sumv=CpxPInit(8);
	epar=GetPar(Nlayer);

	dx=(upper-lower)/((double)(N));


	RSH[1]=(m[y][y]-m[x][x])/2*sin(2*theta)+m[x][y]*cos(2*theta);
	RSH[0]=m[x][z]*sin(theta)-m[y][z]*cos(theta);

	RPS[1]=-(m[y][y]-m[x][x])/2*cos(2*theta)+m[x][y]*sin(2*theta);
	RPS[0]=m[x][z]*cos(theta)+m[y][z]*sin(theta);

	RPS0[0]=(m[x][x]+m[y][y])/2;
	RPS0[1]=m[z][z];

	CalCoff(epar,RPS0,3,Mw,lower,omega,r,Nlayer,vct);

	for(j=0;j<8;j++)
	{
		sumv[j]=0.+0.I;
	}


	for(i=1;i<N;i++)
	{
		dbli=((double)(i));
		CalCoff(epar,RPS0,3,Mw,(dbli+1.0)*dx+lower,omega,r,Nlayer,vct1);

		for(j=0;j<8;j++)
		{
			sumv[j]=sumv[j]+(vct[j]+vct1[j])*dx/2.0;
		}
		for(j=0;j<8;j++)vct[j]=vct1[j];
	}

	vect[0]=Mw/(2*Pi)*(RPS[1]*sumv[0]-RPS[0]*sumv[1]+sumv[2]);
	vect[1]=Mw/(2*Pi)*(RSH[1]*sumv[3]+RSH[0]*sumv[4]);
	vect[2]=-Mw/(2*Pi)*(RPS[1]*sumv[5]-RPS[0]*sumv[6]+sumv[7]);

	CpxPFree(vct);
	CpxPFree(vct1);
	CpxPFree(sumv);

}
