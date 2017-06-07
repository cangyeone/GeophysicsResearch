import os
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
    
    

            
