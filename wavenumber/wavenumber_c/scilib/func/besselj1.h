/*
 * besselj1.h
 *
 *  Created on: 2014Äê12ÔÂ24ÈÕ
 *      Author: CY
 */

#ifndef BESSELJ1_H_
#define BESSELJ1_H_
#include <math.h>
double besselj1(double x)
{
    double ax,x1,x2,theta,fct;
    double besselj1;
    double sign;
    double a[7]={0.50000000,-0.56249985,0.21093573,-0.03954289,0.00443319,-0.00031761,0.00001109};
    double b[7]={0.79788456,0.00000156,0.01659667,0.00017105,-0.00249511,0.00113653,-0.00020033};
    double c[7]={-2.35619449,0.12499612,0.00005650,-0.00637879,0.00074348,0.00079824,-0.00029166};
	ax=fabs(x);
	if(ax<=3.0)
	{
		x2=(ax/3.0)*(ax/3.0);
		besselj1=x*(a[0]+x2*(a[1]+x2*(a[2]+x2*(a[3]+x2*(a[4]+x2*(a[5]+x2*a[6]))))));
	}
	else
	{
		x1=3.0/ax;
		fct=b[0]+x1*(b[1]+x1*(b[2]+x1*(b[3]+x1*(b[4]+x1*(b[5]+x1*b[6])))));
		theta=ax+c[0]+x1*(c[1]+x1*(c[2]+x1*(c[3]+x1*(c[4]+x1*(c[5]+x1*c[6])))));
		if(x>=0)sign=1.0;
		else sign=-1.0;
		besselj1=sign*fct*cos(theta)/sqrt(ax);
	}
	return besselj1;
}

#endif /* BESSELJ1_H_ */
