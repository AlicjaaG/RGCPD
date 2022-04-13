#!/usr/bin/env python
# coding: utf-8

# In[ ]:
from RGCPD import RGCPD
from RGCPD import BivariateMI
import class_BivariateMI, functions_pp

def pipeline(list_of_name_path, output_path, function, alpha, FDR_control, 
            distance_eps, min_area_in_degrees2, tfreq, start_end_year, start_end_TVyear, 
            TVdates_aggr, ext_annual_to_mon, method, detrend, labels, pred_type, q, lags, 
            periodnames, start_end_TVdate, name):
    
    
    
    # initialize BMI class
    list_for_MI = [BivariateMI(name='sst', func=function, 
                           alpha=alpha, FDR_control=FDR_control, 
                           lags=lags, 
                           distance_eps=distance_eps, min_area_in_degrees2=min_area_in_degrees2)]
    
    # initialize RGCPD class
    rg = RGCPD(list_of_name_path=list_of_name_path,
           list_for_MI=list_for_MI,
           tfreq=tfreq, 
           start_end_TVdate=start_end_TVdate, 
           start_end_year = start_end_year,
           path_outmain=output_path)

    # adding lags and target period information
    rg.lags = lags
    rg.periodnames = periodnames
    rg.start_end_TVdate = start_end_TVdate
    
    # preprocessing target variable 
    rg.pp_TV(name, kwrgs_core_pp_time = {'start_end_year':start_end_TVyear}, 
             TVdates_aggr=TVdates_aggr, ext_annual_to_mon = ext_annual_to_mon, detrend = detrend)
    #rg.pp_TV()
    
    # preprocessing precursors
    rg.pp_precursors()
    
    # train-test split
    rg.traintest(method)
    
    # calculating correlation maps
    rg.calc_corr_maps()
    
    # clustering regions together
    rg.cluster_list_MI()
    
    # rename lags
    if periodnames != None:    
        sst = rg.list_for_MI[0]
        sst.prec_labels['lag'] = ('lag', periodnames)
        sst.corr_xr['lag'] = ('lag', periodnames)

    # plotting correlation maps
    rg.plot_maps_corr()
    
    # plotting significant regions
    rg.quick_view_labels()
    
    # getting MI timeseries
    rg.get_ts_prec()
    
    # to be able to access RGCPD class object
    return rg 

