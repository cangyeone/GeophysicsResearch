import h5py
import numpy as np

file = h5py.File('C:/Users/LLL/Documents/GitHub/GeophysicsResearch/H5test/cavity_output/cavity_0.hdf5',
        #libver='latest'
        'r')

for itr in file:
    print(itr)
dataf=file["particles"]
#print(dataf['None'])
#print(file.visit(file.keys()))
#bdry=dataf['boundary']
#flid=dataf['fluid']
flid=dataf['fluid']['arrays']['v'][:]
print(type(flid))
for itr in dataf['fluid']:
    print(itr)
#print(np.shape(flid['arrays']['rho'][:]))


