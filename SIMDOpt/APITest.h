#pragma once

#pragma once

#include <immintrin.h>
#include "stft/cu_stft.h"
#include "avxfunc/afxfunc.h"
#include "io/sacread.h"
#include "stft/zx_fft.h"

#if defined (__cplusplus)
extern "C" {
#endif

	dgVect Conv(dgVect in1, dgVect in2);
	void TestSTFT();
	void TestConv();
#if defined (__cplusplus)
}
#endif
