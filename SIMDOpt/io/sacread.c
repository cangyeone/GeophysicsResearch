#include "sacread.h"
#include <stdio.h>

SacHead SacGetHead(FILE *sacFile)
{
	
	
	SacHead SacHead;
	rewind(sacFile);
	fread((void *)(&SacHead), 4, 158, sacFile);
	return SacHead;
}

SacData SacGetData(FILE *sacFile, SacHead SacHead)
{
	float32 *dataY;
	float32 *dataX;
	SacData outSD;
	int div8;
	if (SacHead.H40i[15] == 1)
	{
		outSD.ndata = 1;
		outSD.length = SacHead.H40i[9];
		outSD.data = malloc(sizeof(float32*) * 1);
		div8 = SacHead.H40i[9] + 8 - SacHead.H40i[9] % 8;
		outSD.length = div8;
		dataY = malloc(4 * div8);
		fread((void *)(dataY), 4, SacHead.H40i[9], sacFile);
		outSD.data[0] = dataY;
	}
	else
	{
		outSD.ndata = 2;
		outSD.length = SacHead.H40i[9];
		outSD.data = malloc(sizeof(float32*) * 2);
		dataY = malloc(4 * SacHead.H40i[9]);
		dataX = malloc(4 * SacHead.H40i[9]);
		fread((void *)(dataX), 4, SacHead.H40i[9], sacFile);
		fread((void *)(dataY), 4, SacHead.H40i[9], sacFile);
		outSD.data[0] = dataX;
		outSD.data[1] = dataY;
	}
	return outSD;
}

SacFile SacFileRead(const char *fileName)
{
	SacFile outSF;
	FILE *sacFile;
	
	sacFile = fopen(fileName, "rb+");

	outSF.sachead = SacGetHead(sacFile);
	
	outSF.sacdata = SacGetData(sacFile, outSF.sachead);
	fclose(sacFile);
	return outSF;
}

void SacFileClose(SacFile file)
{
	int i;
	for (i = 0; i<file.sacdata.ndata; i++)
	{
		free(file.sacdata.data[i]);
	}
	free(file.sacdata.data);
}

void SacFileToTxt(const char *inFileName, const char *outFileName)
{
	int i, j;
	float time;
	//char buffer[256];
	FILE *outFile;
	SacFile scFile;
	scFile = SacFileRead(inFileName);

	outFile = fopen(outFileName, "w+");
	for (i = 0; i<14; i++)
	{
		fprintf(outFile, "Head line:%10d:", i);
		for (j = 0; j<5; j++)
		{
			fprintf(outFile, "%15.7f", scFile.sachead.H70f[i * 5 + j]);
		}
		fprintf(outFile, "\n");
	}

	for (i = 0; i<8; i++)
	{
		fprintf(outFile, "Head line:%10d:", i + 14);
		for (j = 0; j<5; j++)
		{
			fprintf(outFile, "%15d", scFile.sachead.H40i[i * 5 + j]);
		}
		fprintf(outFile, "\n");
	}

	for (i = 0; i<8; i++)
	{
		fprintf(outFile, "Head line:%10d:", i + 22);
		for (j = 0; j<3; j++)
		{
			fprintf(outFile, "%15d", scFile.sachead.H24q[i * 3 + j]);
		}
		fprintf(outFile, "\n");
	}

	for (i = 0; i<scFile.sacdata.length; i++)
	{

		time = i*scFile.sachead.H70f[0];
		fprintf(outFile, "%15.7f %15.7f\n", time, scFile.sacdata.data[0][i]);
	}

	SacFileClose(scFile);
	fclose(outFile);
}



