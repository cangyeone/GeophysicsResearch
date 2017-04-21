//By Cangye@hotmail.com
#include <stdio.h>  
#include <immintrin.h>  
#include <avx2intrin.h>  
  
int main(int argc, char **argv)  
{  
    __m256d x;  
    __m256d y;  
    __m256d z;  
  
    double op1[4] = {11.22, 33.44, 34.23, 23.42};  
    double op2[4] = {11.22, 33.44, 34.23, 23.42};  
    double result[4];  
  
    // Load  
    x = _mm_load_pd((__m256d*)op1);  
    y = _mm_load_pd((__m256d*)op2);  
  
    // Calculate  
    z = _mm_mul_pd(x, y);   // z = x * y  
  
    // Store  
    _mm_store_si128((__m256i*)result, z);  
  
    printf("0: %d\n", result[0]);  
    printf("1: %d\n", result[1]);  
    printf("2: %d\n", result[2]);  
    printf("3: %d\n", result[3]);  
  
    return 0;  
} 