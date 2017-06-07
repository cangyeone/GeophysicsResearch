/*
 * zx_fft.h
 *
 *  Created on: 2013-8-5
 *      Author: monkeyzx
 */

#ifndef _ZX_FFT_H
#define _ZX_FFT_H
#ifdef __cplusplus
extern "C" {
#endif
#include "Config.h"

#define TYPE_FFT_E     float    /* Type is the same with COMPLEX member */     

#ifndef PI
#define PI             (3.14159265f)
#endif

	typedef COMPLEX TYPE_FFT;  /* Define COMPLEX in Config.h */

	int fft(TYPE_FFT *x, uint32_t N);
	int fft_real(TYPE_FFT *x, uint32_t N);
	int ifft(TYPE_FFT *x, uint32_t N);
	int ifft_real(TYPE_FFT *x, uint32_t N);
	TYPE_FFT *stft_real(TYPE_FFT *h_signal, int s_size, int w_lag, int s_len);
#ifdef __cplusplus
}
#endif
#endif /* ZX_FFT_H_ */

