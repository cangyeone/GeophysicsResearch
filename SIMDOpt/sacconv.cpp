#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "APITest.h"
int SacConv(int argc, char **argv)
{
	int st;
	int ed;
	char *fileName1;
	char *fileName2;
	float *out;
	float level;
	FILE *outFile;
	char *outName, tag[7] = ".corr";
	//printf("%s", argv[0]);
	if (argc == 1)
		return 1;
	fileName1 = argv[1];
	fileName2 = argv[2];
	int slen = strlen(fileName1);
	level = atof(argv[3]);
	outName = (char *)malloc(sizeof(char)*(slen + 10));
	for (int i = 0; i < slen + 10; i++)outName[i] = '\0';
	strcat(outName, fileName1);
	strcat(outName, tag);
	SacFile scFile1 = SacFileRead(fileName1);
	SacFile scFile2 = SacFileRead(fileName2);
	out = (float *)DGConvKernel(scFile1.sacdata.data[0], scFile1.sacdata.length,
		scFile2.sacdata.data[0], scFile2.sacdata.length);
	SacFileClose(scFile1);
	SacFileClose(scFile2);
	outFile = fopen(outName, "w");
	for (int i = 0; i < scFile1.sacdata.length; i++)
	{
		if (out[i] > level)
		{
			fprintf(outFile, "%f,%f\n", (float)(i) / 100., out[i]);
		}
	}
	return 0;
}