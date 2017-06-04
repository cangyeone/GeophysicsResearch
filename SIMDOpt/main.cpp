
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>

#include "stft/cu_stft.h"
#include "avxfunc/afxfunc.h"
#include "io/sacread.h"
// The filter size is assumed to be a number smaller than the signal size

////////////////////////////////////////////////////////////////////////////////
// Program main
////////////////////////////////////////////////////////////////////////////////

dgVect Conv(dgVect in1, dgVect in2) {
	dgVect out;
	if (in1.len > in2.len)
	{
		out.data = (float *)calloc(sizeof(float), in1.len);
		out.len = in1.len;
		for (int i = 0; i < in1.len - in2.len; i++)
		{
			for (int j = 0; j < in2.len; j++)
			{
				out.data[i] = out.data[i] + in1.data[i] * in2.data[j];
			}
		}
	}
	return out;
}
float *CONV(float *in1, int in1len, float *in2, int in2len) {
	float *out;
	int outlen;
	if (in1len > in2len)
	{
		out = (float *)calloc(sizeof(float), in1len);
		outlen = in1len;
		for (int i = 0; i < in1len - in2len; i++)
		{
			for (int j = 0; j < in2len; j++)
			{
				out[i] = out[i] + in1[i] * in2[j];
			}
		}
	}
	return out;
}


int main(int argc, char **argv)
{
	Complex *h_signal = (Complex *)malloc(sizeof(Complex) * 1024);

	dgVect in1, in2;
	dgVect out;
	int st;
	int ed;
	in1.len = 256*256;
	in2.len = 256;
	in1.data = (float *)malloc(sizeof(float)*in1.len);
	in2.data = (float *)malloc(sizeof(float)*in2.len);
	for (int i = 0; i < in1.len; i++)
	{
		in1.data[i] = 1.;
	}
	for (int i = 0; i < in2.len; i++)
	{
		in2.data[i] = 1.;
	}
	
	for (int i = 0; i < 1024; i++)h_signal[i].x = 1, h_signal[i].y = 1;
	st = clock();
	Complex *stft_out = my_stft(h_signal, 1024, 8, 128);
	ed = clock();
	printf("cuda stft time:%fs\n", (float)(ed - st) / CLOCKS_PER_SEC);
	free(h_signal);


	st = clock();
	SacFile scFile1=SacFileRead("D:/Program/bin/win64/Debug/st01_0828.z");
	float *ft1=(float *)malloc(sizeof(float)*4096);
	CONV(scFile1.sacdata.data[0],scFile1.sacdata.length, ft1, 4096);
	SacFileClose(scFile1);
	free(ft1);
	ed = clock();
	printf("sacfile:%fs\n", (float)(ed - st) / CLOCKS_PER_SEC);

	st = clock();
	SacFile scFile = SacFileRead("D:/Program/bin/win64/Debug/st01_0828.z");
	float *ft = (float *)malloc(sizeof(float) * 4096);
	DGConvKernel(scFile.sacdata.data[0], scFile.sacdata.length, ft, 4096);
	SacFileClose(scFile);
	free(ft);
	ed = clock();
	printf("avx+sacfile:%fs\n", (float)(ed - st) / CLOCKS_PER_SEC);
	//SacFileToTxt("D:/Program/bin/win64/Debug/st01_0828.z", "D:/out.txt");
	
}
