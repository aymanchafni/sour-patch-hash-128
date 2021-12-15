#!/usr/bin/env bash
# -*- coding: utf-8

#%%
import sys
from bitstring import BitArray
import json
import random
from scipy import stats
import numpy as np
import pandas as pd
import hashlib
import matplotlib.pyplot as plt

#%%
########################################
#
# réaliser une fonction de hash moins
# mauvaise
#

#%%
###########################################


def serialize(obj) :
     
     serialized = json.dumps(obj).encode()
     obj_bits = BitArray(serialized)

     return obj_bits

#%%
###########################################


#%%
###########################################
def sour_patch_hash_128(s):
    bits = serialize(s)
    prime_128= [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107, \
        109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241, \
            251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397, \
                401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563, \
                    569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719]
   
    # Determinism : control the random state 
    

    
    for i in range(bits.len) :
        bits[i] = not bits[i] 

    random.seed(bits.uint)
    
    bits_array = [i for i in bits]
    random.shuffle(bits_array)
    bits = BitArray(bits_array)


    val = bits.uint 

    bits = BitArray()

    # Confusion & Diffusion
    for p in prime_128:
        bit  = val % p % 2
        bits.append(f'0b{bit}')


    return bits.uint

#%%
########################################


#%%
########################################

def test_chi_square(results, cases):
    freq = np.zeros([cases,1])
    for item in results : 
        hash = int(item[0]) % cases
        freq[hash]+=1

    return freq, stats.chisquare(freq)


#%%
#######################################
def md5(s) :
    m= hashlib.md5()
    m.update(bytes(s,'utf8'))

    return m.digest()

#%%
########################################

def read_write(filer,filew,func) :    
    with open(filer,"r") as f1:
        with open(filew, "w") as f2:
            for line in f1:
                f2.write(f"{func(line.rstrip())}\n")
#%%
########################################

if __name__=="__main__":
    if len(sys.argv)==3:
        read_write(sys.argv[1],sys.argv[2],sour_patch_hash_128)
        filew = sys.argv[2]
    else:
        filer = input("donnez le nom de fichier de donnees a hacher")
        filew = input("donnez le nom de fichier pour ecrire les resultats")
        read_write(filer,filew,sour_patch_hash_128)
        
    results = pd.read_table(filew,names = ['hash']).to_numpy()
    test_result = test_chi_square(results,100)
    
    print(test_result[1])
    plt.plot(test_result[0])
    plt.show()

# random.txt
# results.txt
# %%
