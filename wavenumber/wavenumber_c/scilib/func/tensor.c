/*
 * tensor.c
 *
 *  Created on: 2015Äê5ÔÂ9ÈÕ
 *      Author: Cy
 */


#include "../mathematics.h"
#include "../const.h"
#include <math.h>
inline double ModVect2(vect2 a)
{
	double re;
	re=sqrt(a.x*a.x+a.y*a.y);
	return re;
}
inline double ModVect(vect a)
{
	double re;
	re=sqrt(a.x*a.x+a.y*a.y+a.z*a.z);
	return re;
}
inline double AngVect2(vect2 a)
{
	double re,len;
	len=sqrt(a.x*a.x+a.y*a.y);
	if(len==0)return 0;
	re=acos(a.x/len);
	if(a.y<0)re=2*Pi-re;
	return re;
}
inline double Vect2DotVect2(vect2 a,vect2 b)
{
	return (a.x*b.x+a.y*b.y);
}
inline vect2 RotVect2(vect2 a,double theta)
{
	vect2 re;
	double si,co;
	si=sin(theta);
	co=cos(theta);
	re.x=a.x*co-a.y*si;
	re.y=a.x*si+a.y*co;
	return re;
}
inline int QuadVect2(vect2 a)
{
	if(a.x>0&&a.y>0)return 1;
	else if(a.x<0&&a.y>0)return 2;
	else if(a.x<0&&a.y<0)return 3;
	else if(a.x>0&&a.y<0)return 4;
	else return 0;
}
inline vect2 GenVect2(vect2 a,double mod)
{
	double len;
	len=sqrt(a.x*a.x+a.y*a.y);
	a.x=a.x/len;
	a.y=a.y/len;
	a.x=a.x*mod;
	a.y=a.y*mod;
	return a;
}
inline vect2 ZeroVect2()
{
	vect2 re;
	re.x=0;
	re.y=0;
	return re;
}
inline vect2 OppVect2(vect2 a)
{
	a.x=-a.x;
	a.y=-a.y;
	return a;
}
