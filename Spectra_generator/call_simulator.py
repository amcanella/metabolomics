# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:27:28 2024

@author: Alonso
"""
import simulator
from simulator import process_data 
from simulator import Simulator
import time 

p = process_data('C:/txts/Metabo_tables_13.xlsx')
d = p.create_dict()

s = Simulator(dictionary = d, met_data=p.met_data, clust_data = p.clust_data)

print(f'this is a test {p.met_data[0][6]}')

NFREQ = 22_473 #ZEROS REMOVED 32_768 #52_234 #32768
SAMPLES = 10_000
#NO UREA
mets = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,61,62,63, 65,66,67] #np.arange(1,26) #[3,4,5]
nmet = len(mets)
noise = 0.0001

spectrum = [0]*SAMPLES
conc = [0]*SAMPLES

start = time.perf_counter()
for i in range(SAMPLES):

    if i == SAMPLES/2:
        print(f'{i} We are half way through!')
      
    spectrum[i], conc[i] = s.constructor(mets, noise)
    
end =  time.perf_counter()
time = (end - start )/60

print('\nDone with simulating!')

s.csv_gen( f'x_{SAMPLES}_{nmet}_{NFREQ}_44.csv', NFREQ, spectrum)
s.csv_gen( f'y_met_{SAMPLES}_{nmet}_{NFREQ}_44.csv', 67, conc) #leave as 67

