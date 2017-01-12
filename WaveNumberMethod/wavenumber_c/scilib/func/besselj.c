/*
 *  Created on: 30/03/2015
 *      Author: Cangye
 */
#include <math.h>
#include "besselj0.h"
#include "besselj1.h"
#include "../mathematics.h"

double besselj(double x,int n)
{
	  const int iacc=40;
	  double bigno,bigni;
      bigno=10000000000.0;
      bigni=0.0000000001;
      int j,jsum,m,nn;
      double besselj;
      double ax,bj,bjm,bjp,sum,tox;
      nn=n;
      if(0==n)besselj=besselj0(x);
      else if(1==n)besselj=besselj1(x);
      else
      {
    	  if(n<0)n=-n;
    	  ax=fabs(x);
    	  if(0==ax)besselj=0.0;
    	  else if(ax>n)
    	  {
    		  tox=2.0/ax;
    		  bjm=besselj0(ax);
    		  bj=besselj1(ax);
    		  for(j=0;j<n-1;j++)
    		  {
    			  bjp=((double)(j+1))*tox*bj-bjm;
    			  bjm=bj;
    			  bj=bjp;
    		  }
    		  besselj=bj;
    	  }
    	  else
    	  {
    		  tox=2.0/ax;
    		  m=2*((n+(int)(sqrt((double)(iacc*n))))/2);
    		  besselj=0.0;
    		  jsum=0;
    		  sum=0.0;
    		  bjp=0.0;
    		  bj=1.0;
    		  for(j=m;j>=1;j--)
    		  {
    			  bjm=((double)(j))*tox*bj-bjp;
    			  bjp=bj;
    			  bj=bjm;
    			  if(fabs(bj)>bigno)
    			  {
    				  bj=bj*bigni;
    				  bjp=bjp*bigni;
    				  besselj=besselj*bigni;
    				  sum=sum*bigni;
    			  }
    			  if(jsum!=0)sum=sum+bj;
    			  jsum=1-jsum;
    			  if(j==n)besselj=bjp;
    		  }
    		  sum=2.0*sum-bj;
    		  besselj=besselj/sum;
    	  }
    	  if(x<0.0&&(n%2)==1)besselj=-besselj;
      }
      if(nn<0&&(n%2)==1)besselj=-besselj;
      return besselj;
}
double dBesselj(double x,int n)
{
	double bsl;
	double bigni=0.0000000001;
	if(fabs(x)<bigni)
	{
		bsl=(besselj(bigni,n)-besselj(0,n))/bigni;
		return bsl;
	}
	bsl=((double)n)*besselj(x,n)/x-besselj(x,n+1);
	return  bsl;
}
