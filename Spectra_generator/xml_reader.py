# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 09:50:40 2023

@author: Alonso
"""
#Import libraries 
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET

#Write the path where the file is
# path = "C:/Users/Alonso/OneDrive - Fundacio Institut d'Investigacio en ciencies de la salut Germans Trias i Pujol/Escritorio/500_1H_glucose_edited.nmrML"
path = "C:/Users/Alonso/OneDrive - Fundacio Institut d'Investigacio en ciencies de la salut Germans Trias i Pujol/Escritorio/500_1H_glucose.xml"
# path = "C:/Users/Alonso/OneDrive - Fundacio Institut d'Investigacio en ciencies de la salut Germans Trias i Pujol/Escritorio/500_1H_glucose.xml"
# path = "C:/Repos/Metabolomics/Spectra_generator/500_1H_glucose_edited.nmrML"
# glucose_xml = pd.read_xml(path, namespaces= {"doc": "http://nmrml.org/schema"})
# xml = pd.DataFrame(path)



# glucose_xml = pd.read_xml(path)
# glucose_xml = pd.read_xml(path, xpath ="spectrumAnnotationList/atomAssignment/atomAssignmentList/multiplet/peakList/peak", namespaces= {"doc":"http://nmrml.org/schema}" })


tree = ET.parse(path)
eroot = tree.getroot()

stores_items = []

#Function that returns a list of dicts 
def xml_parser(root):
    # #Because the xml is using namespaces (namespaces are uniform resource identifiers (URI)
    # # and are used to provide uniquely named elements and attributes in an xml document) we
    # #have to add them to the paths
    
    # for lines in root.findall('./atomAssigment'):
        # spectrumAnnotationList
    for rows in root.findall('{http://nmrml.org/schema}spectrumAnnotationList/{http://nmrml.org/schema}atomAssignment/{http://nmrml.org/schema}atomAssignmentList/{http://nmrml.org/schema}multiplet'):
        stores_items.append(rows.attrib)
        print("tag:",rows.tag)
        print("attrib:",rows.attrib)
        print("text: ", rows.text)
        
        
        for lines in rows.findall('{http://nmrml.org/schema}peakList/{http://nmrml.org/schema}peak'):
            # store_n = lines.attrib.get('center')
            stores_items.append(lines.attrib)
            print("tag2: ", lines.tag)
            print("attribute2: ", lines.attrib)
            print("text2: ", lines.text)
            
    return stores_items

list_dicts = xml_parser(eroot)
df = pd.DataFrame(list_dicts)
array = df.values 


#Funtion that has the array type object as input with all the values and cleans it of Nans
def cleaner(arr):
    i=0
    indexes = []
    
    for rows in arr:
        value = rows[0]
        if value == rows[0]: 
            # mask = np.isnan(rows)
            centre_cluster = value
            indexes.append(i)
            i+=1
        else:
            rows[0]=centre_cluster
            i+=1
    
    arr=np.delete(arr, indexes, axis=0)
    return arr 

peaks_info = cleaner(array)
#We need to clean the dict 

# for dict in stores_items:
#     if len(dict)<2:
        
    # stores_items = [store_n]
# -----FUNTION-------------------    
# def parse_xml(root):
#     #In case there are attributes in the root, which i have in my case, i dont think i want them 
#     attr = root.attrib
#     # We call the first att insidde the atomAssigment, where the peaks are 
#     xml_data = {}
#     for child in root.findall('{http://nmrml.org/schema}spectrumAnnotationList/{http://nmrml.org/schema}atomAssignment/{http://nmrml.org/schema}atomAssignmentList/{http://nmrml.org/schema}multiplet'):
#         xml_data = {} #attr.copy()
#         xml_data.update(child.attrib)
#         store_itemss = []
#         for lines in child.findall('{http://nmrml.org/schema}peakList/{http://nmrml.org/schema}peak'):
#             #El ptoblema es que tengo varios peak con el mismo atributo
#             store_itemss.append(lines.attrib)
#             # xml_data.update()
#             print(lines.attrib)
#             xml_data.update(store_itemss)
#         yield xml_data


# data_o = parse_xml(eroot)
# data = list(data_o)
# df = pd.DataFrame(data)
# ------------------------------------------------------------

# %history -f filename.txt