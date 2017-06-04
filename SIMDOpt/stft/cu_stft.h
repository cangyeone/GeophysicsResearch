#pragma once
#ifndef CU_STFT_H_
#define CU_STFT_H_
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <cuda_runtime.h>
#include <cufft.h>
#include <cufftXt.h>
// Complex data type
typedef float2 Complex;
#if defined (__cplusplus)
extern "C" {
#endif
	void my_cufft(Complex *h_signal, int SIGNAL_SIZE);
	Complex *my_stft(Complex *h_signal, int s_size, int w_lag, int s_len);
	
#if defined (__cplusplus)
}
#endif

#endif/*CU_STFT_H_*/