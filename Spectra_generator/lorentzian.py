# -*- coding: utf-8 -*-
"""
Alonso Moran Canella 

8.5.2023

"""

import numpy as np 
import matplotlib.pyplot as plt 


#define the function that will create the function 
def loren(x,x0,gamma):
    
    # I think this is the cauchy-lorentzian or sth return 1 / (np.pi * gamma * (1 + ((x - x0)/gamma)**2))
    return (2*gamma)/(np.pi*(4*(x-x0)**2)+(gamma)**2)

#define the x axis 
x = np.linspace(10, 0, 1000)
 
#define the parameters here for now 
x0= 3.24 #centre
gamma = 0.02 #width

#evaluate the lorentzian function at each x value 
y = loren(x,x0,gamma)

#plot the curve 

# plt.plot(x,y)
# plt.show()
