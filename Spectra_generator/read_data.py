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

#Collects the peaks information
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
    v = peaks_data(input_met) #Collects the info from the peaks 
    #Define dictionary to arrange the peaks of each cluster
    # groups_data = defaultdict(list)
    groups_data = {}
    # ---------------------------------------------------
    #It makes more sense to go through the row once and classify directly
    #than going through the different ids and run v for every id there is 
    # for key in input_met:
    # --------------------------------------------------
    #Make a dict with two level, upper label is the metabolite number 
    #and the second level is the number of cluster
    #this way we can print cluster by cluster 
    
    for row in v:
        key = row[0]
        key_2 = int(row[2])
        if key not in groups_data:
            inner_dict = {}
            groups_data[key]=inner_dict
        if key_2 not in inner_dict:
            groups_data[key][key_2]=[row]
        else:
            groups_data[key][key_2].append(row)
        
    # rr = list(groups_data.items()) 
        
        # if key_2 not in groups_data[key]:
        #     groups_data[key][key_2]=[]
        # groups_data[key][key_2].append(row)
    
    # for row in v:
    #     key_2 = row[2]
    # With defaultdict
    # for row in v:
        
    #     #Append first the 
    #     key = row[0]
    #     groups_data[key].append(row)
        
    # keys = list(dict.keys(groups_data))
        # groups_data[key].append(row)
            #TO add the groups_data[1][-1][0]
        #See why the int data in peaks_m gets stored as float in v 
    # for row in groups_data:
    #     key = row[2]
    #     groups_data[key].append(row)
        # if key in groups_data:
        #     groups_data[key].append(row)
        # else:
        #     groups_data[key] = [row]
        
        
    # def plot_fig(row):
        
    #     name = row[1]
    #     x0 = row[4]
    #     gamma=row[5]
    #     print('Peak', c,' with a centre set on ', x0, 'ppm  and a width of ', gamma, 'ppm ')
    #     x = np.linspace(0, 10, 1000)
    #     y = lorentzian.loren(x,x0,gamma)
        
    #     return plt.plot(x,y, label=(name, c) )
    # NEW PLOT TO PLOT CLUSTERS
    name = 0  
    c = 0 #COUNTER TO NOT PLOT THE FIRST PEAK AND WAIT FOR WHOLE CLUSTER 
    clusterr=0
    idd=0
    s=0
    
    for key,value in groups_data.items():#each met
        for key_cluster, list_peaks in value.items():#each cluster
            for row in list_peaks:#inside the cluster
                
                name = row[1]
                x0 = row[4]
                gamma=row[5]
                x = np.linspace(0, 10, 1000)
                #Add the correction factor for the centre and Hs for every cluster 
                if row[0]==idd and row[2]==clusterr:
                    
                    # Might work directly by writting in y, y+=?, no need of suma function?
                    y = lorentzian.loren(x,x0,gamma)
                    s = lorentzian.suma(s,y)
                    c+=1 
                    # print('Peak',c,'with a centre of', x0, 'ppm and a with of ',gamma)
                else:
                    # if c>0:
                    #     plt.plot(x,s, label=(name, row[2]))
                    
                    #New metabolite begins
                    print('\n','Your metabolite:', row[1], 'with cluster', row[2],'\n')
                    y = lorentzian.loren(x,x0,gamma)
                    s=y
                    c=1
                print('Peak',c,'with a centre of', x0, 'ppm and a with of ',gamma)
                idd=row[0]
                clusterr=row[2] 
                #Como saber cual es el final del cluster 
                # plt.plot(x,s, label=(name, row[2]))
            plt.plot(x,s, label=(name, row[2]))
        plt.gca().invert_xaxis()
        plt.xlabel('ppm')
        plt.title('Clusters ')
        plt.grid(True)
        plt.legend(loc='upper left') #'best', 'center right'
        plt.show()
        
        
# # ----------------------------------------------------------------------
    # # |If you want to plot all peaks      
    # def plot_peaks(groups_data):
    #     name = 0  
    #     # custom_cmap = matplotlib.colors.ListedColormap(['red','yellow','blue'])
    #     # color = ['b','b','g','o','p','y','bl','w']
    #     c = 0
    #     fig, ax = plt.subplots()
    #     #NEW PLOT PROCEDURE WITH THE DICT TO PLOT PEAKS
    #     for key,value in groups_data.items():
    #         for key_cluster, list_peaks in value.items():
    #             for row in list_peaks:
                     
    #                 if name == row[1]:
    #                     c +=1
    #                 #     color = color[c]
                        
    #                 else:
    #                     print('\n','Your metabolite:', row[1], '\n')
    #                     c=1
    #                 #     color = color[c]
    #                 name = row[1]
    #                 x0 = row[4]
    #                 gamma=row[5]
    #                 print('Peak', c,' with a centre set on ', x0, 'ppm  and a width of ', gamma, 'ppm ')
    #                 x = np.linspace(0, 10, 1000)
    #                 y = lorentzian.loren(x,x0,gamma)
    #                 ax.plot(x,y, label=(name, c) ) #'${name}$'.format(name=name))
    #     ax.invert_xaxis()
    #     ax.set_xlabel('ppm')
    #     ax.set_title('Peaks ')
    #     ax.grid(True)
    #     ax.legend(loc='upper left') #'best', 'center right'
    #     return fig

    # peaks_fig = plot_peaks(groups_data)
#  # ------------------------------------------------------------------------   
    
    #Make a function for plotting where input is v or w 
    #Plot both??
    #Init the store single set of figure and axes, ax allows to invert the axes later
    # fig is used to store the actual graph inside it and ax for the axes class
    # fig, ax = plt.plot()
    
    # "'
    # name=0
    # count=1
    # with plt.ion():
    #     fig = plt.figure()
    # for met in v:
        
    #     # Set the centre and the width for plotting
    #     if met[1]==name:
    #         count+=1
    #     else:
    #        print('\n','Your metabolite:', met[1], '\n')
    #        count=1
    #     name = met[1]
    #     x0= met[4]
    #     gamma= met[5] #0.02 #met[4] because i dont have the info of many cluster 
    #     print('Peak', count,' With a centre set on ', x0, 'ppm  and a width of ', gamma, 'ppm is represented in the graph below.')
    #     #TODO: apply same color to the clusters of the same metabolite
    #     x = np.linspace(0, 10, 1000)
    #     y = lorentzian.loren(x,x0,gamma)
    #     if count==1:
    #         plt.plot(x,y, label= name) #'${name}$'.format(name=name))
    #     else:
    #         plt.plot(x,y)
    #     plt.gca().invert_xaxis()
    #     plt.xlabel('ppm')
    #     plt.title('Peaks ')
    #     # plt.pause(2)
    #     # plt.show()
    
    # plt.gca().invert_xaxis()
    # plt.xlabel('ppm')
    # plt.title('Peaks ')
    # plt.grid(True)
    # plt.legend(loc='best')
    # plt.show()
    
    # "'
    
    # ax.plot()    
    # ax.invert_xaxis() 
    # ax.set_xlabel('ppm')
    # ax.set_title('Plot of peaks')
    # ax.grid(True)
    # plt.legend(loc='best')
    # plt.show()
    
    