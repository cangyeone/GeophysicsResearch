/*
 * mycomplex.h
 *
 *  Created on: 2014Äê12ÔÂ25ÈÕ
 *      Author: CY
 */

#ifndef MYCOMPLEX_H_
#define MYCOMPLEX_H_
#include <complex.h>
#include "const.h"

#define V2x(A,i,j) (A##[i][j].x)
#define V2y(A,i,j) (A##[i][j].y)
#define Vx(A,i,j,k) (A##[i][j][k].x)
#define Vy(A,i,j,k) (A##[i][j][k].y)
#define Vz(A,i,j,k) (A##[i][j][k].z)

struct vector2d
{
	double x;
	double y;
};
struct vector3d
{
	double x;
	double y;
	double z;
};
struct tensor2d
{
	double xx,xy;
	double yx,yy;
};
struct tensor3d
{
	double xx,xy,xz;
	double yx,yy,yz;
	double zx,zy,zz;
};
///////////////////Compressed Row Storage/////////////////
struct spareMatrix
{
	double *data;
	int *idx;
	int *ptr;
	int nRow;
};
struct spareComplexMatrix
{
	double complex *data;
	int *idx;
	int *ptr;
	int nRow;
};
//////////////////////////////////////////////struct define/////////////////////////////////////////////////
typedef double complex cplx;
typedef double dble;

typedef struct vector3d vect;
typedef struct vector2d vect2;
typedef struct tensor3d tens;
typedef struct tensor2d tens2;

typedef double complex** cpxm;
typedef double ** dblm;
typedef struct spareMatrix dblspm;
typedef struct spareComplexMatrix cpxspm;
typedef vect2** vect2m;



inline cplx CpxSq(cplx a);
/////////////////////////////////////////////harmonic function///////////////////////////////////////
double besselj(double x,int n);
double dBesselj(double x,int n);

////////////////////////////////////////////matrix algorithm /////////////////////////////////////////////////
//double
double **DblMInit(int m,int n);
void DblMFree(double **a);
double *DblPInit(int n);
void DblPFree(double *a);

void DblMMs(double **a,double **b,int n,double **c);
void DblMPs(double **a,double *b,int n,double *c);
void DblMTs(double **a,int n,double **c);
void DblMTsc(double **a,int n);
void DblCMsc(double b,int n,double **a);
void DblMpart(double **a,int yl,int yu,int xl,int xu,double **b);
void DblCP(double *a,double b,int n,double *c);
void DblCPc(double b,int n,double *a);
double DblPP(double *a,double *b,int n);
int DblMinv(double **a2,int n,double **c2);
//cplx
cplx **CpxMInit(int m,int n);
void CpxMFree(cplx **a);
cplx *CpxPInit(int n);
void CpxPFree(cplx *a);

void CpxMMs(cplx **a,cplx **b,int n,cplx **c);
void CpxMPs(cplx **a,cplx *b,int n,cplx *c);
void CpxMTs(cplx **a,int n,cplx **c);
void CpxMTsc(cplx **a,int n);
void CpxCMsc(double b,int n,cplx **a);
void CpxMpart(cplx **a,int yl,int yu,int xl,int xu,cplx **b);
cplx CpxPP(cplx *a,cplx *b,int n);
int CpxMinv(cplx **a2,int n,cplx **c2);
void CpxMsSetI(cpxm a,int n);
//////////////////////////matrix-print//////////////////////////////////
void CpxMsPt(cplx **a,int n);
void CpxPPt(cplx *a,int n);
void DblMsPt(double **a,int n);
void DblPPt(double *a,int n);
void CpxMsSumPt(cplx **a,int n);
/////////////////////////////////////////////tensor calculation//////////////////////////////////////////////////////////
inline double ModVect2(vect2 a);
inline double ModVect(vect a);
inline double AngVect2(vect2 a);
inline double Vect2DotVect2(vect2 a,vect2 b);
inline vect2 RotVect2(vect2 a,double theta);
inline int QuadVect2(vect2 a);
inline vect2 GenVect2(vect2 a,double mod);
inline vect2 ZeroVect2();
inline vect2 OppVect2(vect2 a);
vect2 **Vect2MInit(int m,int n);
void Vect2MFree(vect2 **a);
/////////////////////////////////////////////////////////////////////////////////////////
void myfft(cplx *tA,unsigned int dotN,cplx *B,int sel);
void mydft(cplx *A,int N,cplx *B,int sel);



