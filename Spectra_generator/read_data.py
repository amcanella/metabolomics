# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:09:34 2023

@author: Alonso
"""
import numpy as np 
import pandas as pd 
# import matplotlib
# matplotlib.use('TkAgg')
import matplotlib.pyplot as plt 
import matplotlib.colors 
import lorentzian
from collections import defaultdict
from copy import deepcopy
from scipy import integrate
import random
import datetime
import time
# from scipy.signal import find_peaks 

# path = 'C:/txts/peaks_table.txt'
path = 'C:/txts/Copia de Metabo_tables_10.xlsx'
# NO SE PUEDE COGER DE UN EXCEL CON AUTOGUARDADO!!
# path = "C:/Users/Alonso/OneDrive - Fundacio Institut d'Investigacio en ciencies de la salut Germans Trias i Pujol/Escritorio/WORK/Copia de Metabo_tables_3.xlsx"

#Read data from excel 
#Use the excel file line to not load the excel everytime you read a sheet , TODO: ADD THIS TO MAIN 
xls = pd.ExcelFile(path)
mets_x = pd.read_excel(xls, 'Mets', header=0)
clust_x = pd.read_excel(xls, 'Clusters')
peaks_x = pd.read_excel(xls, 'Peaks')

#Store data in a matrix 
mets_m = mets_x.values
clust_m = clust_x.values 
peaks_m = peaks_x.values


# we need the centre of the cluster, centre of the peak and width,
#in order to do this, we need to call the function with a name or id of metabolite and we get all the data about it
#Collect the necessary cluster data 
def cluster_data(met_id):#TODO: try to be consistent and name functions with the same case 

    total_clusters = [] #Init list 
    for i in met_id:
        for row in clust_m:
            if len(row)>0 and row[0]==i: #length of the row is 9 elements, just preventive, use while
                # width_n=lorentzian.norm(row[8]) #Commented until all values stored in excel #NORMALIZE the widths, it comes in MHzs
                                #id of met, name, number of clusters, cluster number, reference concentration?in mets, centre of cluster, width of cluster, number of Hs?out, rango 0, rango 1
                total_clusters.append([i, mets_m[i-1,1],  mets_m[i-1,4], row[1], mets_m[i-1,5], row[6], row[8], row[4], row[2],row[3]])
    
    return total_clusters 


#Collects the peaks information
def peaks_data(met_id):
    #id=[3]
    total_peaks = [] #init the peaks list 
    total_areas = [] #init the areas sum list 
    for i in met_id:
        suma=0 #restart the sum for another met
        for row in peaks_m:
            if len(row)>0 and row[0]==i:
                #1. CONVERT WIDTHS TO PPM and add the variation
                width = row[5]
                width_var = lorentzian.width_set(width)
                
                
                width_norm = width / 500 #quick check to see if all new width values are within the 10 % at least (i know it is 4 but might be some outties)
                pc= width_norm*0.1 
                print(f'{i} {width_norm:.6f}  {width_var:.8f}')
                if  width_norm+pc >= width_var >= width_norm-pc:
                    print('True')    
                else:
                    print('False')
                    # raise ValueError('width variation out of range ')
                    
                #2. NORMANILIZE area, not anymore, AREA AND CONCENTRATION GO DIFFERENT WAYS 
                area_peak = row[6]
                # ref_concentration=mets_m[i-1,5] #concentration stored in the chenomx 
                # area_norm = area_peak/ref_concentration
                
                #3. GET THE TOTAL AREA OF THE MET BY ADDING ALL THE PEAKS 
                # suma+=area_norm #sum the areas of the different peaks already normalized
                suma+=area_peak #sum the areas of the different peaks
                
                #id, name of met, cluster number,   peak number,  centre,   width normalized&var, area, width without variation 
                total_peaks.append([i, mets_m[i-1,1],row[1],row[2],row[3], width_var, area_peak, width_norm]) # mets_m[i-1,6] max conc in urine profiler
                
        total_areas.append(suma) #append the sum (ONLY USED TO EASILY ADD IT TO THE mets, since it is mets data)
    return total_peaks,total_areas

# METS DATA 
def mets_data(mets_id, areas):
    c=0
    total_mets=[]
    for i in mets_id:
        for row in mets_m:
            if row[0]==i: #while with condition instead of for and if?
                concentration = random.uniform(0, row[6]) #get a float between 0 and MAX concentration in chnMX
                # concentration = [desired_con_1, ..] 
                #mitad= row[6]/2 #Otra forma de hacerlo seria utilizando la gaussiana
                #concentration = lorentzian.gaussian(mitad, mitad)
                # id number of met, name of met, sample concentratio in ChenoMx, MAX urine concentration, TOTAL AREA OF MET, WISHED (rd concentration within ranges)
                total_mets.append([i,row[1],row[5], row[6], areas[c], concentration])
        c+=1
    return total_mets

# Function that saves a list into a dict by met ID and cluster number 
def saveInDict(lista):
    #Define dictionary 
    # groups_data = defaultdict(list)
    groups_data = {}
    # ---------------------------------------------------
    #It makes more sense to go through the row once and classify directly
    #than going through the different ids and run v for every id there is 
    # for key in input_met:
    # --------------------------------------------------
    #Make a DICT with two level, upper label is the metabolite number 
    #and the second level is the number of cluster
    #this way we can print cluster by cluster 
    
    for row in lista:
        key = row[0]
        key_2 = int(row[2])
        if key not in groups_data:
            inner_dict = {}
            groups_data[key]=inner_dict
        if key_2 not in inner_dict:
            groups_data[key][key_2]=[row] #If the key does not exist, create new dict
        else:
            groups_data[key][key_2].append(row) #If the key exists, then append
        
    return groups_data

#Function that appends a new peak centre within pH 7 
def addShift(d):
    
    #I would not change it directly in peaks_dict because I think it is good to keep the reference of pH 7 
 
    for row in cluster_l:
        met = row[0]
        clust_number = row[3]
        clust_centre=row[5]
        
        rango0=row[8]
        rango1=row[9]  #0.04
        sigma = (rango1 - rango0)/2 #0.02 
        #New cluster centre
        new_centre = lorentzian.gaussian(clust_centre, sigma)
        shift = new_centre - clust_centre
        print('\n The cluster',clust_number,'old centre',clust_centre,'new centre', new_centre, 'of difference',shift,'and a range', sigma,'\n')
        
        for row_2 in d[met][clust_number]:
        
            peak_centre=row_2[4]
            
            
            # diff = peak_centre-clust_centre
            # row_2[4] = new_centre + diff #new_cluster centre INSTEAD of row[5]
            # diff_clusts = new_centre - clust_centre #misma variable que shifts
            # diff_null = diff_clusts - shift #should be 0 DELETE
            # new_peak = peak_centre + diff_clusts
            
            new_peak = peak_centre + shift 
            row_2.append(new_peak) #creo que mas correcto seria hacer un for keys, values y appender en values, YA PROBE Y NO FUNCIONA SOL:DEEPCOPY
            #se puede simplificar como row_2[4]+= new_centre - clust_centre
            print('The peak', row_2[3], 'had old peak', peak_centre,'a new peak', new_peak,'and a shift', shift)
        # return new_groups_data 
    return d

    
    
#FUNCTION TO PLOT SIGNALS 
def plot_funct(x,y,name,texto,number,idd):
    
    plt.plot(x,y,label = (name,texto, number))
    plt.gca().invert_xaxis()
    plt.xlabel('ppm')
    plt.title('Clusters '+ name + ' '+ str(idd))
    plt.grid(True)
    plt.legend(loc='upper left') #'best', 'center right'
    plt.show()#A PLOT SHOW PER METABOLITE
    
     
#FUNCTION to plot the peaks  
def plot_compounds(dict_, iteration_number=1):
       
   
    # Init variables 
    name = 0  
    c = 0 #Peak Counter, keep track of the peak sequence 
    ccc = 0 #MET counter 
    clusterr=0
    idd=0
    s=0 #suma de picos
    s_sol = 0 #suma de picos solution
    ss=0 #suma de clusters
    m=0 #suma de mets 
    m_sol = 0 #suma of solutin mets 
    #CHECK FUNCT
    integration_values = []
    integration_values_sum = 0
    int_total_area=0
    zcheckpoint=[]
    conc_solution_row = [0]*len(mets_m)
    
    for key,value in dict_.items():#each met
        ss=0 #reset suma de clusters within met
        ss_sol = 0 #reset the solution of the suma of clusters 
        for key_cluster, list_peaks in value.items():#each cluster
            for row in list_peaks:#inside the cluster
                
                #peak variables 
                id_met = row[0]
                name = row[1]
                clust_number = row[2]
                peak_number = row[3]
                old_centree=row[4]
                gamma=row[5]
                area_r = row[6]
                fix_width = row[7]
                x0 = row[8] #new centre
                        # i WAS DOING THIS TO PLOT AND SEE PROGRESS                 #THIS INDEED MAKES SENSE
                #TODO: 1. SUM ALL THE PEAKS BY METS ONLY, NO NEED TO SEP CLUSTS, 2. MAKE MATRIX MULT TIMES CONCENT AT THE END
                #met variables 
                concentration_ref = mets_l[ccc][2]
                total_area = mets_l[ccc][4]
                concentration = mets_l[ccc][5] #TODO: add this wished concentration to the prompt input 
                conc_solution_row[id_met-1] = concentration #esto es parte del met, no del peak, osea que podria estar en el primer loop
                
                # x = np.linspace(-1, 11.016, 32768) #real spectra have a spectral width of 12.016 ppm centered in 5 and the n of samples 
                # x = np.linspace(0.04, 10, 32_768) #start, end, length variables 
                x = np.linspace(-1.997, 12.024, 32_768) #start, end, length variables 
                

                shift2 = x0 - old_centree  #this is done to compare and check the shifts in every cluster
                #Add the correction factor for the centre and Hs for every cluster 
                if row[0]==idd and row[2]==clusterr:
                    
                    # Might work directly by writting in y, y+=?, no need of suma function?
                    y = lorentzian.loren(x,x0,gamma,area_r,concentration, concentration_ref)
                    s = lorentzian.suma(s,y)
                    
                    #NN SOLUTION SNIPPET
                    y_sol = lorentzian.loren(x,old_centree,fix_width,area_r,concentration, concentration_ref)
                    s_sol = lorentzian.suma(s_sol,y_sol)
                    
                    c+=1 
                    # print('Peak',c,'with a centre of', x0, 'ppm and a with of ',gamma)
                else:
                    # if c>0:
                    #     plt.plot(x,s, label=(name, row[2]))
                    
                    #New metabolite begins
                    print('\n','Your metabolite:', row[1], 'with cluster', row[2],'\n')
                    y = lorentzian.loren(x,x0,gamma, area_r, concentration,concentration_ref)
                    s=y
                    
                    
                    #SOLUTION SNIPPET 
                    y_sol = lorentzian.loren(x,old_centree,fix_width,area_r,concentration, concentration_ref)
                    s_sol = y_sol
                    
                    c=1
                    
                print('Peak',c,'with a centre of', x0, 'ppm, old centre of',old_centree,'ppm, shift of',shift2,' and a concentration of ',concentration)
                idd=row[0]
                clusterr=row[2] 
                
                # plt.plot(x,y, label=(name, row[2]))#PLOT ALL THE PEAKS
                # plot_funct(x, y, name, clust_number, peak_number, idd) #Call the function to plot all peaks individually, 
                #                                                         otherwise a mess if plot function at the end of all the loop  
            # plt.plot(x,s, label=(name, 'sum peaks',row[2]))#PLOT the sum of peaks/ each cluster
            ss = lorentzian.suma(ss, s)#suma de clusters within compound 
            ss_sol = lorentzian.suma(ss_sol, s_sol)#suma de clusters within compound 
        # plot_funct(x, ss, name, clust_number, peak_number, idd)
        # plt.plot(x,ss,'r',label=(name, 'suma'))#PLOT the sum of clusters
        # plot_funct(x, ss, name, 'suma', idd, idd)
        m = lorentzian.suma(m, ss)
        m_sol = lorentzian.suma(m_sol, ss_sol)
        
        #add one to the index counter
        ccc+=1
        # #I want to check that the ints are 1
        integration_ss = np.trapz(ss,x) #No va a ser uno porque no dividimos por area total, es lo mismo que total area * wished concentration
        integration_values.append(integration_ss)
        
        #CHECKPOINT 
        if  concentration+0.00015 >= integration_ss >= concentration-0.00015:
            zcheckpoint.append(['Function', name, 'True']) #I recycle the ccc to count each met 
            print('True')
        indexes = str(list(new_dict.keys()))
        integration_values_sum += integration_values[-1]
        int_total_area += total_area * concentration / concentration_ref #the area of each met * the concentration of each met AND NOW DIVIDED BY REFERENCE SINCE I TOOK IT AWAY FROM THE AREA CALCULATION
    # TODO: ADD NOISE HERE, missing cadenas de proteinas later on 
    #TODO: make a noise function
    mu= 0 
    sigma = 0.0001
    
    noise = np.random.normal(mu, sigma, len(m))
    m_noise = m + noise
    integration_m_noise = np.trapz(m_noise,x)
    m1 = m/integration_values_sum #this is to prove that is  almost the same as int_total_area
    m2 = m/int_total_area
    m3 = m_noise/integration_m_noise #normalize function by dividing by integral of signal with noise
    #m_sol_n = m_sol/int_total_area  #TOTALLY WORKS BUT MORE PRECISE WITH INTEGRAL 
    m_sol_n = m_sol/np.trapz(m_sol, x) #normalize by dividing by integral 
    
    integration_total = np.trapz(m,x) #this is the same almost as int_total_area
    integration_total_2 = np.trapz(m1,x)
    integration_total_3 = np.trapz(m2,x)
    integration_total_4 = np.trapz(m3,x)
    integration_total_5 = np.trapz(m_sol_n,x)
    
    #Add date and time 
    current_datetime= datetime.datetime.now()
    f_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    
    #APPLY THE ZERO RANGES TO THE SPECTRUM 
    # m3[: 5557] = 0
    # m3[16107 : 16692] = 0
    # m3[ 28031 :] = 0
    m3 = lorentzian.ranges(m3) #CALL THE RANGES FX FOR 0 AREAS 
    m_sol_n = lorentzian.ranges(m_sol_n)
    
    # m_sol_n[: 5557] = 0
    # m_sol_n[16107 : 16692] = 0
    # m_sol_n[ 28031 :] = 0
    
    # NORMALIZE THE CONCENTRATION VALUES 
    # conc_solution_row =  [ value / sum(conc_solution_row) for value in conc_solution_row]
    # checkout= sum(conc_solution_row) #ALWAYS 1
    # "s = np.sum(yp, axis = 1).reshape((1000, 1))\n",
    # "yp = yp / s\n",
    
    
    plt.plot(x,m_sol_n, 'b', label = ('REFERENCE')) 
    plt.plot(x,m3, 'g', label = ('shift'))    
    # plt.plot(x,m1, 'r', label = ('ALL COMPOUNDS'))    
    # plt.plot(x,m2, 'b', label = ('ALL COMPOUNDS'))    
     
    plt.gca().invert_xaxis() # plt.xlim(12, -1)
    plt.xlabel('ppm')
    plt.title(f'All mets {indexes} {f_datetime}')
    plt.grid(True)
    plt.legend(loc='upper left') #'best', 'center right'
    plt.show()#A PLOT SHOW PER METABOLITE

    return m3, conc_solution_row, m_sol_n

 

if __name__ == "__main__":
    
    start = time.perf_counter()
    
    instances =  10
    result = [0]*instances
    conc_solution = [0]*instances
    m_alineado = [0]*instances
  
    #TODO: Restructure, I would store all the values in a list and make a dict with all of them, no need to call them every time we run and the for loop woulg go lower then :D
    for i in range(instances):   
        #Change the indexes to the metabolites you would like to see plot 
        #Create a rd function to select a number of mets and another to select which
        input_met = [3,4,5] #TODO: add a input() to add mets or retrieve mets randomly from list? Naa... would be cool but we need to call this automatically
        
        #Store the data from the matrixes in a variable
        cluster_l = cluster_data(input_met)#Collects the cluster info from the demanded mets into this list
        peaks_l , t_areas = peaks_data(input_met) #Collects the peaks info from the demanded mets, the total areas is to sum the peaks areas (no need anymore since integration)
        mets_l = mets_data(input_met, t_areas) #Collects the mets info and and the total area normalized into this list
        
        #TODO:variate the width of the peaks within a gaussians, there are different variations, some repeated 
        # less frequently than others, we gotta see this recurrency 

         # Store the list in a dictionary 
        peaks_dict = saveInDict(peaks_l)
        peaks_dict_copy = deepcopy(peaks_dict) #A shallow copy should not affect since we are adding a new value, not modifying, but it seems to append it
        
        # ---------------I THINK WE CAN START THE FOR LOOP FROM HERE 
        new_dict = addShift(peaks_dict_copy) #Llamar al copy, sino se produce el cambio en v 
        
        result[i], conc_solution[i], m_alineado[i]= plot_compounds(new_dict) #, iter_)
        
    #Current date and time
    current_datetime= datetime.datetime.now()
    f_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    # folder_path = 'C:/Repos/Metabolomics/Spectra_generator/result_'+f_datetime+'/'
    
    # np.savetxt(f'input_{f_datetime}.txt', result, delimiter=' ')   
    np.savetxt(f'x_{instances}.txt', result, delimiter=' ')   
    
    np.savetxt(f'y_met_{instances}.txt', conc_solution, delimiter=' ')   
    np.savetxt(f'y_alineado_{instances}.txt', m_alineado, delimiter=' ')   
        
    end = time.perf_counter()
    
    elapsed = end - start
    # ********__________-____________________________

