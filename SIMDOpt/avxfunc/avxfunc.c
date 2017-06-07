#include "afxfunc.h"
#include <immintrin.h>
#include <math.h>
dgVect DgConvKernel(dgVect in1, dgVect in2)
{
	dgVect out;
	__m256 in1_m, in2_m, mtm, out_m;
	int packlen1,packlen2;
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
	__m256 in1_m, in2_m, mtm, out_m, in4_m;
	__m256 in1_s, in2_s, sum;
	int packlen1, packlen2;
	float tt1, tt2, tt3, tt4, tt5, tt6,tcc;
	float cc1,cc2,tag[8];
	
	if (in1len > in2len)
	{
		//temp= out = (float *)calloc(sizeof(float), in2len);
		out = (float *)calloc(sizeof(float), in1len);
		outlen = in1len;
		packlen1 = (int)(in1len / 8);
		packlen2 = (int)(in2len / 8);
		float zero = 0;
		in1_m = _mm256_setzero_ps();
		for (int j = 0; j < packlen2; j++)
		{
			in2_m = _mm256_loadu_ps(in2 + j * 8);
			in2_m = _mm256_mul_ps(in2_m, in2_m);
			in1_m = _mm256_add_ps(in2_m,in1_m);
			//_mm256_storeu_ps(temp + j * 8, in1_m);
		}
		_mm256_storeu_ps(tag, in1_m);
		cc1 = 0;
		for (int j = 0; j < 8; j++)cc1 += tag[j];
		cc1 = 1/sqrt(cc1);
		in1_s = _mm256_broadcast_ss(&cc1);
		//for (int i = 0; i < 8; i++ )printf("%f\n", tag[i]);
		for (int j = 0; j < packlen2; j++)
		{
			in2_m = _mm256_loadu_ps(in1 + j * 8);
			in1_m = _mm256_fmadd_ps(in2_m, in2_m, in1_m);
		}
		_mm256_storeu_ps(tag, in1_m);
		tt1 = tag[0] + tag[1];
		tt2 = tag[2] + tag[3];
		tt3 = tag[4] + tag[5];
		tt4 = tag[6] + tag[7];
		tt5 = tt1 + tt2;
		tt6 = tt3 + tt4;
		tcc = tt5 + tt6;

		cc2 = 1 / sqrt(tcc);
		in2_s = _mm256_broadcast_ss(&cc2);
		in2_s = _mm256_mul_ps(in1_s, in2_s);
		sum = _mm256_broadcast_ss(&zero);
		for (int j = 0; j < packlen2; j++)
		{

			in1_m = _mm256_loadu_ps(in1 + j * 8);
			in2_m = _mm256_loadu_ps(in2 + j * 8);
			mtm = _mm256_mul_ps(in1_m, in2_m);
			sum = _mm256_fmadd_ps(mtm, in2_s, sum);
		}
		//for (int j = 0; j < in2len; j++)printf("%f,",temp[j]);
		_mm256_storeu_ps(tag, sum);
		tt1 = tag[0] + tag[1];
		tt2 = tag[2] + tag[3];
		tt3 = tag[4] + tag[5];
		tt4 = tag[6] + tag[7];
		tt5 = tt1 + tt2;
		tt6 = tt3 + tt4;
		cc2 = tt5 + tt6;
		out[0] = cc2;

		for (int i = 1; i < in1len - in2len; i++)
		{
			tcc = tcc-in1[i - 1]* in1[i - 1]+
				in1[i + in2len - 1]*in1[i + in2len - 1];
			cc2 = 1/sqrt(tcc);
			in2_s = _mm256_broadcast_ss(&cc2);
			in2_s = _mm256_mul_ps(in1_s, in2_s);
			sum = _mm256_broadcast_ss(&zero);
			for (int j = 0; j < packlen2; j++)
			{

				in1_m = _mm256_loadu_ps(in1 + i + j * 8);
				in2_m = _mm256_loadu_ps(in2 + j * 8);
				mtm = _mm256_mul_ps(in1_m, in2_m);
				sum = _mm256_fmadd_ps(mtm, in2_s, sum);
			}
			_mm256_storeu_ps(tag, sum);
			//tt1 = sum.m256_f32[0] + sum.m256_f32[1];
			//tt2 = sum.m256_f32[2] + sum.m256_f32[3];
			//tt3 = sum.m256_f32[4] + sum.m256_f32[5];
			//tt4 = sum.m256_f32[6] + sum.m256_f32[7];
			tt1 = tag[0] + tag[1];
			tt2 = tag[2] + tag[3];
			tt3 = tag[4] + tag[5];
			tt4 = tag[6] + tag[7];
			tt5 = tt1 + tt2;
			tt6 = tt3 + tt4;
			cc2 = tt5 + tt6;
			out[i] = cc2;
			//printf("%f",cc2);
		}
	}
	//for (int i = 0; i < 30; i++)printf("dt:%f\n", out[i]);
	return out;
}