///////////////////////////////////////////fix-form matrix calculation //////////////////////////////////////////////////////
inline void CpxM2M2c(cplx A[2][2],cplx B[2][2]);
inline void CpxMM2c(cplx **A,cplx B[2][2]);
void CpxM2M2(cplx A[2][2],cplx B[2][2],cplx C[2][2]);
int CpxM2inv(cplx A[2][2],cplx B[2][2]);
void CpxM2toI(cplx a[2][2]);
void CpxM2P2c(cplx a[2][2],cplx b[2]);
void CpxP2pP2c(cplx a[2],cplx b[2]);
void CpxM2pt(cplx a[2][2]);
inline void CpxM2to0(cplx a[2][2]);
inline void CpxM2M2(cplx a[2][2],cplx b[2][2],cplx c[2][2]);
void CpxM2mM2(cplx a[2][2],cplx b[2][2],cplx c[2][2]);
inline void CpxM2pM2(cplx a[2][2],cplx b[2][2],cplx c[2][2]);
inline void CpxM2pM2c(cplx a[2][2],cplx b[2][2]);
inline void CpxM2Sc(double x,cplx a[2][2]);
inline void CpxM2M2M2(cplx a[2][2],cplx b[2][2],cplx c[2][2],cplx d[2][2]);
void CpCpxMM2(cplx **a,cplx b[2][2]);
void CpCpxM2M(cplx a[2][2],cplx **b);

void CpxM4to0(cplx a[4][4]);
void CpxM8to0(cplx a[8][8]);
void CpxM4M4(cplx A[4][4],cplx B[4][4],cplx C[4][4]);
void CpxM4M4c(cplx A[4][4],cplx B[4][4]);
void CpxM8M8(cplx a[8][8],cplx b[8][8],cplx c[8][8]);
void CpxM4P4(cplx a[4][4],cplx b[4],cplx c[4]);
void CpxM8P8(cplx a[8][8],cplx b[8],cplx c[8]);
void CpxM4pt(cplx a[4][4]);
void CpxM8pt(cplx a[8][8]);
inline cplx CpxM4det(cplx A[4][4]);
inline cplx CpxM3dt(cplx A[3][3]);
int CpxM4inv(cplx A[4][4],cplx B[4][4]);
inline void CpxM4pM4(cplx AA[4][4],cplx BB[4][4],cplx CC[4][4]);
inline void CpxM4mM4(cplx AA[4][4],cplx BB[4][4]);
inline void CpCpxM4M(cplx AA[4][4],cplx **BB);
inline void CpCpxMM4(cplx **A,cplx B[4][4]);
void CpxM8inv(cplx AA[8][8],cplx BB[8][8]);
void CpxMquard2(cplx **rs,cplx A[2][2],cplx B[2][2],cplx C[2][2],cplx D[2][2]);


////////////////////spare-matrix//////////////////////////////
void DblSpmFree(dblspm a);
dblspm DblMtoSpm(double **a,int m,int n);
void DblSpmPt(dblspm a);
void DblSpmMV(dblspm a,double *b,double *c);
double DblSpmIdx(dblspm a,int i,int j);
void DblSpmCG(dblspm a,double *b,int n,double *c);

void CpxSpmFree(cpxspm a);
cpxspm CpxMtoSpm(double _Complex **a,int m,int n);
void CpxSpmPt(cpxspm a);
void CpxSpmMV(cpxspm a,double _Complex *b,double _Complex *c);
double CpxSpmIdx(cpxspm a,int i,int j);
void CpxSpmCG(cpxspm a,double _Complex *b,int n,double _Complex *c);

#endif /* MYCOMPLEX_H_ */
