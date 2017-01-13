/*
 * main.c
 *
 *  Created on: 2015Äê8ÔÂ12ÈÕ
 *      Author: Cy
 */


#include "scilib/mathematics.h"
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>


int N=100;
int iterN=3000,itVal=30;
double lambda=1;
double mu=1;
double rho=0.5;
double dt=0.01;
double dl=1;



void NewField(vect2m ut1,vect2m ut2,vect2m ut3)
{
	int i,j;
	double n2u,u,n3u,n1u;
	double tpl,tpl2;
	double ux1,uy1,ux2,uy2,ux3,uy3;
	double lambda1,mu1;
	n1u=lambda+mu;
	n2u=lambda+2*mu;
	n3u=lambda+3*mu;
	u=mu;
	tpl=dt*dt/(dl*dl*rho);
	tpl2=dt*dt/(dl*dl*rho);
	for(i=1;i<N-1;i++)
	{
		for(j=1;j<N-1;j++)
		{
			//if(j<0)
			{
				lambda1=0.5*lambda;
				mu1=0.4*mu;
				n1u=lambda1+mu1;
				n2u=lambda1+2*mu1;
				n3u=lambda1+3*mu1;
				u=mu1;
			}
			//else
			{
				n1u=lambda+mu;
				n2u=lambda+2*mu;
				n3u=lambda+3*mu;
				u=mu;
			}
			ux1=ut2[i][j+1].x-2*ut2[i][j].x+ut2[i][j-1].x;
			ux2=ut2[i+1][j].x-2*ut2[i][j].x+ut2[i-1][j].x;
			ux3=ut2[i+1][j].x-ut2[i+1][j-1].x-ut2[i][j].x+ut2[i][j-1].x;

			uy1=ut2[i+1][j].y-2*ut2[i][j].y+ut2[i-1][j].y;
			uy2=ut2[i][j+1].y-2*ut2[i][j].y+ut2[i][j-1].y;
			uy3=ut2[i][j+1].y-ut2[i][j].y-ut2[i-1][j+1].y+ut2[i-1][j].y;
			ut3[i][j].x=tpl*(u*ux2+n2u*ux1)+tpl2*n1u*uy3+2*ut2[i][j].x-ut1[i][j].x;
			ut3[i][j].y=tpl*(u*uy2+n2u*uy1)+tpl2*n1u*ux3+2*ut2[i][j].y-ut1[i][j].y;
		}
	}
}

void Vect2Swap(vect2m v1,vect2m v2)
{
	vect2 *a;
	a=(vect2 *)malloc(sizeof(vect2)*N*N);
	memcpy(a,v1[0],sizeof(vect2)*N*N);
	memcpy(v1[0],v2[0],sizeof(vect2)*N*N);
	memcpy(v2[0],a,sizeof(vect2)*N*N);
	free(a);
}
void Vect2Cpy(vect2m v1,vect2m v2)
{
	memcpy(v2[0],v1[0],sizeof(vect2)*N*N);
}


