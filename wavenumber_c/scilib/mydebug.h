/*
 * mydebug.h
 *
 *  Created on: 2015Äê3ÔÂ31ÈÕ
 *      Author: Cy
 */

#ifndef MYDEBUG_H_
#define MYDEBUG_H_

#include <stdio.h>
#define PR(A) printf("=====" #A "====\n");
#define PRI(A) printf(#A"=%d\n",(A));
#define PRD(A) printf(#A"=%lf\n",(A));
#define PRC(A) printf(#A"=(%lf,%lf)\n",creal(A),cimag(A));



#endif /* MYDEBUG_H_ */
