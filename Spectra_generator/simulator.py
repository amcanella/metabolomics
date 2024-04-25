# -*- coding: utf-8 -*-
"""
Created on March 20

@author: Alonso
"""
import pandas as pd
import math
import numpy as np 
import random 

class process_data:
    
    def __init__(self, file_name):
        
        self.file_name = file_name
        
        self.met_df = pd.read_excel(self.file_name, 'Mets')
        clust_df = pd.read_excel(self.file_name, 'Clusters')
        peak_df = pd.read_excel(self.file_name, 'Peaks')
        
        self.met_data = self.met_df.values
        self.clust_data = clust_df.values
        self.peak_data = peak_df.values
        

    def list_maker(self, array):
        #Add and remove data from list
        list_peaks = [list(a) for a in array]
        for row in list_peaks: 
            #Insert name of the met
            row.insert(1, self.met_data[int(row[0])-1][1])
            #Remove amplitude 
            row.remove(row[5])   
            
        return  list_peaks        
    
    #Create a dictionary with the peaks info, more accessible       
    def create_dict(self):
        
        list_peaks = self.list_maker(self.peak_data)
         
        peak_dict = {}
        for row in list_peaks:
            key = row[0]
            
            if math.isnan(row[2]):
                pass
            else:
                key_2 = int(row[2])
            if key not in peak_dict:
                inner_dict = {}
                peak_dict[key]=inner_dict
            if key_2 not in inner_dict:
                peak_dict[key][key_2]=[row] #If the key does not exist, create new dict
            else:
                peak_dict[key][key_2].append(row) 
        return peak_dict
    


class Simulator:
    
    def __init__(self, *, dictionary = {}, met_data, clust_data):
        
        self.dictionary = dictionary
        self.met_data = met_data
        self.clust_data = clust_data
        
        
    #Vary the width
    def set_width(self, width):
        spectral_f = 500 #samples are taken at 500 MHz

        width_norm = width/spectral_f #scaled width by the reference 500 MHz  
        return width_norm*random.gauss(1, 0.04) #4% small variation to the width of the peak
    
    #Shift the centres
    def set_new_centre(self, clusters):
        
        id_ = 0
        lista = []
        for row in clusters:
            met_id = row[0]
            
            #cluster ranges
            rango0=row[2]  #0
            rango1=row[3]  #0.04
            sigma = (rango1 - rango0)/2 #0.02 
            
            clust_centre = row[5]
            
            new_centre = random.gauss(clust_centre, sigma)
            shift = new_centre - clust_centre
            
            
            if met_id == id_ :
                pass
                
            else:
                id_ +=1
                lista.append([id_])
                
            lista[id_ - 1].append(shift)   
            
        return lista
                
         
        
    def lorentzian(self, x,x0,gamma,area_n,conc, conc_ref):
        return ((conc/conc_ref)*(2*gamma*area_n)/(np.pi*((gamma**2)+4*(x-x0)**2))) 
    
    #Make the zero areas
    def ranges(self, a):
    
        a[: 5557] = 0
        a[16107 : 16692] = 0
        a[ 28031 :] = 0
        return a
    
   
    def constructor(self, mets, noise):
            #Add the shift and the width variations and plot
            d = self.dictionary
            shifts = self.set_new_centre(self.clust_data)
            x = np.linspace(-1.997, 12.024, 32_768)
            raw_spect = 0
            conc_solution_row = [0]*len(self.met_data)
            
            for m in mets:
                concentration_urine =  self.met_data[m-1][6]
                wished = random.uniform(0, concentration_urine)

                conc_solution_row[m -1] = wished
                
                con_reference = self.met_data[m-1][5]
                
                for key, value in d[m].items():

                    for row in value:

                        shift = shifts[m-1][key]
                        new_centre = row[4] + shift


                        #Change width to ppm and add variation
                        width_var= self.set_width(row[5])

                        x0= new_centre
                        gamma = width_var
                        area = row[6]
                        conc = wished #wished concentration
                        conc_ref = con_reference
                        #call the lorentzian
                        raw_spect += self.lorentzian(x,x0,gamma,area,conc, conc_ref)
                        
            #Add noise           
            noise = np.random.normal(0, noise, len(raw_spect))
            spect_noise = raw_spect + noise
                        
            #Normalize to 1
            integral = np.trapz(spect_noise,x)
            spect = spect_noise/integral

            
            #Add the zero areas
            spect = self.ranges(spect)
            
            return spect, conc_solution_row
    