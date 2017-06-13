# -*- coding: utf-8 -*-
"""
Created on Wed May 24 14:21:19 2017

@author: LLL
"""


import os

#importlib.reload(read)
#sys.setdefaultencoding('utf8') 
hasf=''
if(len(hasf)==0):
    hasf='gethash'
def get_dir_list(cdir,suffix='.z'):
    lst=os.walk(cdir)
    for item in lst:
        #print("File dir %s is processing...(file total number:%d)"%(item[0],len(item[2])))
        for file in item[2]:
            fdir=os.path.join(item[0],file)
            if(fdir[-len(suffix):]==suffix):
                yield fdir,file
hashidx=open(hasf,'r').readlines()
outData=[[] for aa in hashidx]
fn=['file'+str(aa) for aa in range(len(hashidx))]
tct=[0 for aa in hashidx]
for fileName,files in get_dir_list(os.getcwd(),suffix='.hash'):
    file=open(fileName)
    fileData=file.readlines()
    ct=0
    for hh in hashidx:
        fct=0
        tff=[]
        for ff in fileData:
            if(ff.find(hh.strip())!=-1):
                fct+=1
                tff.append(ff.strip())
        outData[ct].append([files,tff])
        #outData[ct].append(fct)
        tct[ct]+=fct
        ct+=1
    file.close()
    
outFile=open("dt.json","w")

outFile.write('{')
outFile.write('\"nodes\":')
outFile.write('[')
outFile.write("{\"name\":\"DataBase\"},\n")

for it in range(len(outData)):
    outFile.write("{\"name\":\"hash:%s\"},\n"%(hashidx[it].strip()))
for it in range(len(outData)):
    ct=0
    for aa in outData[it]:
        try:
            outFile.write("{\"name\":\"%s\"},\n"%
                    ("hash"+str(it)+":"+fn[ct]))
            ct+=1
        except:
            pass
    
for it in range(len(outData)):
    ct=0
    for aa in outData[it]:
        try:
            for bb in aa[1]:
                outFile.write("{\"name\":\"%s\"},\n"
                            %("hash"+str(it)+":"+fn[ct]+":time:"+bb.split(',')[0]))
            ct+=1
        except:
            pass
outFile.seek(outFile.tell()-3)
"""
it=len(outData)-1
outFile.write("{\"name\":\"hash:%s\"},\n"%(hashidx[it].strip()))
aa=outData[it]
outFile.write("{\"name\":\"%s\"},\n"%(aa[0]))
for bb in aa[1][:-1]:
    outFile.write("{\"name\":\"time:%s\"},\n"
                          %(bb.split(',')[0]))
outFile.write("{\"name\":\"time:%s\"}\n"
                          %(bb.split(',')[0]))
"""
outFile.write('],')
outFile.write('\"links\":')
outFile.write('[')



for it in range(len(outData)):
    outFile.write("{ \"source\":\"%s\",\"target\":\"%s\",\"value\":%f },\n"
                 %("DataBase",
                 "hash:"+(hashidx[it].strip()),
                   tct[it]/sum(tct)))
    ct=0
    for aa in outData[it]:
        try:
            outFile.write("{ \"source\":\"%s\",\"target\":\"%s\",\"value\":%f },\n"
                    %("hash:"+(hashidx[it].strip()),
                    "hash"+str(it)+":"+fn[ct],
                    len(aa[1])/tct[it]))
            for bb in aa[1][:]:
                outFile.write("{ \"source\":\"%s\",\"target\":\"%s\",\"value\":%f },\n"
                    %("hash"+str(it)+":"+fn[it],
                    "hash"+str(it)+":"+fn[ct]+":time:"+bb.split(',')[0],
                    1/sum(tct)))
            ct+=1
        except:
            pass
outFile.seek(outFile.tell()-3)
outFile.write(']')
outFile.write('}')
outFile.close()
