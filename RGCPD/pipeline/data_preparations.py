#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd

def coordinates(data, lon, lat):
    lon_min = lon[0]
    lon_max = lon[1]
    lat_min = lat[0]
    lat_max = lat[1]
    
    # latitude
    data1 = data[data.iloc[:,1] <= lat_max][data[data.iloc[:,1] <= lat_max].iloc[:,1] >= lat_min]
    
    # longitude
    data2 = data1[data1.iloc[:,0] <= lon_max][data1[data1.iloc[:,0] <= lon_max].iloc[:,0] >= lon_min]
    
    return data2

# data_coor is dataframe for selected coordinates, target is a string with target variable name, e.g. 'rainfall'
def data_steps(data_coor, target):
    data_coor_mean = mean(data_coor)
    data_coor_mean = data_coor_mean[2:]
    data_coor_mean = data_coor_mean.reset_index()
    data_coor_mean['index'] = pd.to_datetime(data_coor_mean['index'])
    data_coor_mean = data_coor_mean.set_index('index')
    data_coor_mean.columns = [target]
    return data_coor_mean    

def mean(data):
    mean_data = data.mean(axis=0)
    return mean_data

def xarray(data):
    xr_data = data.to_xarray()
    xr_data = xr_data.rename({'index':'time'})
    #xr_data.expand_dims('cluster')
    #xr_data = xr_data.expand_dims('cluster')
    #xr_data['cluster'] = ('cluster', [1])
    return xr_data

def month(data, month):
    return data[data.index.month.isin(month)]    

def data_prep(data, lon, lat, target, m = None):
    data = coordinates(data, lon, lat)
    data = mean(data)[2:].reset_index()
    data['index'] = pd.to_datetime(data['index'])
    
    data = data.set_index('index')
    data.columns = [target]
    
    
    if m is not None:
        data = month(data, m)
    
    data.index.name = None
    
    return data


# %%
