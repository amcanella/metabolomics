# -*- coding: utf-8 -*-
"""
Created on Wed May 29 11:27:28 2024

@author: Alonso
"""
import simulator_LF
from simulator_LF import process_data 
from simulator_LF import Simulator
import time 

import random 

p = process_data('C:/Repos/low_field_db.xlsx')
d = p.create_dict()
s = Simulator(dictionary = d, met_data=p.met_data, clust_data = p.clust_data, clust_dict=p.clust_dict())

print(f'this is a test {p.met_data[0][6]}')

NFREQ = 23_122 #ZEROS REMOVED 65536
SAMPLES = 1#0_000
#NO UREA, 64 nor cholate 37 for 292 peaks
#mets = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,38,39,40,41,42,43,44,45,46,47,48,49,50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,61,62,63,65,66,67] #np.arange(1,26) #[3,4,5]
mets = [1,2,3,4,5,7,9,22]
# mets = [3,4,5]
nmet = len(mets)
noise = 0.001              #0.0001

for j in range(1,11):
    
    print(j)
    spectrum = [0]*SAMPLES
    conc = [0]*SAMPLES
    aligned = [0]*SAMPLES
    
    noise_variable = noise * random.gauss(1, 0.1)
    start = time.perf_counter()
    for i in range(SAMPLES):
    
        if i == SAMPLES/2:
            print(f'\n {i} We are half way through!')
          
        spectrum[i], conc[i], aligned[i] = s.constructor(mets, noise_variable)  #, aligned[i]
        
    end =  time.perf_counter()
    timer = (end - start )/60
    
    print(f'\nDone with simulating! Time: {timer}')
    
    # s.csv_gen( f'low_field/prueba_8_mets/x_{j}_GLYBIEN.csv', NFREQ, spectrum)
    # s.csv_gen( f'low_field/prueba_8_mets/y_met_{j}_GLYBIEN.csv', 67, conc) #leave as 67
    
    # s.csv_gen( f'low_field/prueba_8_mets/y_aligned_{j}_GLYBIEN.csv', NFREQ, aligned)
    # print('----------------------------------------------------')
    



# import matplotlib.pyplot as plt 
# import numpy as np 

# x = np.linspace(0.3807, 9.9946, 22_473)
# plt.plot(x, spectrum[0], label = 'shifted')
# plt.plot(x, aligned[0], label = 'aligned')
# plt.legend(loc= 'upper right')
# plt.show()