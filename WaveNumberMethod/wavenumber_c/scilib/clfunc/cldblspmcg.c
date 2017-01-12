/*
 * cldblspmcg.c
 *
 *  Created on: 2015Äê9ÔÂ2ÈÕ
 *      Author: Cy
 */


#include "../mathematics.h"
#include <memory.h>
/*

void DblSpmCG(dblspm A,double *f,int n,double *c)
{
	double *r,*pOld,*rOld,*Ap,*ptr;
	double q,e;
	int i;

	cl_unit err;
	cl_device_id device;
	cl_context context;
	cl_command_queue cmdQueue;
	cl_mem clr,clpOld,clrOld,clAp,clf,clData,clPtr,clIdx,clTldata,clpar,clc,clTptr;
	cl_program program;
	cl_kernel kernelSpareDataMultVect,kernelVectReduce,kernelVectConstVect,kernelVectDotVect,kernelConstDivConst,kernelVectMinusVect,kernelCopyVect,kernelMapPtr;
	size_t golbalWorkSize[1];

	r=DblPInit(n);
	pOld=DblPInit(n);
	rOld=DblPInit(n);
	Ap=DblPInit(n);

	tldata=DblPinit(A.ptr[A.nRow]);
	ptr=DblPInit(A.ptr[A.nRow]);

	ptr[1]=ptr[2]=ptr[3]=1;
	device=ClGetDevice();
	context=clCreateContext(Null,1,&device,NULL,NULL,&err);
	cmdQueue=clCreateCommandQueue(context,device,0,&err);

	clr=ClWriteBuff(context,cmdQueue,r,sizeof(double)*n,CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clc=ClWriteBuff(context,cmdQueue,c,sizeof(double)*n,CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clpOld=ClWriteBuff(context,cmdQueue,pOld,sizeof(double)*n,CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clrOld=ClWriteBuff(context,cmdQueue,rOld,sizeof(double)*n,CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clAp=ClWriteBuff(context,cmdQueue,Ap,sizeof(double)*n,CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clf=ClWriteBuff(context,cmdQueue,f,sizeof(double)*n,CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clpar=ClWriteBuff(context,cmdQueue,par,4,CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clTldata=ClWriteBuff(context,cmdQueue,clTldata,sizeof(double)*A.ptr[A.nRow],CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clData=ClWriteBuff(context,cmdQueue,A.data,sizeof(double)*A.ptr[A.nRow],CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clTptr=ClWriteBuff(context,cmdQueue,A.ptr,sizeof(double)*A.ptr[A.nRow],CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clPtr=ClWriteBuff(context,cmdQueue,ptr,sizeof(double)*A.ptr[A.nRow],CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);
	clIdx=ClWriteBuff(context,cmdQueue,A.idx,sizeof(double)*A.ptr[A.nRow],CL_MEM_WRITE_ONLY&&CL_MEM_REAL_ONLY);

	program=ClGetProgram(context,&device,1,"ConjugateGradinet.cl");

	kernelSpareDataMultVect=clCreateKernel(program,"SpareDataMultVect",&err);
	kernelVectReduce=clCreateKernel(program,"VectReduce",&err);
	kernelVectConstVect=clCreateKernel(program,"VectConstVect",&err);
	kernelVectDotVect=clCreateKernel(program,"VectDotVect",&err);
	kernelConstDivConst=clCreateKernel(program,"ConstDivConst",&err);
	kernelVectMinusVect=clCreateKernel(program,"VectMinusVect",&err);
	kernelCopyVect=clCreateKernel(program,"CopyVect",&err);
	kernelMapPtr=clCreateKernel(program,"MapPtr",&err);

	clSetKernelArg(kernelMapPtr,0,&clTptr);
	clSetKernelArg(kernelMapPtr,0,&clPtr);
	golbalWorkSize[0]=A.ptr[A.nRow];
	clEnqueueNDRangeKernel(cmdQueue,kernelMapPtr,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);

	clSetKernelArg(kernelSpareDataMultVect,0,&clData);
	clSetKernelArg(kernelSpareDataMultVect,1,&clIdx);
	clSetKernelArg(kernelSpareDataMultVect,2,&clc);
	clSetKernelArg(kernelSpareDataMultVect,3,&clTlData);
	golbalWorkSize[0]=A.ptr[A.nRow];
	clEnqueueNDRangeKernel(cmdQueue,kernelSpareDataMultVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);
	clSetKernelArg(kernelVectReduce,0,&clTlData);
	clSetKernelArg(kernelVectReduce,1,&clPtr);
	clSetKernelArg(kernelVectReduce,2,&clAp);
	golbalWorkSize[0]=A.ptr[A.nRow];
	clEnqueueNDRangeKernel(cmdQueue,kernelVectReduce,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);

	clSetKernelArg(kernelVectConstVect,0,&clc);
	clSetKernelArg(kernelVectConstVect,1,&clPar);
	clSetKernelArg(kernelVectConstVect,2,2);
	clSetKernelArg(kernelVectConstVect,3,-1);
	clSetKernelArg(kernelVectConstVect,4,clAp);
	clSetKernelArg(kernelVectConstVect,5,clrOld);
	golbalWorkSize[0]=n;
	clEnqueueNDRangeKernel(cmdQueue,kernelVectDotVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);
	clSetKernelArg(kernelCopyVect,0,clrOld);
	clSetKernelArg(kernelCopyVect,1,clpOld);
	golbalWorkSize[0]=n;
	clEnqueueNDRangeKernel(cmdQueue,kernelCopyVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);


	//DblPmSpMP(f,A,c,rOld);
	//DblPmSpMP(f,A,c,pOld);

	for(i=0;i<n;i++)
	{
		clSetKernelArg(kernelSpareDataMultVect,0,&clData);
		clSetKernelArg(kernelSpareDataMultVect,1,&clIdx);
		clSetKernelArg(kernelSpareDataMultVect,2,&clpOld);
		clSetKernelArg(kernelSpareDataMultVect,3,&clTlData);
		golbalWorkSize[0]=A.ptr[A.nRow];
		clEnqueueNDRangeKernel(cmdQueue,kernelSpareDataMultVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);
		clSetKernelArg(kernelVectReduce,0,&clTlData);
		clSetKernelArg(kernelVectReduce,1,&clPtr);
		clSetKernelArg(kernelVectReduce,2,&clAp);
		golbalWorkSize[0]=A.ptr[A.nRow];
		clEnqueueNDRangeKernel(cmdQueue,kernelVectReduce,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);

		clSetKernelArg(kernelVectDotVect,0,&clrOld);
		clSetKernelArg(kernelVectDotVect,1,&clrOld);
		clSetKernelArg(kernelVectDotVect,2,&clPar[0]);
		clSetKernelArg(kernelVectDotVect,3,0);
		golbalWorkSize[0]=n;
		clEnqueueNDRangeKernel(cmdQueue,kernelVectDotVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);
		clSetKernelArg(kernelVectDotVect,0,&clrOld);
		clSetKernelArg(kernelVectDotVect,1,&clAp);
		clSetKernelArg(kernelVectDotVect,2,&clPar);
		clSetKernelArg(kernelVectDotVect,3,1);
		golbalWorkSize[0]=n;
		clEnqueueNDRangeKernel(cmdQueue,kernelVectDotVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);
		clSetKernelArg(kernelConstDivConst,0,&clPar);
		clSetKernelArg(kernelConstDivConst,1,2);
		golbalWorkSize[0]=1;
		clEnqueueNDRangeKernel(cmdQueue,kernelConstDivConst,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);
		clSetKernelArg(kernelVectConstVect,0,&clc);
		clSetKernelArg(kernelVectConstVect,1,&clPar);
		clSetKernelArg(kernelVectConstVect,2,2);
		clSetKernelArg(kernelVectConstVect,3,+1);
		clSetKernelArg(kernelVectConstVect,4,clpOld);
		clSetKernelArg(kernelVectConstVect,5,clc);
		golbalWorkSize[0]=n;
		clEnqueueNDRangeKernel(cmdQueue,kernelVectConstVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);
		clSetKernelArg(kernelVectConstVect,0,&clrOld);
		clSetKernelArg(kernelVectConstVect,1,&clPar);
		clSetKernelArg(kernelVectConstVect,2,2);
		clSetKernelArg(kernelVectConstVect,3,-1);
		clSetKernelArg(kernelVectConstVect,4,clAp);
		clSetKernelArg(kernelVectConstVect,5,clr);
		golbalWorkSize[0]=n;
		clEnqueueNDRangeKernel(cmdQueue,kernelVectConstVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);

		clSetKernelArg(kernelVectDotVect,0,&clr);
		clSetKernelArg(kernelVectDotVect,1,&clr);
		clSetKernelArg(kernelVectDotVect,2,&clPar);
		clSetKernelArg(kernelVectDotVect,3,0);
		golbalWorkSize[0]=n;
		clEnqueueNDRangeKernel(cmdQueue,kernelVectDotVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);
		clSetKernelArg(kernelVectDotVect,0,&clrOld);
		clSetKernelArg(kernelVectDotVect,1,&clrOld);
		clSetKernelArg(kernelVectDotVect,2,&clPar);
		clSetKernelArg(kernelVectDotVect,3,1);
		golbalWorkSize[0]=n;
		clEnqueueNDRangeKernel(cmdQueue,kernelVectDotVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);
		clSetKernelArg(kernelConstDivConst,0,&clPar);
		clSetKernelArg(kernelConstDivConst,1,3);
		golbalWorkSize[0]=1;
		clEnqueueNDRangeKernel(cmdQueue,kernelVectConstVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);

		clSetKernelArg(kernelVectConstVect,0,&clr);
		clSetKernelArg(kernelVectConstVect,1,&clPar);
		clSetKernelArg(kernelVectConstVect,2,3);
		clSetKernelArg(kernelVectConstVect,3,1);
		clSetKernelArg(kernelVectConstVect,4,clpOld);
		clSetKernelArg(kernelVectConstVect,5,clpOld);
		golbalWorkSize[0]=n;
		clEnqueueNDRangeKernel(cmdQueue,kernelVectConstVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);

		clSetKernelArg(kernelCopyVect,0,clr);
		clSetKernelArg(kernelCopyVect,1,clrOld);
		golbalWorkSize[0]=n;
		clEnqueueNDRangeKernel(cmdQueue,kernelCopyVect,1,NULL,golbalWorkSize,NULL,0,NULL,NULL);
		//DblSpmMV(A,pOld,Ap);
		//q=DblPP(rOld,rOld,n)/DblPP(pOld,Ap,n);
		//DblCPpP(c,q,pOld,n,c);
		//DblCPpP(rOld,-q,Ap,n,r);
		//e=DblPP(r,r,n)/DblPP(rOld,rOld,n);
		//DblCPpP(r,e,pOld,n,pOld);
		//memcpy(rOld,r,sizeof(double)*n);
	}

	ClReadBuff(context,cmdQueue,c,n*sizeof(double));
	clReleaseKernel(kernelSpareDataMultVect);
	clReleaseKernel(kernelVectReduce);
	clReleaseKernel(kernelVectConstVect);
	clReleaseKernel(kernelVectDotVect);
	clReleaseKernel(kernelConstDivConst);
	clReleaseKernel(kernelVectMinusVect);
	clReleaseKernel(kernelCopyVect);
	clReleaseKernel(kernelMapPtr);

	clReleaseKernel(program);
	clReleaseKernel(cmdQueue);

	clReleaseMemObject(clr);
	clReleaseMemObject(clc);
	clReleaseMemObject(clpOld);
	clReleaseMemObject(clrOld);
	clReleaseMemObject(clAp);
	clReleaseMemObject(clf);
	clReleaseMemObject(clpar);
	clReleaseMemObject(clTldata);
	clReleaseMemObject(clData);
	clReleaseMemObject(clTptr);
	clReleaseMemObject(clPtr);
	clReleaseMemObject(clIdx);

	clReleaseContext(context);

	DblPFree(ptr);
	DblPFree(r);
	DblPFree(pOld);
	DblPFree(rOld);
	DblPFree(Ap);
}



*/
