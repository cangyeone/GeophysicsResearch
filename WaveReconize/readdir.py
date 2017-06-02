import numpy as np
def FileToList(fileName):
    f=open(fileName,"r",encoding=None)
    fdata=f.readlines()
    data=[]
    for itr in fdata:
        #print(itr)
        if(itr[:2]=='20'):
            data.append([ii.strip() for ii in itr.split() if(len(ii)>0)])
    return data
la=31.0
lo=102.36
dt1 = FileToList("dir/dir1.txt")
dt2 = FileToList("dir/dir2.txt")
#print(dt1[:3])
#print(dt2[:3])
for itr in dt2:
    si1=np.sin(np.pi/2-la/180*np.pi)*6731*np.tan(np.abs(float(itr[3])-lo)/180*np.pi)
    si2=np.sin(np.abs(float(itr[2])-la)/180*np.pi)*6371
    si=np.sqrt(si1**2+si2**2)
    if(si<400):
        print(si)






    