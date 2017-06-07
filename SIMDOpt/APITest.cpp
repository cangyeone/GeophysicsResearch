
////////////////////////////////////////////////////////////////////////////////
// Program main
////////////////////////////////////////////////////////////////////////////////

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>

#include "stft/cu_stft.h"
#include "avxfunc/afxfunc.h"
#include "io/sacread.h"
#include "stft/zx_fft.h"
#include "APITest.h"

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
	float tc1,tc2,temp,tcc;
	tc1 = 0;
	for (int i = 0; i < in2len; i++)tc1 += in2[i] * in2[i];
	tc1 = 1 / sqrt(tc1);
	if (in1len > in2len)
	{
		out = (float *)calloc(sizeof(float), in1len);
		outlen = in1len;
		tc2 = 0;
		for (int j = 0; j < in2len; j++)tc2 += in1[j] * in1[j];
		tcc = tc2;
		for (int i = 1; i < in1len - in2len; i++)
		{
			tcc = tcc - in1[i - 1] * in1[i - 1] +
				in1[i + in2len - 1] * in1[i + in2len - 1];
			tc2 = 1 / sqrt(tcc)*tc1;
			temp = 0;
			for (int j = 0; j < in2len; j++)
			{
				temp = temp + in1[i] * in2[j];
			}
			out[i] = temp*tc2;
		}
	}
	return out;
}


void TestSTFT()
{
	Complex *h_signal = (Complex *)malloc(sizeof(Complex) * 1024);

	dgVect in1, in2;
	dgVect out;
	int st;
	int ed;
	st = clock();
	SacFile scFile3 = SacFileRead("D:/Program/bin/win64/Debug/st01_0828.z");
	TYPE_FFT *data3 = (TYPE_FFT *)malloc(sizeof(TYPE_FFT)*scFile3.sacdata.length);
	for (int i = 0; i < scFile3.sacdata.length; i++)
		data3[i].real = scFile3.sacdata.data[0][i], data3[i].imag = 0;
	TYPE_FFT *o3 = stft_real(data3, scFile3.sacdata.length, 1, 1024);
	SacFileClose(scFile3);
	free(o3);
	ed = clock();
	printf("stft time:%fs\n", (float)(ed - st) / CLOCKS_PER_SEC);
	free(h_signal);

	st = clock();
	SacFile scFile2 = SacFileRead("D:/Program/bin/win64/Debug/st01_0828.z");
	Complex *data = (Complex *)malloc(sizeof(Complex)*scFile2.sacdata.length);
	for (int i = 0; i < scFile2.sacdata.length; i++)
		data[i].x = scFile2.sacdata.data[0][i], data[i].y = 0;
	Complex *o1 = my_stft(data, scFile2.sacdata.length, 1, 1024);
	free(o1);
	SacFileClose(scFile2);
	ed = clock();
	printf("cuda stft time:%fs\n", (float)(ed - st) / CLOCKS_PER_SEC);
	free(h_signal);

}

void TestConv()
{
	int st;
	int ed;

	st = clock();
	SacFile scFile = SacFileRead("D:/Program/bin/win64/Debug/st01_0828.z");
	float *ft = (float *)malloc(sizeof(float) * 1024);
	//for (int i = 0; i < 1024; i++)ft[i] = 1;
	float *ooot = DGConvKernel(scFile.sacdata.data[0], scFile.sacdata.length, ft, 1024);
	SacFileClose(scFile);
	for (int j = 0; j < 10; j++)printf("%f,", ooot[j]);
	free(ft);
	ed = clock();
	printf("avx+sacfile:%fs\n", (float)(ed - st) / CLOCKS_PER_SEC);

	st = clock();
	SacFile scFile1 = SacFileRead("D:/Program/bin/win64/Debug/st01_0828.z");
	float *ft1 = (float *)malloc(sizeof(float) * 1024);
	CONV(scFile1.sacdata.data[0], scFile1.sacdata.length, ft1, 1024);
	
	SacFileClose(scFile1);
	free(ft1);
	ed = clock();
	printf("sacfile:%fs\n", (float)(ed - st) / CLOCKS_PER_SEC);


}
