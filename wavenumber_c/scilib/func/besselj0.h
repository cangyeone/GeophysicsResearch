/*
 * besselj0.h
 *
 *  Created on: 24/12/2014
 *      Author: CY
 */

#ifndef BESSELJ0_H_
#define BESSELJ0_H_
#include <math.h>
double besselj0(double x)
{
	double ax,x1,x2,theta,fct;
	double besselj0;
	double a[7]={1.00000000,-2.24999970,1.26562080,-0.31638660,0.04444790,-0.00394440,0.00021000};
	double b[7]={0.79788456,-0.00000077,-0.00552740,-0.00009512,0.00137237,-0.00072805,0.00014476};
	double c[7]={-0.78539816,-0.04166397,-0.00003954, 0.00262573,-0.00054125,-0.00029333,0.00013558};
	ax=fabs(x);
	if(ax<=3)
	{
		x2=(ax/3.0)*(ax/3.0);
		besselj0=a[0]+x2*(a[1]+x2*(a[2]+x2*(a[3]+x2*(a[4]+x2*(a[5]+x2*a[6])))));
	}
	else
	{
		x1=3.0/ax;
		fct=b[0]+x1*(b[1]+x1*(b[2]+x1*(b[3]+x1*(b[4]+x1*(b[5]+x1*b[6])))));
		theta=ax+c[0]+x1*(c[1]+x1*(c[2]+x1*(c[3]+x1*(c[4]+x1*(c[5]+x1*c[6])))));
		besselj0=fct*cos(theta)/sqrt(ax);
	}

	return besselj0;
}

#endif /* BESSELJ0_H_ */
