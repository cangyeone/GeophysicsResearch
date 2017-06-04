
#pragma once
#include <immintrin.h>
#if defined (__cplusplus)
extern "C" {
#endif
	struct mydgvector
	{
		float *data;
		int len;
	};
	typedef struct mydgvector dgVect;

	dgVect DgConvKernel(dgVect in1,dgVect in2);
	float *DGConvKernel(float *in1, int in1len, float *in2, int in2len);


#if defined (__cplusplus)
}
#endif
