/*
Cangye@hotmail.com
2017/04/28
*/


#include <stdio.h>
#include <math.h>

int main(void){
    double x, y, t;
    for (y = -1.5; y <= 4.5; y += sqrt(2) * 0.1, putchar('\n') )
        for (x = -2.5; x <= 2.5; x += sqrt(2) * 0.05){
                t = (x > 0) ? (-atan(y/x)) :- (-atan(y/x)+3.1415*2);
                (2 - 2*sin(t) + (sqrt(fabs(cos(t)))*sin(t))/(1.4 + sin(t)) >
                 sqrt(x*x+y*y)) ? 
                putchar(' ') : putchar('x');
        }
}

