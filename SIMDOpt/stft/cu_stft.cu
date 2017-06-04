/*
* Copyright 1993-2015 NVIDIA Corporation.  All rights reserved.
*
* Please refer to the NVIDIA end user license agreement (EULA) associated
* with this source code for terms and conditions that govern your use of
* this software. Any use, reproduction, disclosure, or distribution of
* this software and related documentation outside the terms of the EULA
* is strictly prohibited.
*
*/

/*
* Copyright 1993-2014 NVIDIA Corporation.  All rights reserved.
*
* Please refer to the NVIDIA end user license agreement (EULA) associated
* with this source code for terms and conditions that govern your use of
* this software. Any use, reproduction, disclosure, or distribution of
* this software and related documentation outside the terms of the EULA
* is strictly prohibited.
*
*/

/* Example showing the use of CUFFT for fast 1D-convolution using FFT. */

// includes, system
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

// includes, project

#include <cuda_runtime.h>
#include <cufft.h>
#include <cufftXt.h>
//#include <helper_functions.h>
//#include <helper_cuda.h>
#include "cu_stft.h"
// Complex data type
////////////////////////////////////////////////////////////////////////////////
void my_cufft(Complex *h_signal, int SIGNAL_SIZE)
{
	// Allocate device memory for signal
	int mem_size = sizeof(Complex)*SIGNAL_SIZE;
	Complex *d_signal;
	cudaMalloc((void **)&d_signal, mem_size);
	// Copy host memory to device
	cudaMemcpy(d_signal, h_signal, mem_size,
		cudaMemcpyHostToDevice);

	cudaMemcpy(h_signal, d_signal, mem_size,
		cudaMemcpyDeviceToHost);
	// CUFFT plan simple API
	cufftHandle plan;
	cufftPlan1d(&plan, SIGNAL_SIZE, CUFFT_C2C, 1);
	// CUFFT plan advanced API
	cufftExecC2C(plan, (cufftComplex *)d_signal, (cufftComplex *)d_signal, CUFFT_FORWARD);
	cudaMemcpy(h_signal, d_signal, mem_size,
		cudaMemcpyDeviceToHost);
	//Destroy CUFFT context
	cufftDestroy(plan);
	cudaFree(d_signal);
}

Complex *my_stft(Complex *h_signal, int s_size, int w_lag, int s_len)
{
	// Allocate device memory for signal
	//int mem_size = sizeof(Complex)*SIGNAL_SIZE;
	int x_size = (int)((s_size - s_len) / w_lag);
	int y_size = s_len;
	int stft_size = sizeof(Complex)*x_size*y_size;
	int mem_size = sizeof(Complex)*s_size;
	Complex *d_signal;
	cudaMalloc((void **)&d_signal, mem_size);
	// Copy host memory to device
	cudaMemcpy(d_signal, h_signal, mem_size,
		cudaMemcpyHostToDevice);
	Complex *d_stft;
	cudaMalloc((void **)&d_stft, stft_size);
	//cudaMemcpy(h_signal, d_signal, mem_size,
		//cudaMemcpyDeviceToHost);
	// CUFFT plan simple API
	cufftHandle plan;
	cufftPlan1d(&plan, s_len, CUFFT_C2C, 1);
	// CUFFT plan advanced API
	for (int i = 0; i < x_size; i++)
	{
		cufftExecC2C(plan, (cufftComplex *)d_signal+i, (cufftComplex *)d_stft+i*y_size, CUFFT_FORWARD);
	}
	Complex *h_stft;
	h_stft = (Complex *)malloc(sizeof(Complex)*stft_size);
	cudaMemcpy(h_stft, d_stft, stft_size,
		cudaMemcpyDeviceToHost);
	//Destroy CUFFT context
	cufftDestroy(plan);
	cudaFree(d_signal);
	cudaFree(d_stft);
	return h_stft;
}