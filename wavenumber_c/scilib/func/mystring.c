#include "../mystring.h"
int vcharcount=0;

VCHAR sregister(void)
{
	VCHAR init;
	vcharcount++;
	init=(struct v_string *)malloc(sizeof(struct v_string));
	init->count=0;
	init->string=NULL;
	return init;
}
void sfree(VCHAR a)
{
int i;
for(i=0;i<a->count;i++)free(a->string[i]);
free(a->string);
free(a);
vcharcount--;
}

void sappend(VCHAR orig,char *apd)
{
	char **temp;

	if(orig->count==0)
	{
		orig->string=(char **)malloc(sizeof(char *));
		orig->count=1;
		orig->string[0]=(char *)malloc(sizeof(char)*(strlen(apd)+1));
		strcpy(orig->string[0],apd);
	}
	else
	{
		temp=orig->string;
		orig->string=(char **)malloc(sizeof(char *)*(orig->count+1));
		memcpy(orig->string,temp,sizeof(char *)*(orig->count));
		free(temp);
		orig->string[orig->count]=(char *)malloc(sizeof(char)*(strlen(apd)+1));
		strcpy(orig->string[orig->count],apd);
		orig->count=orig->count+1;
	}
}
/*===============defind VCHAR method===============*/
int strHeadMatch(char *a,char *b)
{
	while(*(a)!='\0'&&*(b)!='\0')
	{
		if((*(a++))!=(*(b++)))return 0;
	}

	return 1;
}
int strEndMatch(char *a,char *b)
{
	UINT i,llen,alen,blen;
	alen=strlen(a);
	blen=strlen(b);
	llen=MIN(alen,blen);
	for(i=0;i<llen;i++)
	{
		if(a[alen-i-1]!=b[blen-i-1])return 0;
	}

	return 1;
}

void charsetnull(char *a,UINT b)
{
	int i;
	for(i=0;(i<b&&a[i]!='\0');i++)a[i]='\0';
}

VCHAR ssplit(char *text,char *dot)
{
	VCHAR name;
	char *pt,*ptn;
	int len,i;
	len=strlen(text);
	pt=(char *)malloc(sizeof(char)*(len+1));
	strcpy(pt,text);
	name=sregister();
	ptn=pt;
	for(i=0;i<len;i++)
	{
		if(strHeadMatch(&pt[i],dot)==1)
		{
			charsetnull(&pt[i],strlen(dot));
		}
	}
	pt=ptn;
	if(*pt!='\0')sappend(name,pt);
	for(i=1;i<len;i++)
	{
		if(pt[i-1]=='\0'&&pt[i]!='\0')sappend(name,&pt[i]);
	}
	free(ptn);
	return name;
}

void sprint(VCHAR a)
{
	int i;
	for(i=0;i<a->count;i++)
	{
		printf("%s\n",a->string[i]);
	}

}

STRING sjoin(VCHAR a,char *b)
{
	UINT alen=0,blen;
	UINT i;
	STRING c;
	for(i=0;i<a->count;i++)
	{
		alen=alen+strlen(a->string[i]);
	}

	blen=strlen(b);
	c=(STRING)malloc(sizeof(char)*(alen+blen+1));
	strcpy(c,a->string[0]);
	for(i=1;i<a->count;i++)
	{
		strcat(c,b);
		strcat(c,a->string[i]);
	}
	return c;
}

STRING strConnect(STRING a,STRING b)
{
	STRING c;
	c=(STRING)malloc(sizeof(char)*(strlen(a)+strlen(b)+1));
	strcpy(c,a);
	strcat(c,b);
	return c;
}

void strSetNull(STRING a,int num)
{
	UINT len;
	int i;
	len=strlen(a);
	for(i=0;i<num;i++)
	{a[len-i-1]='\0';}
}


STRING strReplace(STRING a,STRING b,STRING c)
{
	VCHAR test;
	STRING rt;
	int st,ed;

	st=strHeadMatch(a,b);
	ed=strEndMatch(a,b);
	test=ssplit(a,b);
	rt=sjoin(test,c);
	if(st==1)rt=strConnect(c,rt);
	if(ed==1)rt=strConnect(rt,c);
	sfree(test);
	return rt;
}

int strStartMatch(STRING father, STRING child)
{
	int flen, clen,i,k=0;
	clen = strlen(child);
	flen = strlen(father);
	if (flen < clen)return 0;
	while (father[k] == ' ')k++;
	for (i = 0; i < clen; i++)if (father[i+k] != child[i])return 0;
	return 1;
}

/*=============STRING process end=============*/

void ScanDir(STRING dirName,VCHAR fileList)
{
	DIR *sDir;
	DIRENT *dirList;
	char temp[CHARLEN];
	if((sDir=opendir(dirName))==NULL)
	{
		sappend(fileList,dirName);
	}
	while((dirList=readdir(sDir))!=NULL)
	{
		if('.'==dirList->d_name[0])continue;
		strcpy(temp,dirName);
		strcat(temp,"\\");
		strcat(temp,dirList->d_name);
		ScanDir(temp,fileList);
	}


}

VCHAR GetDirFiles(STRING selfold)
{
	char mycwd[CHARLEN];
	VCHAR fileList;
	fileList=sregister();
	if(strcmp(CURRENTFOLD,selfold)==0)
	{
		getcwd(mycwd,CHARLEN);
	}
	else
	{
		strcpy(mycwd,selfold);
	}
	ScanDir(mycwd,fileList);
	return fileList;
}

VCHAR GetEndMatch(VCHAR a,STRING b)
{
	int i;
	VCHAR re;
	re=sregister();
	for(i=0;i<a->count;i++)
	{
		//PS(a->string[i]);
		if(strEndMatch(a->string[i],b)==1)sappend(re,a->string[i]);
	}
	return re;
}


/*===============dirprocess end====================*/
