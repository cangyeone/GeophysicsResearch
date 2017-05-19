import h5py
import numpy as np

file = h5py.File('D:/GitHub/GeophysicsResearch/H5test/cavity_output/cavity_0.hdf5',
        #libver='latest'
        'r')

for itr in file:
    print(itr)
print("==============")
data1=file["particles"]
for itr in data1:
    print(itr)
print("==============")
data2=data1["fluid"]
for itr in data2:
    print(itr)
print("==============")
data3=data2["arrays"]
for itr in data3:
    print(itr)
print("==============")
data4=data3["x"]
for itr in data4:
    print(itr)
print("==============")
#print(dataf['None'])
#print(file.visit(file.keys()))
#bdry=dataf['boundary']
#flid=dataf['fluid']
#flid=dataf['fluid']['arrays']['v'][:]
#print(type(flid))
#for itr in dataf['fluid']:
#    print(itr)
#print(np.shape(flid['arrays']['rho'][:]))


