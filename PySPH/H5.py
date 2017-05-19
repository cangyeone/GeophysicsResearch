import h5py
import numpy as np
import os


def getArray(file,outfile,cont):
    if(cont%5!=0):
        return
    particle=file["particles"]
    fluid=particle["fluid"]
    solid=particle["boundary"]
    fluid_a=fluid["arrays"]
    solid_a=solid["arrays"]
    outfile.write("{{\"fluid\":[[%f,%f,%f,%f],"%(0,0,0,0))
    print(len(fluid_a["x"]))
    for ii in range(len(fluid_a["x"])):
        outfile.write("[%f,%f,%f,%f],"%(fluid_a["x"][ii],fluid_a["y"][ii],fluid_a["z"][ii],4))
    outfile.write("[%f,%f,%f,%f]],"%(0,0,0,0))
    
    x=solid_a["x"]
    y=solid_a["y"]
    z=solid_a["z"]
    print(len(x))
    outfile.write("\"solid\":[[%f,%f,%f,%f],"%(0,0,3,0))
    maz=np.max(z)
    miz=np.min(z)
    mrg=maz-miz    
    for i in range(len(x)):
        outfile.write("[%f,%f,%f,%f],"%(x[i],y[i],z[i],4*(1-(z[i]-miz)/mrg*0.6+0.4)))
    outfile.write("[%f,%f,%f,%f]]}}"%(0,0,0,0))
    
outfile=open("out.json","w")
mydir=os.walk(os.getcwd())
cont=0
for itr in mydir:
   cdir=itr[0]
   print(cdir)
   for cf in itr[2]:
       if(cf[-4:]=="hdf5"):
           try:
               file=h5py.File(cdir+"/"+cf,"r")
               getArray(file,outfile,cont)
               file.close()
               if(cont%5!=0):
                   print(cf)
               cont += 1
           except:
               file=h5py.File(cdir+"/"+cf,"r")
               getArray(file,outfile,cont)
               file.close()
               if(cont%5!=0):
                   print(cf)
               cont += 1
outfile.close()