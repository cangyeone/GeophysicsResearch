# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 20:37:58 2016

@author: LLL
"""

from datasketch import MinHash, MinHashLSH

data1 = ['minhash', 'is', 'a', 'probabilistic', 'data', 'structure', 'for',
        'estimating', 'the', 'similarity', 'between', 'datasets']
data2 = ['minhash', 'is', 'a', 'probability', 'data', 'structure', 'for',
        'estimating', 'the', 'similarity', 'between', 'documents']
data3 = ['minhash', 'is', 'probability', 'data', 'structure', 'for',
        'estimating', 'the', 'similarity', 'between', 'documents']

# Create MinHash objects
m1 = MinHash(num_perm=128)
m2 = MinHash(num_perm=128)
m3 = MinHash(num_perm=128)

for d in data1:
    m1.update(d.encode('utf8'))
for d in data2:
    m1.update(d.encode('utf8'))
for d in data3:
    m1.update(d.encode('utf8'))
print((m1.hashvalues))
print((m2.hashvalues))
print((m3.hashvalues))
import numpy as np
print(np.shape(m1.hashvalues))
# Create an MinHashLSH index optimized for Jaccard threshold 0.5,
# that accepts MinHash objects with 128 permutations functions
lsh = MinHashLSH(threshold=0.5, num_perm=128)

# Insert m2 and m3 into the index
lsh.insert("m2", m2)
lsh.insert("m3", m3)

# Check for membership using the key
print("m2" in lsh)
print("m3" in lsh)

# Using m1 as the query, retrieve the keys of the qualifying datasets
result = lsh.query(m1)
print("Candidates with Jaccard similarity > 0.5", result)

# Remove key from lsh
lsh.remove("m2")