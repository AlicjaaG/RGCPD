############ IMPORTS HERE ############### remember to change data_path
import pandas as pd
import numpy as np
import os, inspect
from RGCPD import RGCPD
from RGCPD import BivariateMI
import class_BivariateMI, functions_pp
from stat_models_cont import ScikitModel
from sklearn.linear_model import Ridge
from sklearn.linear_model import LogisticRegressionCV
from data_preparations import coordinates, data_steps, mean, xarray
import func_models as fc_utils
from pipeline import pipeline

%load_ext autoreload
%autoreload 2

# main directory is the directory of this notebook
main_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 

# my main directory (which contains folders with data etc)
my_main_dir = 'C:\\Users\\alicj\\Desktop\\WORK'
data_path = os.path.join(my_main_dir, 'data')
# import pre function from prediction.py script
data_path = "/scistor/ivm/aga259/RGCPD_masterthesis/data_Ala"
my_main_dir = "/scistor/ivm/aga259/RGCPD_masterthesis"

# define parameters for all experiments
function = class_BivariateMI.corr_map
alpha = 0.01
FDR_control = True 
distance_eps = 500
min_area_in_degrees2 = 5
tfreq = None

TVdates_aggr = False
ext_annual_to_mon = False 
method = 'leave_1'
detrend = True
labels = True
pred_type = 'continuous'
q = 0.66
name = 'rainfall'

#### TETE
## OND 
# directory of target variable data
TV_path = os.path.join(data_path, 'tete_ond_aggr.nc')
# directory of precursor data
prec_path = os.path.join(data_path,'sst_1950-2020_1_12_monthly_1.0deg.nc')
# directory for test data 
path_test = os.path.join(my_main_dir, 'test')
# directory for output
output_path = os.path.join(my_main_dir, 'out')
list_of_name_path = [(1, TV_path), ('sst', prec_path)]

### 1 month lead time (SON)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)

lags = np.array([['09-01', '11-01']])            
periodnames = ['SON']                                         
start_end_TVdate = ('10-01', '12-01')   

rg_tete_ond1 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, 
min_area_in_degrees2, tfreq, start_end_year, start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, 
detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data!!!!

### 2 months lead time (ASO)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)

lags = np.array([['08-01', '10-01']])            
periodnames = ['ASO']                                         
start_end_TVdate = ('10-01', '12-01') 

rg_tete_ond2 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, 
min_area_in_degrees2, tfreq, start_end_year, start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, 
detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 3 months lead time (JAS)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)


lags = np.array([['07-01', '09-01']])            
periodnames = ['JAS']                                         
start_end_TVdate = ('10-01', '12-01')    

rg_tete_ond3 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 4 months lead time (JJA)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)


lags = np.array([['06-01', '08-01']])            
periodnames = ['JJA']                                         
start_end_TVdate = ('10-01', '12-01')  

rg_tete_ond4 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)


# pickle the data

### 5 months lead time (MJJ)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)


lags = np.array([['05-01', '07-01']])            
periodnames = ['MJJ']                                         
start_end_TVdate = ('10-01', '12-01') 

rg_tete_ond5 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 6 months lead time (AMJ)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)

lags = np.array([['04-01', '06-01']])            
periodnames = ['AMJ']                                         
start_end_TVdate = ('10-01', '12-01')  

rg_tete_ond6 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

## NDJ
# directory of target variable data
TV_path = os.path.join(data_path, 'tete_ndj_aggr.nc')

# directory of precursor data
prec_path = os.path.join(data_path,'sst_1950-2020_1_12_monthly_1.0deg.nc')

# directory for test data 
path_test = os.path.join(my_main_dir, 'test')

# directory for output
output_path = os.path.join(my_main_dir, 'out')
list_of_name_path = [(1, TV_path), ('sst', prec_path)]

### 1 month lead time (OND)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['10-01', '12-01']])            
periodnames = ['OND']                                         
start_end_TVdate = ('01-01', '11-01')  

rg_tete_ndj1 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 2 months lead time (SON)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['09-01', '11-01']])            
periodnames = ['SON']                                         
start_end_TVdate = ('01-01', '11-01')  

