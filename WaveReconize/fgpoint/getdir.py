DIR = "D:/Weiyuan/"
CATLOG = "catlog/"
TEMPLATES = "templates/"
import os
from obspy import read as pread
from obspy import Stream
class GetLogDir():
    def __init__(self,DIRS,time=[2015330,2015365]):
        self.DIRS=DIRS
    def GetDirIter(self):
        for itr in os.walk(self.DIRS):
            path = itr[0]
            for fileName in itr[2]:
                if(fileName[-4:]!=".out"):
                    continue
                files = fileName.split(".")
                if(int(files[2]) > 2015330 and int(files[2]) <= 2015365):
                    yield path+fileName,files[1]+'/',files[2]+'/'
    def GetDirList(self):
        logDirs=[]
        for itr in self.GetDirIter():
            logDirs.append(list(itr))
        return logDirs
def GetLogFile(fileName):
    file=open(fileName,"r")
    time=[]
    for itr in file.readlines():
        slt=[aa for aa in itr.split(" ") if len(aa)>0]
        time.append(float(slt[1]))
    return time
    
class GetDirFile():
    def __init__(self,DIRS):
        self.DIRS=DIRS
    def GetIter(self):
        for itr in os.walk(self.DIRS):
            path = itr[0]
            for fileName in itr[2]:
                if(self.NameFunc(fileName)==True):
                    yield path+"/"+fileName  
    def GetList(self):
        logDirs=[]
        for itr in self.GetIter():
            logDirs.append(itr)
        return logDirs

class GetTemplate(GetDirFile):
    def NameFunc(self,fileName):
        names=fileName.split('.')
        if(len(names)<=2):
            return False
        
        if(names[1]=='s28'):
            return True
        else:
            return False


def GetSacInfo(fileName):
    stream=pread(fileName)
        
    time=[stream[0].stats.sac.nzyear,
                stream[0].stats.sac.nzjday,
                stream[0].stats.sac.nzhour*3600+
                stream[0].stats.sac.nzmin*60+
                stream[0].stats.sac.nzsec+
                stream[0].stats.sac.nzmsec/1000]
    
    return stream[0].data,time

def GetTempFiles():
    sss=GetTemplate(DIR+TEMPLATES)
    lst=sss.GetList()
    group=[]
    Dict={}
    for itr in lst:
        names=itr.split(".")
        if(Dict.get(names[0])==None):
            Dict[names[0]]=[]
            Dict[names[0]].append(itr)
        else:
            Dict[names[0]].append(itr)

    for itr in Dict:
        group.append(Dict[itr])

    return group