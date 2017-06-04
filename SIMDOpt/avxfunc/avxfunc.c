#include "afxfunc.h"
#include <immintrin.h>
dgVect DgConvKernel(dgVect in1, dgVect in2)
{
	dgVect out;
	__m256 in1_m, in2_m, mtm, out_m;
	int packlen1,packlen2;
	float tag[8];
	if (in1.len > in2.len)
	{
		out.data = (float *)calloc(sizeof(float), in1.len);
		out.len = in1.len;
		packlen1 = (int)(in1.len / 8);
		packlen2 = (int)(in2.len / 8);
		for (int i = 0; i < in1.len-in2.len; i++)
		{
			for (int j = 0; j < packlen2; j++)
			{
				
				in1_m = _mm256_loadu_ps(in1.data + i);
				in2_m = _mm256_loadu_ps(in2.data + j * 8);
				//_mm256_storeu_ps(tag, in1_m);
				//printf("%d,$%d,%f,%f,%f,%f\n",i,j, tag[0], tag[1], tag[2], tag[3]);
				mtm = _mm256_mul_ps(in1_m, in2_m);

				out_m = _mm256_loadu_ps(out.data + i +j * 8);
				mtm = _mm256_add_ps(mtm, out_m);
				_mm256_storeu_ps(out.data + i + j * 8, mtm);
			}
		}
	}
	return out;
}
float *DGConvKernel(float *in1, int in1len, float *in2, int in2len)
{
	float *out;
	int outlen;
	__m256 in1_m, in2_m, mtm, out_m;
	int packlen1, packlen2;
	float tag[8];
	if (in1len > in2len)
	{
		out = (float *)calloc(sizeof(float), in1len);
		outlen = in1len;
		packlen1 = (int)(in1len / 8);
		packlen2 = (int)(in2len / 8);
		for (int i = 0; i < in1len - in2len; i++)
		{
			for (int j = 0; j < packlen2; j++)
			{

				in1_m = _mm256_loadu_ps(in1 + i);
				in2_m = _mm256_loadu_ps(in2 + j * 8);
				//_mm256_storeu_ps(tag, in1_m);
				//printf("%d,$%d,%f,%f,%f,%f\n",i,j, tag[0], tag[1], tag[2], tag[3]);
				mtm = _mm256_mul_ps(in1_m, in2_m);

				out_m = _mm256_loadu_ps(out + i + j * 8);
				mtm = _mm256_add_ps(mtm, out_m);
				_mm256_storeu_ps(out + i + j * 8, mtm);
			}
		}
	}
	return out;
}