/*
 * parameter.c
 *
 *  Created on: 2015Äê10ÔÂ28ÈÕ
 *      Author: Cy
 */


#include "unionfunc.h"
#include <stdlib.h>
elasticpar *GetPar(int n)
{
	int i;
	elasticpar *re;
	re=(elasticpar *)malloc(sizeof(elasticpar)*n);
	for(i=0;i<n;i++)
	{
		re[i].n=10e1;
		re[i].u=10e1;
		re[i].p=3e3;
		re[i].h=4;
	}
	for(i=0;i<n;i++)
	{
		re[i].n=17.79e9*1e6;
		re[i].u=17.79e9*1e6;
		re[i].p=4650*1e18;
		re[i].h=0.05;
	}
	return re;

}
