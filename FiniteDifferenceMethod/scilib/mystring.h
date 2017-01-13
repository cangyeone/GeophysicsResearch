/*
 *  This header is used to realize dynamic strings
 *   Some functions is used to get the fold file
 *	   Copyright Canyge@geophyfx.com
 *       2014-12-8   vision 0.1
 */

/*
==============Instruction to filetype and macro=======
    STRING is char *
    VCHAR->count is the quantity of STRING
    VCHAR->string[i] is the STRING
    CURRENTFOLD stands for the current directory
    CHARLEN stands for the max length of the directory 
==============Instruction to functions================
  ===VCHAR function:===
    VCHAR sregister()     is used to initialize the VCHAR file. All VCHAR must be initialized before used!!
    void sfree()          is used to free VCHAR memory.
    void sappend(VCHAR vc,STRING a)   is used to append a to VCHAR file.
    VCHAR ssplit(STRING a,STRING b)   is used to split a with b. Retrun value is the substring
    STRING sjoin(VCHAR a,STRINT b) 	is used to connect a with b to new STRING
  ==STRING function:===
    STRING strReplace(STRING a,STRING b,STRING c)      replace b in a with c return a new STRING
    STRING strConnect(STRING a,STRING b)                    connect a and b return a new STRING
    int strHeadMatch(STRING a,STRING b)                       a and b is the same from head regardless of the rest
    int strEndMatch(STRING a,STRING b)                       a and b is the same from end regardless of the rest
  ===DIR function:===
    VCHAR GetDirFiles(STRING selfold)                         get all files in selfold;
 
==============Black-Red Tree function need to be added in v0.2================
    BRTree sregister()     is used to initialize the BRTree file. All BRTree must be initialized before used!!
    void BRTreefree()                   is used to free BRTree memory.
    void BRTappend(BRTree vc,void *p)   is used to append a to VCHAR file.
    void *BRTfind(BRTree vc,*p)         is used to find

  *VCHAR sregister()     is used to initialize the VCHAR file. All VCHAR must be initialized before used!!
 *void sfree()          is used to free VCHAR memory.
 *void sappend(VCHAR vc,STRING a)   is used to append a to VCHAR file.
 */



#ifndef _MYSTRING_H_
#define _MYSTRING_H_
#include <dirent.h>
#include <stdio.h>
#include <string.h>
#include <malloc.h>
#define MIN(A,B) ((A)>(B))?((B)):((A))
#define CHARLEN 1000
#define CURRENTFOLD "no_name_put_in"
//Test Mode Define

typedef unsigned int UINT; 
typedef char * STRING;
struct v_string
{
	UINT count;
	char **string;
};
typedef struct v_string * VCHAR;
typedef struct dirent DIRENT;

VCHAR sregister(void);
void sfree(VCHAR a);

void sappend(VCHAR orig,char *apd);
/*===============defind VCHAR method===============*/
int strHeadMatch(char *a,char *b);
int strEndMatch(char *a,char *b);
void charsetnull(char *a,UINT b);
VCHAR ssplit(char *text,char *dot);
void sprint(VCHAR a);
STRING sjoin(VCHAR a,char *b);
STRING strConnect(STRING a,STRING b);
void strSetNull(STRING a,int num);
STRING strReplace(STRING a,STRING b,STRING c);
int strStartMatch(STRING father, STRING child);

/*=============STRING process end=============*/
void ScanDir(STRING dirName,VCHAR fileList);
VCHAR GetDirFiles(STRING selfold);
VCHAR GetEndMatch(VCHAR a,STRING b);
/*===============dirprocess end====================*/

#endif
