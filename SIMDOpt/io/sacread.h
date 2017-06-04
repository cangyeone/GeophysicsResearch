#include <stdio.h>
#include <float.h>
#include <stdlib.h>
#ifndef SAC_H_
#define SAC_H_
typedef float float32;
typedef int int32;
typedef long long int64;

#pragma pack(4)
struct SacHead
{
	float32 H70f[70];
	int32 H40i[40];
	int64 H24q[24];
};
typedef struct SacHead SacHead;

struct SacData
{
	float32 **data;
	int ndata;
	int length;
};
typedef struct SacData SacData;

struct SacFile
{
	SacHead sachead;
	SacData sacdata;
};
typedef struct SacFile SacFile;
#if defined (__cplusplus)
extern "C" {
#endif
	SacHead SacGetHead(FILE *sacFile);
	SacData SacGetData(FILE *sacFile, SacHead SacHead);
	SacFile SacFileRead(const char *fileName);
	void SacFileClose(SacFile file);
	void SacFileToTxt(const char *inFileName, const char *outFileName);
#if defined (__cplusplus)
}
#endif
#endif /*SAC_H_*/