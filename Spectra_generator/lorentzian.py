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
    return (gamma/(np.pi*(gamma**2+(x-x0)**2)))

#define the x axis 
# x = np.linspace(10, 0, 1000)

def suma(a,b):
    
    return a+b

# # #define the parameters here for now 
# x01= 3.24 #centre
# gamma1 = 0.02 #width

# x02= 5.73 #centre
# gamma2 = 0.03 #width

# #define the x axis 
# x = np.linspace(10, 0, 1000)
# y1 = loren(x, x01, gamma1)
# y2 = loren(x, x02, gamma2)
# sumi = suma(y1,y2)

# fig, ax =plt.subplots(3,1,figsize=(8, 12))

# ax[0].plot(x,y1)
# ax[0].set_title('Subplot 1')
# ax[0].set_xlabel('X')
# ax[0].set_ylabel('Y1')
# ax[0].grid(True)

# ax[1].plot(x,y2)
# ax[1].set_title('Subplot 2')
# ax[1].set_xlabel('X')
# ax[1].set_ylabel('Y2')
# ax[1].grid(True)

# ax[2].plot(x,sumi)
# ax[2].set_title('Subplot 3')
# ax[2].set_xlabel('X')
# ax[2].set_ylabel('Y3')
# ax[2].grid(True)

# # plt.tight.layout()
# plt.show()
# a = int(input('ingrese el valor de a='))
# b= int(input('ingrese el valor de b='))
# suma()


# #evaluate the lorentzian function at each x value 
# y = loren(x,x0,gamma)

#plot the curve 

# plt.plot(x,y)
# plt.show()
