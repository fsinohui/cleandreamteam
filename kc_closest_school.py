# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 11:11:16 2018

@author: FSinohui
"""

import pandas as pd
from math import sin, cos, sqrt, atan2, radians

house_data = pd.read_csv("kc_house_data.csv")
school_data =pd.read_excel('kc_schools.xlsx')
print(house_data.head())
print(school_data.head())

def dist_between(lat_1,lon_1,lat_2,lon_2):
    # approximate radius of earth in km
    R = 6373.0
    
    lat1 = radians(lat_1)
    lon1 = radians(lon_1)
    lat2 = radians(lat_2)
    lon2 = radians(lon_2)
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c
    return distance

closest_school_name_list =[]
closest_school_dist_list =[]


for i, rowi in house_data.iterrows():
    lat_house = house_data.get_value(i, 'lat', takeable=False)
    long_house = house_data.get_value(i, 'long', takeable=False) 
    closest_school = 1000
    for j, rowj in school_data.iterrows():
        lat_school = school_data.get_value(j, 'lat', takeable=False)
        long_school = school_data.get_value(j, 'long', takeable=False) 
        
        dist_2_school = dist_between(lat_house,long_house,lat_school,long_school)
        
        if dist_2_school < closest_school:
            closest_school = dist_2_school
            closest_school_name = school_data.get_value(j, 'schools', takeable=False)
    closest_school_name_list.append(closest_school_name)
    closest_school_dist_list.append(closest_school)
    
name_df = pd.Series(closest_school_name_list)
dist_df = pd.Series(closest_school_dist_list)

house_data['closest_school'] = name_df.values
house_data['dist_2_closest'] = dist_df.values


writer = pd.ExcelWriter('kc_house_closest_school.xlsx')
house_data.to_excel(writer,'house_school')
print('done')
