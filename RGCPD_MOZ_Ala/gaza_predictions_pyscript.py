############ IMPORTS HERE ############### remember to change data_path

# import data - HCANGE DIRECTORIES HERE
data_ond = pd.read_csv(os.path.join(data_path, 'OND.X1981_X2020.csv'))
data_ndj = pd.read_csv(os.path.join(data_path, 'NDJ.X1982_X2020.csv'))
data_djf = pd.read_csv(os.path.join(data_path, 'DJF.X1982_X2020.csv'))
data_jfm = pd.read_csv(os.path.join(data_path, 'JFM.X1981_X2020.csv'))

# prepare the data
data_ond.columns = data_ond.columns.str.replace('[X]', '')
data_ndj.columns = data_ndj.columns.str.replace('[X]', '')
data_djf.columns = data_djf.columns.str.replace('[X]', '')
data_jfm.columns = data_jfm.columns.str.replace('[X]', '')

# import pre function from prediction.py script

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

#### gaza
## OND 
# directory of target variable data
TV_path = os.path.join(data_path, 'gaza_ond_aggr.nc')
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

rg_gaza_ond1 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, 
min_area_in_degrees2, tfreq, start_end_year, start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, 
detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data!!!!

### 2 months lead time (ASO)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)

lags = np.array([['08-01', '10-01']])            
periodnames = ['ASO']                                         
start_end_TVdate = ('10-01', '12-01') 

rg_gaza_ond2 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, 
min_area_in_degrees2, tfreq, start_end_year, start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, 
detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 3 months lead time (JAS)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)


lags = np.array([['07-01', '09-01']])            
periodnames = ['JAS']                                         
start_end_TVdate = ('10-01', '12-01')    

rg_gaza_ond3 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 4 months lead time (JJA)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)


lags = np.array([['06-01', '08-01']])            
periodnames = ['JJA']                                         
start_end_TVdate = ('10-01', '12-01')  

rg_gaza_ond4 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)


# pickle the data

### 5 months lead time (MJJ)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)


lags = np.array([['05-01', '07-01']])            
periodnames = ['MJJ']                                         
start_end_TVdate = ('10-01', '12-01') 

rg_gaza_ond5 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 6 months lead time (AMJ)
start_end_year = (1981, 2020)
start_end_TVyear = (1981, 2020)

lags = np.array([['04-01', '06-01']])            
periodnames = ['AMJ']                                         
start_end_TVdate = ('10-01', '12-01')  

rg_gaza_ond6 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

## NDJ
# directory of target variable data
TV_path = os.path.join(data_path, 'gaza_ndj_aggr.nc')

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

rg_gaza_ndj1 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 2 months lead time (SON)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['09-01', '11-01']])            
periodnames = ['SON']                                         
start_end_TVdate = ('01-01', '11-01')  

rg_gaza_ndj2 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 3 months lead time (ASO)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['08-01', '10-01']])            
periodnames = ['ASO']                                         
start_end_TVdate = ('01-01', '11-01')  

rg_gaza_ndj3 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 4 months lead time (JAS)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['07-01', '09-01']])            
periodnames = ['JAS']                                         
start_end_TVdate = ('01-01', '11-01') 

rg_gaza_ndj4 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 5 months lead time (JJA)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['06-01', '08-01']])            
periodnames = ['JJA']                                         
start_end_TVdate = ('01-01', '11-01') 

rg_gaza_ndj5 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 6 months lead time (MJJ)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['05-01', '07-01']])            
periodnames = ['MJJ']                                         
start_end_TVdate = ('01-01', '11-01')    

rg_gaza_ndj6 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

## DJF
# directory of target variable data
TV_path = os.path.join(data_path, 'gaza_djf_aggr.nc')

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

rg_gaza_djf1 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 2 months lead time (OND)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['10-01', '12-01']])            
periodnames = ['OND']                                         
start_end_TVdate = ('02-01', '12-01')   

rg_gaza_djf2 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 3 months lead time (SON)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['09-01', '11-01']])            
periodnames = ['SON']                                         
start_end_TVdate = ('02-01', '12-01')    

rg_gaza_djf3 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 4 month lead time (ASO)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['08-01', '10-01']])            
periodnames = ['ASO']                                         
start_end_TVdate = ('02-01', '12-01') 

rg_gaza_djf4 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 5 month lead time (JAS)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)


lags = np.array([['07-01', '09-01']])            
periodnames = ['JAS']                                         
start_end_TVdate = ('02-01', '12-01')  


rg_gaza_djf5 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 6 month lead time (JJA)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['06-01', '08-01']])            
periodnames = ['JJA']                                         
start_end_TVdate = ('02-01', '12-01')  

rg_gaza_djf6 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### JFM
# directory of target variable data
TV_path = os.path.join(data_path, 'gaza_jfm_aggr.nc')

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

rg_gaza_jfm1 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle data

### 2 months lead time (NDJ)
start_end_year = (1981, 2020)
start_end_TVyear = (1982, 2020)

lags = np.array([['11-01', '01-01']])            
periodnames = ['NDJ']                                         
start_end_TVdate = ('01-01', '03-01')   

rg_gaza_jfm2 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 3 months lead time (OND)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['10-01', '12-01']])            
periodnames = ['OND']                                         
start_end_TVdate = ('01-01', '03-01')  

rg_gaza_jfm3 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 4 months lead time (SON)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['09-01', '11-01']])            
periodnames = ['SON']                                         
start_end_TVdate = ('01-01', '03-01') 

rg_gaza_jfm4 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 5 months lead time (ASO)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['08-01', '10-01']])            
periodnames = ['ASO']                                         
start_end_TVdate = ('01-01', '03-01')   

rg_gaza_jfm5 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)

# pickle the data

### 6 months lead time (JAS)
start_end_year = (1981, 2019)
start_end_TVyear = (1982, 2020)

lags = np.array([['07-01', '09-01']])            
periodnames = ['JAS']                                         
start_end_TVdate = ('01-01', '03-01')    

rg_gaza_jfm6 = pipeline(list_of_name_path, output_path, function, alpha, FDR_control, distance_eps, min_area_in_degrees2, tfreq, start_end_year, 
             start_end_TVyear, TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, periodnames, start_end_TVdate, name)