void Source(vect2m ut,int n)
{
	double t;
	double f0=1,Tc=4.;
	int i;
	int mid;
	int nSpd;
	int fLen;
	double dn,per;
	dn=(double)n;
	mid=(int)(N/2)-15;
	fLen=(int)(N/3);
	per=50.;
/*
	for(i=0;i<fLen;i++)
	{
		nSpd=(int)(iterN/N*4);

		if((n-nSpd*i)>0)
		{
			t=((n-nSpd*i)/per);
		}
		else
		{
			t=0;
		}
		if(t<Tc&&t>0)
		{
			ut[mid][mid+i].x=(1+cos(2.*Pi*(t-Tc/2.)/Tc))*cos(2.*Pi*f0*(t-Tc/2.))*10;
			ut[mid][mid+i].y=(1+cos(2.*Pi*(t-Tc/2.)/Tc))*cos(2.*Pi*f0*(t-Tc/2.))*50;
			ut[mid][mid+1+i].x=-(1+cos(2.*Pi*(t-Tc/2.)/Tc))*cos(2.*Pi*f0*(t-Tc/2.))*50;
			ut[mid+1][mid+1+i].y=-(1+cos(2.*Pi*(t-Tc/2.)/Tc))*cos(2.*Pi*f0*(t-Tc/2.))*50;
		}
		else
		{
			ut[mid][mid].x=0.;
			ut[mid][mid].y=0.;
		}

		if((n-nSpd*i)>0&&(n-nSpd*i)<2)
		{
			t=((n-nSpd*i)/per);

			ut[mid][mid+i].x=0.5;
			ut[mid][mid+i].y=1;
			ut[mid+1][mid+i].x=-0.5;
			ut[mid+1][mid+i].y=-1;
		}
	}*/

	if(n==1)
	{
		ut[mid][mid-5].x=0.5;
		ut[mid][mid-5].y=1;
		ut[mid+1][mid-5].x=-0.5;
		ut[mid+1][mid-5].y=-1;

		ut[mid][mid+5].x=0.5;
		ut[mid][mid+5].y=1;
		ut[mid+1][mid+5].x=-0.5;
		ut[mid+1][mid+5].y=-1;
	}
	else if(n==30)
	{
		//ut[mid][mid+20].x=0;
		//ut[mid][mid+20].y=0;
	}
	else
	{
		//ut[mid][mid].x=0;
		//ut[mid][mid].y=0;
	}/**/
}
void TimeDomainIter(FILE *out,FILE *out1)
{
	vect2m ut1,ut2,ut3,*result;
	int i,j,iter,itRst,itRstN;
	int per=1;
	ut1=Vect2MInit(N,N);
	ut2=Vect2MInit(N,N);
	ut3=Vect2MInit(N,N);
	itRst=0;
	itRstN=1;
	result=(vect2m *)malloc(sizeof(vect2m)*itRstN);
	for(i=0;i<itRstN;i++)result[i]=Vect2MInit(N,N);

	for(iter=0;iter<iterN;iter++)
	{
		Source(ut2,iter);


		for(i=0;i<N/per;i++)
		{
			for(j=0;j<N/per;j++)
			{
				result[0][i][j].x=ut2[i*per][j*per].x;
				result[0][i][j].y=ut2[i*per][j*per].y;
			}
		}



		NewField(ut1,ut2,ut3);
		Vect2Cpy(ut2,ut1);
		Vect2Cpy(ut3,ut2);

		if(iter%itVal==1)
		{
			printf("%fpercnet\n",100*(double)(iter)/(double)(iterN));
	/////////////////////////////////////////////
		fprintf(out,"frame\n");
		for(i=0;i<N/per;i++)
		{
			for(j=0;j<N/per;j++)
			{
				fprintf(out,"%lf,%lf,%lf,%lf\n",(double)i*per*dl,(double)j*per*dl,result[0][i*per][j*per].x,result[0][i*per][j*per].y);
			}
		}
	///////////////////////////////////////////////
		fprintf(out1,"frame\n");
		for(i=0;i<N/per;i++)
		{
			fprintf(out1,"lines\n");
			for(j=0;j<N/per;j++)
			{
				if(j<=N/per/2)
				{
				fprintf(out1,"%lf,%lf\n",(double)(i)*per*dl+result[0][j*per][i*per].y,(double)(j)*per*dl+dl*0.5+result[0][j*per][i*per].x);
				}
				else
				{
					fprintf(out1,"%lf,%lf\n",(double)(i)*per*dl+result[0][j*per][i*per].y,(double)j*per*dl+dl*0.5+result[0][j*per][i*per].x);
				}
				if(j==N/per/2)
					fprintf(out1,"%lf,%lf\n",(double)(i)*per*dl+result[0][j*per][i*per].y,(double)(j)*per*dl+dl*0.5+result[0][j*per][i*per].x);
			}
		}
		for(i=0;i<N/per;i++)
		{
			fprintf(out1,"lines\n");
			for(j=0;j<N/per;j++)
			{
				if(i<=N/per/2)
				{
				fprintf(out1,"%lf,%lf\n",(double)(j)*per*dl+result[0][i*per][j*per].y,(double)(i)*per*dl+dl*0.5+result[0][i*per][j*per].x);
				//fprintf(out1,"%lf,%lf\n",(double)(j)*per*dl+result[iter][i*per][j*per].y,(double)(i)*per*dl+result[iter][i*per][j*per].x);
				}
				else
				{
					fprintf(out1,"%lf,%lf\n",(double)j*per*dl+result[0][i*per][j*per].y,(double)i*per*dl+dl*0.5+result[0][i*per][j*per].x);
				}
				if(i==N/per/2)
					fprintf(out1,"%lf,%lf\n",(double)(j)*per*dl+result[0][i*per][j*per].y,(double)(i)*per*dl+dl*0.5+result[0][i*per][j*per].x);
			}
		}


	}

	}
	for(i=0;i<itRstN;i++)Vect2MFree(result[i]);
	free(result);
	Vect2MFree(ut1);
	Vect2MFree(ut2);
	Vect2MFree(ut3);
}

int main(void)
{
	FILE *out,*out1;
	out=fopen("frame.txt","w");
	out1=fopen("lines.txt","w");
	TimeDomainIter(out,out1);
	return 0;
}
