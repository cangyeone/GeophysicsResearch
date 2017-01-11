/*
 * clcompiletime.c
 *
 *  Created on: 2015Äê9ÔÂ1ÈÕ
 *      Author: Cy
 */


#include "../clmathematics.h"
#include <stdio.h>
/*
cl_device_id ClGetDevice()
{
	cl_uint numPlatforms=0;//,numDevices=0;
	cl_platform_id *platforms;
	cl_device_id devices;
	clGetPlatformIDs(0,NULL,&numPlatforms);
	platforms=(cl_platform_id *)malloc(sizeof(cl_platform_id)*numPlatforms);
	clGetPlatformIDs(numPlatforms,platforms,NULL);

	//clGetDeviceIDs(platforms[0],CL_DEVICE_TYPE_GPU,0,NULL,&numDevices);
	//devices=(cl_device_id *)malloc(sizeof(cl_device_id)*numDevices);
	clGetDeviceIDs(platforms[0],CL_DEVICE_TYPE_GPU,1,&devices,NULL);
	free(platforms);
	return devices;
}

cl_program ClGetProgram(cl_context context,cl_device_id *device,cl_uint numDevice,const char* filename)
{
	cl_program program;
	FILE *clFile;
	char *clFileBuff, *program_log;
	size_t clFileSize, log_size;
	int err;

	clFile=fopen(filename, "r");
	fseek(clFile,0,SEEK_END);
	clFileSize=ftell(clFile);
	rewind(clFile);
	clFileBuff=(char *)malloc(clFileSize+1);
	clFileBuff[clFileSize] = '\0';
	fread(clFileBuff,sizeof(char),clFileSize,clFile);
	fclose(clFile);

	program=clCreateProgramWithSource(context,1,(const char**)&clFileBuff, &clFileSize, &err);
	free(clFileBuff);

	clBuildProgram(program,numDevice,device,NULL,NULL,NULL);
	return program;
}

cl_mem ClWriteBuff(cl_context context,cl_command_queue cmdQueue,void *buff,cl_unit dataSize,cl_bool BOOL)
{
	int err;
	cl_mem buffA;
	buffA=clCreateBuffer(context,BOOL,dataSize,buff,&err);
	clEnqueueWriteBuffer(cmdQueue,buffA,CL_FALSE,0,dataSize,buff,0,NULL,NULL);
	return buffA;
}

cl_mem ClReadBuff(cl_context context,cl_command_queue cmdQueue,void *buff,cl_unit dataSize,cl_bool BOOL)
{
	int err;
	cl_mem buffA;
	buffA=clCreateBuffer(context,BOOL,dataSize,buff,&err);
	clEnqueueReadBuffer(cmdQueue,buffA,CL_FALSE,0,dataSize,buff,0,NULL,NULL);
	return buffA;
}
*/
