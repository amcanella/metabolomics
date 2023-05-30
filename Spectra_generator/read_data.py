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
import lorentzian
from collections import defaultdict
# path = 'C:/txts/peaks_table.txt'
path = 'C:/txts/Copia de Metabo_tables_3.xlsx'
# NO SE PUEDE COGER DE UN EXCEL CON AUTOGUARDADO!!
# path = "C:/Users/Alonso/OneDrive - Fundacio Institut d'Investigacio en ciencies de la salut Germans Trias i Pujol/Escritorio/WORK/Copia de Metabo_tables.xlsx"

#Read data from excel 
#Use the excel file line to not read the excel everytime you read a sheet 
xls = pd.ExcelFile(path)
mets_x = pd.read_excel(xls, 'Mets', header=0)
clust_x = pd.read_excel(xls, 'Clusters')
peaks_x = pd.read_excel(xls, 'Peaks')

# data = pd.read_csv(path,"\t" , header = 1)
print('DATA ISSS \n', mets_x)

#Store data in a matrix 
mets_m = mets_x.values
print(mets_m)
clust_m = clust_x.values 
peaks_m = peaks_x.values

#Collect the data necessary for the lorentzian
# we need the centre of the cluster, width of the cluster although could be various, centre of the peak and width,
#in order to do this, we need to calle the function with a name or id of metabolite and we get all the data about it

def cluster_data(id):
        # Init variables 
        # centre_clust = 0
        # width_clust = 0
        # name_met = 0
        
    # In the case of an array with numbers only 
    # a = np.array(peaks_m[:,1])
    # where = np.where(a==2)
    
    #id = [3,4] #para cuando queramos plotear varios metabolitos a la vez
    total_clusters = [] #Init list 
    for i in id:
        for row in clust_m:
            if len(row)>0 and row[0]==i: #and len(row)>=7: #length of the row is 9 elements, just preventive
            #id of met, name, number of clusters, concentration, centre of cluster, width of cluster 
                total_clusters.append([i, mets_m[i-1,1],mets_m[i-1,4], mets_m[i-1,5], row[6], row[8]])

        # indexes = clust_m[:,0]#we could avoid this step and store the whole row into f, but maybe to messy
        # f = np. where(indexes == i)[0] #This [0] makes an array
    
    # if (clust_m[:,0] == id):
    #centre and width of the cluster
    # centre = clust_m[f,6]
    # width = clust_m[f,6]
    
    return total_clusters #name_met, centre_clust, width_clust = mets_m[id,1], clust_m[id,6], clust_m[id,8]



    #return name_met, centre_clust, width_clust, where 

#Separate the different values of the columns 
# metabolitess = mets[:,0]
# clusterss = mets[:,1]
# peaksss = mets[:, 2:7]

# my_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
# print("The index of element C is ", my_list.index('C'))

def peaks_data(id):
    #id=[3]
    total_peaks = []
    for i in id:
        for row in peaks_m:
            if len(row)>0 and row[0]==i:
                                    #id, name of met, cluster number, peak number, centre, width 
                total_peaks.append([i, mets_m[i-1,1],row[1],row[2],row[3], row[4]])
    
    return total_peaks
#TODO, add ranges and use them for the movement of the clusters


if __name__ == "__main__":
    
    #Store the data from the matrixes in a variable
    input_met = [3,4,5]
    w = cluster_data(input_met)#Make a plot of clusts function
    v = peaks_data(input_met) #Make a plot of peaks funct
    #Define dictionary to arrange the peaks of each cluster
    groups_data = defaultdict(list)
    
    for row in v:
        #See why the int data in peaks_m gets stored as float in v 
        key = row[2]
        groups_data[key].append(row)
        # if key in groups_data:
        #     groups_data[key].append(row)
        # else:
        #     groups_data[key] = [row]
            
    #Make a function for plotting where input is v or w 
    #Plot both??
    #Init the store single set of figure and axes, ax allows to invert the axes later
    fig, ax = plt.subplots()
    name=0
    i=1
    for met in v:
        
        # Set the centre and the width for plotting
        if met[1]==name:
            i+=1
        else:
           print('\n','Your metabolite:', met[1], '\n')
           i=1
        name = met[1]
        x0= met[4]
        gamma= met[5] #0.02 #met[4] because i dont have the info of many cluster 
        print('Peak', i,' With a centre set on ', x0, 'ppm  and a width of ', gamma, 'ppm is represented in the graph below.')
        #TODO: apply same color to the clusters of the same metabolite
        x = np.linspace(0, 10, 1000)
        y = lorentzian.loren(x,x0,gamma)
    
        ax.plot(x,y)
        
    ax.invert_xaxis() 
    ax.set_xlabel('ppm')
    ax.set_title('Plot of clusters')
    ax.grid(True)
    plt.show()
    
    