rg_tete_ndj2 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 3 months lead time (ASO)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['08-01', '10-01']])            
periodnames = ['ASO']                                         
start_end_TVdate = ('01-01', '11-01')  

rg_tete_ndj3 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 4 months lead time (JAS)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['07-01', '09-01']])            
periodnames = ['JAS']                                         
start_end_TVdate = ('01-01', '11-01') 

rg_tete_ndj4 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 5 months lead time (JJA)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['06-01', '08-01']])            
periodnames = ['JJA']                                         
start_end_TVdate = ('01-01', '11-01') 

rg_tete_ndj5 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 6 months lead time (MJJ)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['05-01', '07-01']])            
periodnames = ['MJJ']                                         
start_end_TVdate = ('01-01', '11-01')    

rg_tete_ndj6 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

## DJF
# directory of target variable data
TV_path = os.path.join(data_path, 'tete_djf_aggr.nc')

# directory of precursor data
prec_path = os.path.join(data_path,'sst_1950-2020_1_12_monthly_1.0deg.nc')

# directory for test data 
path_test = os.path.join(my_main_dir, 'test')

# directory for output
output_path = os.path.join(my_main_dir, 'out')
list_of_name_path = [(1, TV_path), ('sst', prec_path)]

# 1 month lead time (NDJ)
start_end_year = (1981, 2020)
start_end_TVyear = (1982, 2020)

lags = np.array([['11-01', '01-01']])            
periodnames = ['NDJ']                                         
start_end_TVdate = ('02-01', '12-01') 

rg_tete_djf1 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 2 months lead time (OND)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['10-01', '12-01']])            
periodnames = ['OND']                                         
start_end_TVdate = ('02-01', '12-01')   

rg_tete_djf2 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 3 months lead time (SON)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['09-01', '11-01']])            
periodnames = ['SON']                                         
start_end_TVdate = ('02-01', '12-01')    

rg_tete_djf3 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 4 month lead time (ASO)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['08-01', '10-01']])            
periodnames = ['ASO']                                         
start_end_TVdate = ('02-01', '12-01') 

rg_tete_djf4 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 5 month lead time (JAS)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)


lags = np.array([['07-01', '09-01']])            
periodnames = ['JAS']                                         
start_end_TVdate = ('02-01', '12-01')  


rg_tete_djf5 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 6 month lead time (JJA)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['06-01', '08-01']])            
periodnames = ['JJA']                                         
start_end_TVdate = ('02-01', '12-01')  

rg_tete_djf6 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### JFM
# directory of target variable data
TV_path = os.path.join(data_path, 'tete_jfm_aggr.nc')

# directory of precursor data
prec_path = os.path.join(data_path,'sst_1950-2020_1_12_monthly_1.0deg.nc')

# directory for test data 
path_test = os.path.join(my_main_dir, 'test')

# directory for output
output_path = os.path.join(my_main_dir, 'out')
list_of_name_path = [(1, TV_path), ('sst', prec_path)]

### 1 month lead time (DJF)
start_end_year = (1981, 2020)
start_end_TVyear = (1982, 2020)

lags = np.array([['12-01', '02-01']])            
periodnames = ['DJF']                                         
start_end_TVdate = ('01-01', '03-01')    

rg_tete_jfm1 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle data

### 2 months lead time (NDJ)
start_end_year = (1981, 2020)
start_end_TVyear = (1982, 2020)

lags = np.array([['11-01', '01-01']])            
periodnames = ['NDJ']                                         
start_end_TVdate = ('01-01', '03-01')   

rg_tete_jfm2 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 3 months lead time (OND)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['10-01', '12-01']])            
periodnames = ['OND']                                         
start_end_TVdate = ('01-01', '03-01')  

rg_tete_jfm3 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 4 months lead time (SON)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['09-01', '11-01']])            
periodnames = ['SON']                                         
start_end_TVdate = ('01-01', '03-01') 

rg_tete_jfm4 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 5 months lead time (ASO)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['08-01', '10-01']])            
periodnames = ['ASO']                                         
start_end_TVdate = ('01-01', '03-01')   

rg_tete_jfm5 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 6 months lead time (JAS)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['07-01', '09-01']])            
periodnames = ['JAS']                                         
start_end_TVdate = ('01-01', '03-01')    

rg_tete_jfm6 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)









 