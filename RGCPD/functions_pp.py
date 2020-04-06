#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 17:48:31 2018

@author: semvijverberg
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import itertools
import core_pp
import datetime


from dateutil.relativedelta import relativedelta as date_dt
flatten = lambda l: list(set([item for sublist in l for item in sublist]))
flatten = lambda l: list(itertools.chain.from_iterable(l))

def get_oneyr(pddatetime, *args):
    dates = []
    pddatetime = pd.to_datetime(pddatetime)
    year = pddatetime.year[0]

    for arg in args:
        year = arg
        dates.append(pddatetime.where(pddatetime.year==year).dropna())
    dates = pd.to_datetime(flatten(dates))
    if len(dates) == 0:
        dates = pddatetime.where(pddatetime.year==year).dropna()
    return dates


def perform_post_processing(list_of_name_path, kwrgs_pp=None, verbosity=1):
    ''' 
    if argument of kwrgs_pp is list, then the first item is assumed to be the
    default argument value, the second item should be a dict contaning the 
    {varname : exception_argument}.
    '''
    
    list_precur_pp = []
    for idx, (name, filename) in enumerate(list_of_name_path[1:]):
        
        outfile = check_pp_done(name, filename)
        list_precur_pp.append( (name, outfile) )
        if os.path.isfile(outfile) == True:
            if verbosity == 1:
                print('Loaded post-processed data of {}\n'.format(name))
            pass
        else:
            print('\nPerforming the post-processing {}'.format(name))
            kwrgs = {}
            for key, value in kwrgs_pp.items():
                if type(value) is list and name in value[1].keys():
                    kwrgs[key] = value[1][name]
                elif type(value) is list and name not in value[1].keys():
                    kwrgs[key] = value[0] # plugging in default value
                else:
                    kwrgs[key] = value
            
            core_pp.detrend_anom_ncdf3D(filename, outfile, **kwrgs)
    return list_precur_pp
        # update the dates stored in var_class:
#        var_class, ex = update_dates(var_class, ex)
        # store updates
#        ex[var] = var_class


def check_pp_done(name, filename, verbosity=1):
    #%%
    '''
    Check if pre processed ncdf already exists
    '''
    # =============================================================================
    # load dataset lazy
    # =============================================================================
#    filename = os.path.join(ex['path_raw'], cls.filename)
    kwrgs_pp = {'loadleap':False, 'format_lon':None}
    ds = core_pp.import_ds_lazy(filename, **kwrgs_pp)
    dates = pd.to_datetime(ds['time'].values)
    start_day = get_oneyr(dates)[0]
    end_day   = get_oneyr(dates)[-1]

    # =============================================================================
    # give appropriate name to output file
    # =============================================================================
    outfilename = filename.split('/')[-1];
#    outfilename = outfilename.replace('daily', 'dt-{}days'.format(1))
    months = dict( {1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',
                         8:'aug',9:'sep',10:'okt',11:'nov',12:'dec' } )
                
    input_freq = (dates[1] - dates[0]).days
    if input_freq == 1: # daily data
        startdatestr = '_{}{}_'.format(start_day.day, months[start_day.month])
        enddatestr   = '_{}{}_'.format(end_day.day, months[end_day.month])
    elif input_freq > 27 and input_freq < 32: # monthly data
        startdatestr = '_{}_'.format(months[start_day.month])
        enddatestr   = '_{}_'.format(months[end_day.month])

    outfilename = outfilename.replace('_{}_'.format(1), startdatestr)
    outfilename = outfilename.replace('_{}_'.format(12), enddatestr)
#    filename_pp = outfilename
    path_raw = '/'.join(filename.split('/')[:-1])
    path_pp = os.path.join(path_raw, 'preprocessed')
    if os.path.isdir(path_pp) == False: os.makedirs(path_pp)
    outfile = os.path.join(path_pp, outfilename)
#    dates_fit_tfreq = dates
    #%%
    return outfile


def kornshell_with_input(args, cls):
#    stopped working for cdo commands
    '''some kornshell with input '''
#    args = [anom]
    import os
    import subprocess
    cwd = os.getcwd()
    # Writing the bash script:
    new_bash_script = os.path.join(cwd,'bash_scripts', "bash_script.sh")
#    arg_5d_mean = 'cdo timselmean,5 {} {}'.format(infile, outfile)
    #arg1 = 'ncea -d latitude,59.0,84.0 -d longitude,-95,-10 {} {}'.format(infile, outfile)

    bash_and_args = [new_bash_script]
    [bash_and_args.append(arg) for arg in args]
    with open(new_bash_script, "w") as file:
        file.write("#!/bin/sh\n")
        file.write("echo bash script output\n")
        for cmd in range(len(args)):

            print(args[cmd].replace(cls.base_path, 'base_path/')[:300])
            file.write("${}\n".format(cmd+1))
    p = subprocess.Popen(bash_and_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    out = p.communicate()
    print(out[0].decode())
    return

def update_dates(cls, ex):
    import os
    file_path = os.path.join(cls.path_pp, cls.filename_pp)
    kwrgs_pp = {'selbox':ex['selbox'],
                'loadleap':False }
    ds = core_pp.import_ds_lazy(file_path, **kwrgs_pp)

    temporal_freq = pd.Timedelta((ds['time'][1] - ds['time'][0]).values)
    cls.dates = pd.to_datetime(ds['time'].values)
    cls.temporal_freq = '{}days'.format(temporal_freq.days)
    return cls, ex

def load_TV(list_of_name_path, loadleap=False, name_ds='ts'):
    '''
    function will load first item of list_of_name_path
    list_of_name_path = [('TVname', 'TVpath'), ('prec_name', 'prec_path')]
    
    if TVpath refers to .npy file: 
        it tries to import the variable {TVname}
    if TVpath refers to .nc file:
        it tries to import the timeseries of cluster {TVname}.
    
    
    returns:
    fulltso : full timeseries original
    '''
    name = list_of_name_path[0][0]
    filename = list_of_name_path[0][1]
    
    if filename.split('.')[-1] == 'npy':
        fulltso = load_npy(filename, name=name)
    elif filename.split('.')[-1] == 'nc':
        ds = core_pp.import_ds_lazy(filename)
        fulltso = ds[name_ds].sel(cluster=name)
    hashh = filename.split('_')[-1].split('.')[0]
    fulltso.name = str(list_of_name_path[0][0])
    if loadleap == False:
        dates = core_pp.remove_leapdays(pd.to_datetime(fulltso.time.values))
        fulltso = fulltso.sel(time=dates)
    return fulltso, hashh


def nc_xr_ts_to_df(filename, name_ds='ts'):
    if filename.split('.')[-1] == 'nc':
        ds = core_pp.import_ds_lazy(filename)
    else:
        print('not a NetCDF file')
    return xrts_to_df(ds[name_ds]), ds

def xrts_to_df(xarray):
    dims = list(xarray.coords.keys())
    standard_dim = ['latitude', 'longitude', 'time', 'mask', 'cluster']
    dims = [d for d in dims if d not in standard_dim]
    if 'n_clusters' in dims:
        dims[0] = 'ncl'
        xarray = xarray.rename({'n_clusters':dims[0]}).copy()
    var1 = int(xarray[dims[0]])
    var2 = int(xarray[dims[1]])
    dim1 = dims[0]
    dim2 = dims[1]       
    name = '{}{}_{}{}'.format(dim1, var1, dim2, var2)
    df = xarray.drop(dim1).drop(dim2).T.to_dataframe(
                                        name=name).unstack(level=1)
    df = df.droplevel(0, axis=1)
    df.index.name = name
    return df

def process_TV(fullts, tfreq, start_end_TVdate, start_end_date=None,
               start_end_year=None, RV_detrend=True, RV_anomaly=False,
               verbosity=1):
    #%%
    name = fullts.name
    dates = pd.to_datetime(fullts.time.values)
    startyear = dates.year[0]
    endyear = dates.year[-1]
    n_timesteps = dates.size
    n_yrs       = (endyear - startyear) + 1

#    if start_end_date is None:
#        start_end_date = ('01-01', '12-31')

    timestep = (dates[1] - dates[0])
    if timestep == pd.Timedelta('1d'):
        input_freq = 'daily'
        same_freq = (dates[1] - dates[0]).days == tfreq
    elif timestep.days >= 28 and timestep.days <= 31 and n_yrs != n_timesteps:
        input_freq = 'monthly'
        same_freq = (dates[1].month - dates[0].month) == tfreq
    else:
        same_freq = True


    if same_freq == False:
        if verbosity == 1:
            print('original tfreq of imported response variable is converted to '
                  'desired tfreq')
        to_freq = tfreq

        fullts, dates_tobin = time_mean_bins(fullts, to_freq,
                                                start_end_date,
                                                start_end_year)
        

    if same_freq == True and start_end_date is not None:
        to_freq = tfreq
        fullts, dates = timeseries_tofit_bins(fullts, to_freq, start_end_date,
                                       start_end_year)
        print('Selecting subset as defined by start_end_date')

    if RV_detrend == True:
        print('Detrending Respone Variable.')
        fullts = detrend1D(fullts, anomaly=RV_anomaly)
    
    if input_freq == 'daily':
        dates_RV = core_pp.get_subdates(pd.to_datetime(fullts.time.values), start_end_TVdate,
                                  start_end_year)
    elif input_freq == 'monthly':
        dates_RV = TVmonthrange(fullts, start_end_TVdate)

    # get indices of RVdates
    string_RV = list(dates_RV.strftime('%Y-%m-%d'))
    string_full = list(pd.to_datetime(fullts.time.values).strftime('%Y-%m-%d'))
    RV_period = [string_full.index(date) for date in string_full if date in string_RV]
    
    fullts.name = name
    TV_ts = fullts[RV_period] # extract specific months of MT index
    
    return fullts, TV_ts, input_freq

def load_npy(filename, name=None):
    '''
    expects dictionary with 1D xarray timeseries
    '''
    dicRV = np.load(filename, encoding='latin1', 
                    allow_pickle=True).item()
    logical = ['RVfullts', 'RVfullts95']
    if name is not None:
        logical.insert(0, name)
    for name_ in logical:
        try:
            fullts = dicRV[name_]
        except:
            pass
    return fullts

def import_ds_timemeanbins(filepath, tfreq=1, start_end_date=None, 
                           start_end_year=None,
                           selbox=None,
                           loadleap=False, 
                           to_xarr=True,
                           seldates=None,
                           format_lon='only_east'):

    ds = core_pp.import_ds_lazy(filepath, loadleap=loadleap, 
                                seldates=seldates, selbox=selbox, 
                                format_lon=format_lon)
    
    to_freq = tfreq
    if to_freq != 1:
        ds, dates_tobin = time_mean_bins(ds, to_freq,
                                        start_end_date,
                                        start_end_year)
#    print('temporal frequency \'dt\' is: \n{}'.format(dates[1]- dates[0]))
    if to_xarr:
        if type(ds) == type(xr.DataArray(data=[0])):
            ds = ds.squeeze()
        else:
            ds = ds.to_array().squeeze()
    # check if no axis has length 0:
    assert 0 not in ds.shape, ('loaded ds has a dimension of length 0'
                               f', shape {ds.shape}')
    return ds



def csv_to_npy(ex):
   #%%
   import os
   import pandas as pd
   import xarray as xr
   import numpy as np
   # load data from csv file and save to .npy as xarray format

   path = os.path.join(ex['path_pp'], 'RVts2.5', ex['RVts_filename'])
   table = pd.read_csv(path)
   data  = np.array(table)
   dates = pd.to_datetime(['{}-{}-{}'.format(A[0],A[1],A[2]) for A in data])

   y_val = data[:,-1]  # ATTENTION: This only works if values are in last column

   xrdata = xr.DataArray(data=y_val, coords=[dates], dims=['time'])

   ofile = ex['RVts_filename'].split('.')[0] + '.npy'
   to_dict = dict( {'RVfullts'     : xrdata } )
   np.save(os.path.join(ex['path_pp'], 'RVts2.5', ofile), to_dict)
   ex['RVts_filename'] = ofile

   #%%
   return ex


def time_mean_bins(xr_or_df, to_freq=int, start_end_date=None, start_end_year=None, 
                   verbosity=0):
   #%%

    types = [type(xr.Dataset()), type(xr.DataArray([0])), type(pd.DataFrame([0]))]

    assert (type(xr_or_df) in types), ('{} given, should be in {}'.format(type(xr_or_df), types) )

    if type(xr_or_df) == types[-1]:
        return_df = True
        xr_init = xr_or_df.to_xarray().to_array()
        if len(xr_init.shape) > 2:
            dims = xr_init.dims.items()
            i_time = np.argmax([ z[1] for z in dims])
            old_name = [ z[0] for z in dims][i_time]
        else:
            old_name = 'index'
        xarray = xr_init.rename({old_name : 'time'})
    else:
        return_df = False
        xarray = xr_or_df

    datetime = pd.to_datetime(xarray['time'].values)
    # ensure to remove leapdays
    datetime = core_pp.remove_leapdays(datetime)
    xarray = xarray.sel(time=datetime)
    one_yr = datetime.where(datetime.year == datetime.year[0]).dropna(how='any')

    if one_yr.size % to_freq != 0:
        possible = []
        for i in np.arange(1,20):
            if one_yr.size%i == 0:
                possible.append(i)
        if verbosity == 1:
            print('Note: stepsize {} does not fit in one year\n '
                            ' supply an integer that fits {}'.format(
                                to_freq, one_yr.size))
            print('\n Stepsize that do fit are {}'.format(possible))
            print('\n Will shorten the \'subyear\', so that the temporal'
                 ' frequency fits in one year')
        datetime = pd.to_datetime(np.array(xarray['time'].values,
                                          dtype='datetime64[D]'))
        
        
        dates_tobin = timeseries_tofit_bins(datetime, to_freq, 
                                                     start_end_date=start_end_date, 
                                                     start_end_year=start_end_year, 
                                                     verbosity=verbosity)
        dates_notpresent = [d for d in dates_tobin if d not in datetime]
        assert len(dates_notpresent)==0, f'dates not present in xr_or_df\n{dates_notpresent}'
        xarray = xarray.sel(time=dates_tobin)
        one_yr = dates_tobin.where(dates_tobin.year == dates_tobin.year[0]).dropna(how='any')

    else:
        dates_tobin = datetime

    fit_steps_yr = (one_yr.size )  / to_freq
    bins = list(np.repeat(np.arange(0, fit_steps_yr), to_freq))
    n_years = np.unique(dates_tobin.year).size
    for y in np.arange(1, n_years):
        x = np.repeat(np.arange(0, fit_steps_yr), to_freq)
        x = x + fit_steps_yr * y
        [bins.append(i) for i in x]
    label_bins = xr.DataArray(bins, [xarray.coords['time'][:]], name='time')
    label_dates = xr.DataArray(xarray.time.values, [xarray.coords['time'][:]], name='time')
    xarray['bins'] = label_bins
    xarray['time_dates'] = label_dates
    xarray = xarray.set_index(time=['bins','time_dates'])

    half_step = to_freq/2.
    newidx = np.arange(half_step, dates_tobin.size, to_freq, dtype=int)
    newdate = label_dates[newidx]

    # suppres warning for nans in field
    import warnings
    warnings.simplefilter("ignore", category=RuntimeWarning)
    group_bins = xarray.groupby('bins', restore_coord_dims=True).mean(dim='time', 
                               skipna=True,
                               keep_attrs=True)
    
    
    group_bins['bins'] = newdate.values
    xarray = group_bins.rename({'bins' : 'time'})
    dates = pd.to_datetime(newdate.values)

    if return_df:
        if len(xr_init.shape) == 3:
            iterables = [xarray.level_0.values, dates]
            index = pd.MultiIndex.from_product(iterables,
                                              names=['split', 'time'])
            xr_index = xarray.stack(index=['level_0', 'time'])
            return_obj = pd.DataFrame(xr_index.values.T,
                                      index=index,
                                      columns=list(xr_init.coords['variable'].values))
        elif len(xr_init.shape) == 2:
            return_obj = pd.DataFrame(xarray.values.T,
                                      index=dates,
                                      columns=list(xr_init.coords['variable'].values))
            return_obj = return_obj.astype(xr_or_df.dtypes)
    elif return_df == False:
        return_obj = xarray
   #%%
    return return_obj, dates_tobin


def timeseries_tofit_bins(xr_or_dt, to_freq, start_end_date=None, start_end_year=None, 
                          verbosity=0):
    #%%
    '''
    if to_freq is an even number, the centered date will be 
    1 day to the right of the window. 
    '''
    if type(xr_or_dt) == type(xr.DataArray([0])):
        datetime = pd.to_datetime(xr_or_dt['time'].values)
    else:
        datetime = xr_or_dt.copy()

    datetime = core_pp.remove_leapdays(datetime)
    input_freq = datetime.resolution
# =============================================================================
#   # select dates
# =============================================================================
    if start_end_date is None:
        seldays = 'all'
        d_s = datetime[0]
        d_e = datetime[-1]
        sstartdate = '{}-{}'.format(d_s.month, d_s.day)
        senddate   = '{}-{}'.format(d_e.month, d_e.day)
        one_yr = datetime.where(datetime.year == datetime.year[0]).dropna(how='any')
        sdate = one_yr[0]
        seldays_pp = pd.date_range(start=one_yr[0], end=one_yr[-1],
                                freq=datetime[1] - datetime[0])
    else:
        seldays = 'part'
        sstartdate, senddate = start_end_date
    
    if start_end_year is None:
        startyear, endyear = datetime[0].year, datetime[-1].year
        years = np.unique(datetime.year)
        assert (np.unique(datetime.year).size == len(years)), \
            (f'Range of years ({len(years)}) requested not in dataset,',
            f'only {np.unique(datetime.year).size} years present.')
    else:
        startyear, endyear = start_end_year
        years = range(startyear, endyear+1)
    
    
    
    # selday_pp is the period you aim to study
    if seldays == 'part':
        # add corresponding time information
        crossyr = int(sstartdate.replace('-','')) > int(senddate.replace('-',''))
        sstartdate = '{}-{}'.format(startyear, sstartdate)
        if crossyr:
            senddate   = '{}-{}'.format(startyear+1, senddate)
        else:
            senddate   = '{}-{}'.format(startyear, senddate)

        adjhrsstartdate = sstartdate + ' {:}:00:00'.format(datetime[0].hour)
        adjhrsenddate   = senddate + ' {:}:00:00'.format(datetime[0].hour)
        sdate = pd.to_datetime(adjhrsstartdate)
        seldays_pp = pd.date_range(start=adjhrsstartdate, end=adjhrsenddate,
                                freq=pd.Timedelta(datetime[1] - datetime[0]))

    seldays_pp = core_pp.remove_leapdays(seldays_pp)

    if input_freq == 'day' and to_freq != 1:
        dt = np.timedelta64(to_freq, 'D')
        end_day = seldays_pp.max()
        start_day = seldays_pp.min()
        # after time averaging over 'tfreq' number of days, you want that each year
        # consists of the same day. For this to be true, you need to make sure that
        # the selday_pp period exactly fits in a integer multiple of 'tfreq'
        fit_steps_yr = (end_day - start_day + np.timedelta64(1, 'D'))  / dt
        # line below: The +1 = include day 1 in counting
        start_day = (end_day - (dt * np.round(fit_steps_yr, decimals=0))) \
                    + np.timedelta64(1, 'D')
                    
        if start_day.month==1 and start_day.day==1 and start_day.is_leap_year:
            # if leap year, start_day is adjusted one day backward in time,
            # however, if start_day is already first of januari, this can't be done
            # thus removing one step_yr
            start_day = (end_day - (dt * np.round(fit_steps_yr-1, decimals=0))) \
                    + np.timedelta64(1, 'D')
        
        # account for leap_year #1
        if start_day.is_leap_year and start_day.month <= 2 :
            # add day in front to compensate for removing a leap day
            start_day = start_day - np.timedelta64(1, 'D')                    

        if start_day.dayofyear < sdate.dayofyear or start_day.year < sdate.year:
            # if startday is before the desired starting period then 
            # startday dayofyear < dayofyear of first data available )
            # skip one bin forward in time
            start_day = (end_day - (dt * np.round(fit_steps_yr-1, decimals=0))) \
                    + np.timedelta64(1, 'D')
            # after this if statement, the 'account for leap_year' may again 
            # be an issue.
        
            # account for leap_year #2
            if start_day.is_leap_year and start_day.month <= 2 :
                # add day in front to compensate for removing a leap day
                start_day = start_day - np.timedelta64(1, 'D')
            


        start_yr = pd.date_range(start=start_day, end=end_day,
                                    freq=(datetime[1] - datetime[0]))

        start_yr = core_pp.remove_leapdays(start_yr)
        
        
    if input_freq == 'day' and to_freq == 1:
        end_day = seldays_pp.max()
        start_day = seldays_pp.min()
        start_yr = seldays_pp

    if input_freq == 'month':
        dt = date_dt(months=to_freq)
        start_day = adjhrsstartdate.split(' ')[0]
        start_day = pd.to_datetime(start_day.replace(start_day[-2:], '01'))
        end_day = adjhrsenddate.split(' ')[0]
        end_day = pd.to_datetime(end_day.replace(end_day[-2:], '01'))
        fit_steps_yr = (end_day.month - start_day.month + 1) / to_freq
        start_day = (end_day - (dt * int(fit_steps_yr))) \
                + date_dt(months=+1)
        days_back = end_day
        start_yr = [end_day.strftime('%Y-%m-%d %H:%M:%S')]
        while start_day < days_back:
            days_back -= date_dt(months=+1)
            start_yr.append(days_back.strftime('%Y-%m-%d %H:%M:%S'))
        start_yr.reverse()
        start_yr = pd.to_datetime(start_yr)


#    n_oneyr = start_yr.size
#    end_year = endyear
    datesdt = make_dates(start_yr, years)

#    n_yrs = datesdt.size / n_oneyr
    if verbosity==1:
        months = dict( {1:'jan',2:'feb',3:'mar',4:'apr',5:'may',6:'jun',7:'jul',
                             8:'aug',9:'sep',10:'okt',11:'nov',12:'dec' } )
        startdatestr = '{} {}'.format(start_day.day, months[start_day.month])
        enddatestr   = '{} {}'.format(end_day.day, months[end_day.month])
        if input_freq == 'day':
            print('Period of year selected: \n{} to {}, tfreq {} days'.format(
                    startdatestr, enddatestr, to_freq))
        if input_freq == 'month':
            print('Months of year selected: \n{} to {}, tfreq {} months'.format(
                    startdatestr.split(' ')[-1], enddatestr.split(' ')[-1], to_freq))

    if type(xr_or_dt) == type(xr.DataArray([0])):
        adj_xarray = xr_or_dt.sel(time=datesdt)
        out = (adj_xarray, datesdt)
    else:
        out = (datesdt)
    #%%
    return out


#def make_dates(datetime, start_yr, endyear):
#    '''
#    Extend same date period to other years
#    datetime is full datetime
#    start_yr are date period to 'copy'
#    '''
#    breakyr = endyear
#    nyears = (datetime.year[-1] - datetime.year[0])+1
#    next_yr = start_yr
#    for yr in range(0,nyears-1):
#        next_yr = pd.to_datetime([date + date_dt(years=1) for date in next_yr])
#        start_yr = start_yr.append(next_yr)
#        if next_yr[-1].year == breakyr:
#            break
#    return start_yr

def make_dates(datetime, years):
    '''
    Extend same date period to other years
    datetime is start year
    start_yr is date period to 'copy'
    '''

    start_yr = datetime
    next_yr = start_yr
    for yr in years:
        delta_year = yr - start_yr[-1].year
        if delta_year != 0:
            next_yr = pd.to_datetime([date + date_dt(years=delta_year) for date in next_yr])
            start_yr = start_yr.append(next_yr)

    return start_yr



def TVmonthrange(fullts, start_end_TVdate):
    '''
    fullts : 1-D xarray timeseries
    start_end_TVdate is tuple of start- and enddate in format ('mm-dd', 'mm-dd')
    '''
    want_month = np.arange(int(start_end_TVdate[0].split('-')[0]),
                       int(start_end_TVdate[1].split('-')[0])+1)
    months = fullts.time.dt.month
    months_pres = np.unique(months)
    selmon = [m for m in want_month if m in list(months_pres)]
    if len(selmon) == 0:
        print('The RV months are no longer in the time series, perhaps due to '
              'time mean bins, in which time axis is changed, i.e. new time axis'
              'takes the center month of the bin')
        new_want_m = []
        for want_m in want_month:
            idx_close = max(months_pres)
            diff = []
            for m in months_pres:
                diff.append(abs(m - want_m))
                # choosing month present closest to desired month in ex['startperiod']
                min_diff = min(diff[-1], idx_close)
            new_want_m.append(months_pres[diff.index(min_diff)])
        selmon = [m for m in new_want_m if m in list(months_pres)]
    mask = np.zeros(months.size, dtype=bool)
    idx = [i for i in range(months.size) if months[i] in selmon]
    mask[idx] = True
    xrdates = fullts.time.where(mask).dropna(dim='time')
    dates_RV = pd.to_datetime(xrdates.values)
    return dates_RV

#def make_TVdatestr(dates, ex):
#
#    startyr = dates[0].year
#    sstartdate = pd.to_datetime(str(startyr) + '-' + ex['startperiod'])
#    senddate   = pd.to_datetime(str(startyr) + '-' + ex['endperiod'])
#    first_d = sstartdate.dayofyear
#    last_d  = senddate.dayofyear
#    datesRV = pd.to_datetime([d for d in dates if d.dayofyear >= first_d and d.dayofyear <= last_d])
#    return datesRV


def area_weighted(xarray):
   # Area weighted, taking cos of latitude in radians
   coslat = np.cos(np.deg2rad(xarray.coords['latitude'].values)).clip(0., 1.)
   area_weights = np.tile(coslat[..., np.newaxis],(1,xarray.longitude.size))
#   area_weights = area_weights / area_weights.mean()
   return xr.DataArray(xarray.values * area_weights, coords=xarray.coords,
                          dims=xarray.dims)

def xarray_plot(data, path='default', name = 'default', saving=False):
    # from plotting import save_figure
    import matplotlib.pyplot as plt
    import cartopy.crs as ccrs
    import numpy as np
    plt.figure()
    data = data.squeeze()
    if len(data.longitude[np.where(data.longitude > 180)[0]]) != 0:
        data = convert_longitude(data)
    else:
        pass
    if data.ndim != 2:
        print("number of dimension is {}, printing first element of first dimension".format(np.squeeze(data).ndim))
        data = data[0]
    else:
        pass
    if 'mask' in list(data.coords.keys()):
        cen_lon = data.where(data.mask==True, drop=True).longitude.mean()
        data = data.where(data.mask==True, drop=True)
    else:
        cen_lon = data.longitude.mean().values
    proj = ccrs.LambertCylindrical(central_longitude=cen_lon)
#    proj = ccrs.Orthographic(central_longitude=cen_lon, central_latitude=data.latitude.mean())
    ax = plt.axes(projection=proj)
    ax.coastlines()
    # ax.set_global()
    if 'mask' in list(data.coords.keys()):
        plot = data.where(data.mask==True).plot.pcolormesh(ax=ax, cmap=plt.cm.RdBu_r,
                             transform=ccrs.PlateCarree(), add_colorbar=True)
    else:
        plot = data.plot.pcolormesh(ax=ax, cmap=plt.cm.RdBu_r,
                             transform=ccrs.PlateCarree(), add_colorbar=True)
    if saving == True:
        save_figure(data, path=path)
    plt.show()


def find_region(data, region='EU'):
    import numpy as np

    def find_nearest(array, value):
        idx = (np.abs(array - value)).argmin()
        return int(idx)

    def find_nearest_coords(array, region_coords):
        for lon_value in region_coords[:2]:
            region_idx = region_coords.index(lon_value)
            idx = find_nearest(data['longitude'], lon_value)
            if region_coords[region_idx] != float(data['longitude'][idx].values):
                print('longitude value of latlonbox did not match, '
                      'updating to nearest value')
            region_coords[region_idx] = float(data['longitude'][idx].values)
        for lat_value in region_coords[2:]:
            region_idx = region_coords.index(lat_value)
            idx = find_nearest(data['latitude'], lat_value)
            if region_coords[region_idx] != float(data['latitude'][idx].values):
                print('latitude value of latlonbox did not match, '
                      'updating to nearest value')
            region_coords[region_idx] = float(data['latitude'][idx].values)
        return region_coords

    if region == 'EU':
        west_lon = -30; east_lon = 40; south_lat = 35; north_lat = 65

    elif region ==  'U.S.':
        west_lon = -120; east_lon = -70; south_lat = 20; north_lat = 50

    if type(region) == list:
        west_lon = region[0]; east_lon = region[1];
        south_lat = region[2]; north_lat = region[3]
    region_coords = [west_lon, east_lon, south_lat, north_lat]

    # Update regions coords in case they do not exactly match
    region_coords = find_nearest_coords(data, region_coords)
    west_lon = region_coords[0]; east_lon = region_coords[1];
    south_lat = region_coords[2]; north_lat = region_coords[3]


    lonstep = abs(data.longitude[1] - data.longitude[0])
    latstep = abs(data.latitude[1] - data.latitude[0])
    # abs() enforces that all values are positve, if not the case, it will not meet
    # the conditions
    lons = abs(np.arange(data.longitude[0], data.longitude[-1]+lonstep, lonstep))



    if (lons == np.array(data.longitude.values)).all():

        lons = list(np.arange(west_lon, east_lon+lonstep, lonstep))
        lats = list(np.arange(south_lat, north_lat+latstep, latstep))

        all_values = data.sel(latitude=lats, longitude=lons)
    if west_lon <0 and east_lon > 0:
        # left_of_meridional = np.array(data.sel(latitude=slice(north_lat, south_lat), longitude=slice(0, east_lon)))
        # right_of_meridional = np.array(data.sel(latitude=slice(north_lat, south_lat), longitude=slice(360+west_lon, 360)))
        # all_values = np.concatenate((np.reshape(left_of_meridional, (np.size(left_of_meridional))), np.reshape(right_of_meridional, np.size(right_of_meridional))))
        lon_idx = np.concatenate(( np.arange(find_nearest(data['longitude'], 360 + west_lon), len(data['longitude'])),
                              np.arange(0,find_nearest(data['longitude'], east_lon), 1) ))
        lat_idx = np.arange(find_nearest(data['latitude'],north_lat),find_nearest(data['latitude'],south_lat),1)
        all_values = data.sel(latitude=slice(north_lat, south_lat),
                              longitude=(data.longitude > 360 + west_lon) | (data.longitude < east_lon))
    if west_lon < 0 and east_lon < 0:
        all_values = data.sel(latitude=slice(north_lat, south_lat), longitude=slice(360+west_lon, 360+east_lon))
        lon_idx = np.arange(find_nearest(data['longitude'], 360 + west_lon), find_nearest(data['longitude'], 360+east_lon))
        lat_idx = np.arange(find_nearest(data['latitude'],north_lat),find_nearest(data['latitude'],south_lat),1)

    return all_values, region_coords

def selbox_to_1dts(cls, latlonbox):
    marray, var_class = import_array(cls, path='pp')
    selboxmarray, region_coords = find_region(marray, latlonbox)
    print('spatial mean over latlonbox {}'.format(region_coords))
    lats = selboxmarray.latitude.values
    cos_box = np.cos(np.deg2rad(lats))
    cos_box_array = np.tile(cos_box, (selboxmarray.longitude.size,1) )
    weights_box = np.swapaxes(cos_box_array, 1,0)
    RV_fullts = (selboxmarray*weights_box).mean(dim=('latitude','longitude'))
    return RV_fullts



def detrend1D(da, anomaly=False):
    import scipy.signal as sps
    import xarray as xr
    if da.dims[0] == 'index':
        # rename axes to 'time'
        da = da.rename({'index':'time'})
    dates = pd.to_datetime(da.time.values)
    stepsyr = dates.where(dates.year == dates.year[0]).dropna(how='all')

    if (stepsyr.day== 1).all() == True or int(da.time.size / 365) >= 120:
        print('\nHandling time series longer then 120 day or monthly data, no smoothening applied')
        data_smooth = da.values

    elif (stepsyr.day== 1).all() == False and int(da.time.size / 365) < 120:
        window_s = max(min(25,int(stepsyr.size / 12)), 1)
        print('Performing {} day rolling mean with gaussian window (std={})'
              ' to get better interannual statistics'.format(window_s, window_s/2))

        print('using absolute anomalies w.r.t. climatology of '
              'smoothed concurrent day accross years')
        data_smooth =  rolling_mean_np(da.values, window_s)
    output = np.empty( (da.time.size), dtype='float32' )
    for i in range(stepsyr.size):
        sliceyr = np.arange(i, da.time.size, stepsyr.size)
        arr_oneday = da.isel(time=sliceyr)
        arr_oneday_smooth = data_smooth[sliceyr]

        detrended_sm = xr.DataArray(sps.detrend(arr_oneday_smooth),
                            dims=arr_oneday.dims,
                            coords=arr_oneday.coords)
        # subtract trend smoothened signal of arr_oneday values
        if anomaly == False:
            trend = (arr_oneday_smooth - detrended_sm)            
        else:
            trend = (arr_oneday_smooth - detrended_sm)- np.mean(arr_oneday_smooth, 0)
        detrended = arr_oneday - trend
        output[i::stepsyr.size] = detrended
    dao = xr.DataArray(output,
                            dims=da.dims,
                            coords=da.coords)
    return dao


def rolling_mean_np(arr, win, center=True, plot=False):
    import scipy.signal.windows as spwin
    if plot == True:
        plt.plot(range(-int(win/2),+int(win/2)+1), spwin.gaussian(win, win/2))
        plt.title('window used for rolling mean')
        plt.xlabel('timesteps')
    df = pd.DataFrame(data=arr.reshape( (arr.shape[0], arr[0].size)))

    rollmean = df.rolling(win, center=center, min_periods=1,
                          win_type='gaussian').mean(std=win/2.)

    return rollmean.values.reshape( (arr.shape))


def regrid_xarray(xarray_in, to_grid_res, periodic=True):
    #%%
    '''
    Only supports 2 (lat, lon) or 3 (time, lat, lon) xr.DataArrays
    '''
    import xesmf as xe
    method_list = ['bilinear', 'conservative', 'nearest_s2d', 'nearest_d2s', 'patch']
    method = method_list[0]


    ds = xr.Dataset({'data':xarray_in})
    ds = xarray_in

    if 'longitude' in ds.dims:
        ds = ds.rename({'longitude': 'lon',
                        'latitude' : 'lat'})

    lats = ds.lat
    lons = ds.lon
    orig_grid = float(abs(ds.lat[1] - ds.lat[0] ))
    
    if method == 'conservative':
        # add lon_b and lat_b
        

        lat_b = np.concatenate(([lats.max()+orig_grid/2.], (lats - orig_grid/2.).values))
        lon_b = np.concatenate(([lons.max()+orig_grid/2.], (lons - orig_grid/2.).values))
        ds['lat_b'] = xr.DataArray(lat_b, dims=['lat_b'], coords={'lat_b':lat_b})
        ds['lon_b'] = xr.DataArray(lon_b, dims=['lon_b'], coords={'lon_b':lon_b})

        lat0_b = lat_b.min()
        lat1_b = lat_b.max()
        lon0_b = lon_b.min()
        lon1_b = lon_b.max()
    else:
        lat0_b = lats.min()
        lat1_b = lats.max()
        lon0_b = lons.min()
        lon1_b = lons.max()
    to_grid = xe.util.grid_2d(lon0_b, lon1_b, to_grid_res, lat0_b, lat1_b, to_grid_res)
#    to_grid = xe.util.grid_global(2.5, 2.5)
    regridder = xe.Regridder(ds, to_grid, method, periodic=periodic, reuse_weights=True)
    xarray_out = regridder(ds)
    regridder.clean_weight_file()
    xarray_out = xarray_out.rename({'lon':'longitude',
                                    'lat':'latitude'})
    if len(xarray_out.shape) == 2:
        xarray_out = xr.DataArray(xarray_out.values[::-1], 
                                  dims=['latitude', 'longitude'],
                                  coords={'latitude':xarray_out.latitude[:,0].values[::-1],
                                  'longitude':xarray_out.longitude[0].values})
    elif len(xarray_out.shape) == 3:
        xarray_out = xr.DataArray(xarray_out.values[:,::-1], 
                                  dims=['time','latitude', 'longitude'],
                                  coords={'time':xarray_out.time,
                                          'latitude':xarray_out.latitude[:,0].values[::-1],
                                          'longitude':xarray_out.longitude[0].values})   
    xarray_out.attrs = xarray_in.attrs
    xarray_out.name = xarray_in.name
    if 'is_DataArray' in xarray_out.attrs:
        del xarray_out.attrs['is_DataArray']
    xarray_out.attrs['regridded'] = f'{method}_{orig_grid}d_to_{to_grid_res}d'
#    xarray_out['longitude'] -= xarray_out['longitude'][0] # changed 17-11-20
    #%%
    return xarray_out

def store_hdf_df(dict_of_dfs, file_path=None):
    import warnings
    import tables
    today = datetime.datetime.today().strftime("%d-%m-%y_%Hhr")
    if file_path is None:
        file_path = get_download_path()+ f'/pandas_dfs_{today}.h5'

    warnings.filterwarnings('ignore', category=tables.NaturalNameWarning)
    with pd.HDFStore(file_path, 'w') as hdf:
        for key, item in  dict_of_dfs.items():
            try:
                hdf.put(key, item, format='table', data_columns=True)
            except:
                hdf.put(key, item, data_columns=True)
            if item.index.name is not None:
                hdf.root._v_attrs[key] = str(item.index.name)
        hdf.close()
    return file_path

def load_hdf5(path_data):
    '''
    Loading hdf5 can not be done simultaneously:
    '''
    import h5py
    import time
    for attempt in range(5):
        try:
            hdf = h5py.File(path_data,'r+')
        except:
            time.sleep(0.5) # wait 0.5 seconds, perhaps other process is trying
            # to load it simultaneously
            continue
        else:
            break
    dict_of_dfs = {}
    for k in hdf.keys():
        df = pd.read_hdf(path_data, k)
        if k in hdf.attrs.keys():
            str_attr_index = str(hdf.attrs[k])
            df.index.name = str_attr_index
        dict_of_dfs[k] = df
    hdf.close()
    return dict_of_dfs

def rand_traintest_years(RV, test_yrs=None, method=str, seed=None, 
                         kwrgs_events=None, verb=0):
    #%%
    '''
    possible method are:
    random{int} : with the int(method[6:8]) determining the amount of folds
    leave{int} : chronologically split train and test years
    split{int} : split dataset into single train and test set
    no_train_test_split.
    
    if test_yrs are given, all arguments are overwritten and we return the samme
    train test masks that are in compliance with the test yrs
    '''


    RV_ts = RV.RV_ts
    tested_yrs = [] ; # ex['n_events'] = []
    all_yrs = list(np.unique(RV_ts.index.year))
    n_yrs   = len(all_yrs)
    
    if test_yrs is not None:
        method = 'copied_from_import_ts'
        n_spl  = test_yrs.shape[0]
    if method[:6] == 'random' or method[:9] == 'ran_strat':
        if seed is None:
            seed = 30 # control reproducibility train/test split
        else:
            seed = seed
        if method[:6] == 'random':
            n_spl = int(method[6:8])
        else:
             n_spl = int(method[9:])
    elif method[:5] == 'leave':
        n_spl = int(n_yrs / int(method.split('_')[1]) )
        iterate = np.arange(0, n_yrs+1E-9,
                            int(method.split('_')[1]), dtype=int )
    elif method == 'no_train_test_split': 
        n_spl = 1



    full_time  = pd.to_datetime(RV.fullts.index)
    RV_time  = pd.to_datetime(RV_ts.index.values)
    RV_mask = np.array([True if d in RV_time else False for d in full_time])
    full_years  = list(RV.fullts.index.year.values)
    RV_years  = list(RV_ts.index.year.values)

    traintest = [] ; list_splits = []
    for s in range(n_spl):

        # conditions failed initally assumed True
        a_conditions_failed = True
        count = 0

        while a_conditions_failed == True:
            count +=1
            a_conditions_failed = False


            if method[:6] == 'random' or method[:9] == 'ran_strat':


                rng = np.random.RandomState(seed)
                size_test  = int(np.round(n_yrs / n_spl))
                size_train = int(n_yrs - size_test)

                leave_n_years_out = size_test
                yrs_to_draw_sample = [yr for yr in all_yrs if yr not in flatten(tested_yrs)]
                if (len(yrs_to_draw_sample)) >= size_test:
                    rand_test_years = rng.choice(yrs_to_draw_sample, leave_n_years_out, replace=False)
                # if last test sample will be too small for next iteration, add test yrs to current test yrs
                if (len(yrs_to_draw_sample)) < size_test:
                    rand_test_years = yrs_to_draw_sample
                check_double_test = [yr for yr in rand_test_years if yr in flatten( tested_yrs )]
                if len(check_double_test) != 0 :
                    a_conditions_failed = True
                    print('test year drawn twice, redoing sampling')


            elif method[:5] == 'leave':
                leave_n_years_out = int(method.split('_')[1])
                t0 = iterate[s]
                t1 = iterate[s+1]
                rand_test_years = all_yrs[t0: t1]

            elif method[:5] == 'split':
                size_train = int(np.percentile(range(len(all_yrs)), int(method[5:])))
                size_test  = len(all_yrs) - size_train
                leave_n_years_out = size_test
                print('Using {} years to train and {} to test'.format(size_train, size_test))
                rand_test_years = all_yrs[-size_test:]

            elif method == 'no_train_test_split':
                size_train = len(all_yrs)
                size_test  = 0
                leave_n_years_out = size_test
                print('No train test split'.format(size_train, size_test))
                rand_test_years = []

            elif method == 'copied_from_import_ts':
                size_train = len(all_yrs)
                rand_test_years = test_yrs[s]
                if s == 0:
                    size_test  = len(rand_test_years)
                leave_n_years_out = len(test_yrs[s])




            # test duplicates
            a_conditions_failed = np.logical_and((len(set(rand_test_years)) != leave_n_years_out),
                                     s != n_spl-1)
            # Update random years to be selected as test years:
        #        initial_years = [yr for yr in initial_years if yr not in random_test_years]
            rand_train_years = [yr for yr in all_yrs if yr not in rand_test_years]



            TrainIsTrue = np.zeros( (full_time.size), dtype=bool )

            Prec_train_idx = [i for i in range(len(full_years)) if full_years[i] in rand_train_years]
            RV_train_idx = [i for i in range(len(RV_years)) if RV_years[i] in rand_train_years]
            RV_train = RV_ts.iloc[RV_train_idx]


            TrainIsTrue[Prec_train_idx] = True


            if method != 'no_train_test_split':
                Prec_test_idx = [i for i in range(len(full_years)) if full_years[i] in rand_test_years]
                RV_test_idx = [i for i in range(len(RV_years)) if RV_years[i] in rand_test_years]
                RV_test = RV_ts.iloc[RV_test_idx]

                test_years = np.unique(RV_test.index.year)

                if method[:9] == 'ran_strat':
                    RV_bin = RV.RV_bin.iloc[RV_test_idx]
                    # check if representative sample
                    out = check_test_split(RV, RV_bin, kwrgs_events, a_conditions_failed,
                                           s, count, seed, verb)
                    a_conditions_failed, count, seed = out
            else:
                RV_test = [] ; test_years = [] ; Prec_test_idx = []
        data = np.concatenate([TrainIsTrue[None,:], RV_mask[None,:]], axis=0)
        list_splits.append(pd.DataFrame(data=data.T,
                                       columns=['TrainIsTrue', 'RV_mask'],
                                       index = full_time))

        tested_yrs.append(test_years)

        traintest_ = dict( { 'years'            : test_years,
                            'RV_train'          : RV_train,
                            'Prec_train_idx'    : Prec_train_idx,
                            'RV_test'           : RV_test,
                            'Prec_test_idx'     : Prec_test_idx} )
        traintest.append(traintest_)

    df_splits = pd.concat(list_splits , axis=0, keys=range(n_spl))

    #%%
    return df_splits



def check_test_split(RV, RV_bin, kwrgs_events, a_conditions_failed, s, count, seed, verbosity=0):
    #%%
    tol_from_exp_events = 0.20

    if kwrgs_events is None:
        print('Stratified Train Test based on +1 tercile events\n')
        kwrgs_events  =  {'event_percentile': 66,
                    'min_dur' : 1,
                    'max_break' : 0,
                    'grouped' : False}

    if kwrgs_events['event_percentile'] == 'std':
        exp_events_r = 0.15
    elif type(kwrgs_events['event_percentile']) == int:
        exp_events_r = 1 - kwrgs_events['event_percentile']/100


    test_years = np.unique(RV_bin.index.year)
    n_yrs      = np.unique(RV.RV_ts.index.year).size
    exp_events = (exp_events_r * RV.RV_ts.size / n_yrs) * test_years.size
    tolerance  = tol_from_exp_events * exp_events
    event_test = RV_bin
    diff       = abs(len(event_test) - exp_events)


    if diff > tolerance:
        if verbosity > 1:
            print('not a representative sample drawn, drawing new sample')
        seed += 1 # next random sample
        a_conditions_failed = True
    else:
        if verbosity > 0:
            print('{}: test year is {}, with {} events'.format(s, test_years, len(event_test)))
    if count == 7:
        if verbosity > 1:
            print(f"{s}: {count+1} attempts made, lowering tolence threshold from {tol_from_exp_events} "
                "to 0.40 deviation from mean expected events" )
        tol_from_exp_events = 0.40
    if count == 10:
        if verbosity > 1:
            print(f"kept sample after {count+1} attempts")
            print('{}: test year is {}, with {} events'.format(s, test_years, len(event_test)))
        a_conditions_failed = False
    #%%
    return a_conditions_failed, count, seed


def get_testyrs(df_splits):
    #%%
    traintest_yrs = []
    splits = df_splits.index.levels[0]
    for s in splits:
        df_split = df_splits.loc[s]
        test_yrs = np.unique(df_split[df_split['TrainIsTrue']==False].index.year)
        traintest_yrs.append(test_yrs)
    return np.array(traintest_yrs)


def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'Downloads')

def dfsplits_to_dates(df_splits, s):
    dates_train = df_splits.loc[s]['TrainIsTrue'][df_splits.loc[s]['TrainIsTrue']].index
    dates_test  = df_splits.loc[s]['TrainIsTrue'][~df_splits.loc[s]['TrainIsTrue']].index
    return dates_train, dates_test

def func_dates_min_lag(dates, lag):
    if lag != 0:
        tfreq = dates[1] - dates[0]
        oneyr = get_oneyr(pd.to_datetime(dates.values))
        start_d_min_lag = oneyr[0] - pd.Timedelta(int(lag), unit='d')
        end_d_min_lag = oneyr[-1] - pd.Timedelta(int(lag), unit='d')
        if pd.Timestamp(f'{dates[0].year}-01-01') > start_d_min_lag:
            start_d_min_lag = pd.Timestamp(f'{dates[0].year}-01-01') 
        
        startyr = pd.date_range(start_d_min_lag, end_d_min_lag, freq=tfreq)
        
        if startyr.is_leap_year[0]:
            # ensure that everything before the leap day is shifted one day back in time
            # years with leapdays now have a day less, thus everything before
            # the leapday should be extended back in time by 1 day.
            mask_lpyrfeb = np.logical_and(startyr.month == 2,
                                                 startyr.is_leap_year
                                                 )
            mask_lpyrjan = np.logical_and(startyr.month == 1,
                                                 startyr.is_leap_year
                                                 )
            mask_ = np.logical_or(mask_lpyrfeb, mask_lpyrjan)
        
            new_dates = np.array(startyr)
            if np.logical_and(startyr[0].month==1, startyr[0].day==1)==False:
                # compensate lag shift for removing leap day
                new_dates[mask_] = startyr[mask_] - tfreq
            else:
                startyr =core_pp.remove_leapdays(startyr)
    else:
        startyr = get_oneyr(pd.to_datetime(dates.values))
   
    dates_min_lag = make_dates(startyr, np.unique(dates.year))

    
    # to be able to select date in pandas dataframe
    dates_min_lag_str = [d.strftime('%Y-%m-%d %H:%M:%S') for d in dates_min_lag]
    return dates_min_lag_str, dates_min_lag    

def apply_lsm(var_filepath, lsm_filepath, threshold_lsm=.8):
    from pathlib import Path
    path = Path(var_filepath)
    xarray = core_pp.import_ds_lazy(path.as_posix())
    lons = xarray.longitude.values
    lats = xarray.latitude.values
    selbox = (min(lons), max(lons)+1, min(lats), max(lats)+1)
    lsm = core_pp.import_ds_lazy(lsm_filepath, selbox=selbox)
    lsm = lsm.to_array().squeeze() > threshold_lsm
    xarray['mask'] = (('latitude', 'longitude'), lsm[::-1].values)
    xarray = xarray.where( xarray['mask'] )
    xarray[0].plot()
    xarray = xarray.where(xarray.values != 0.).fillna(-9999)
    xarray.attrs.pop('is_DataArray')
    encoding = ( {xarray.name : {'_FillValue': -9999}} )
    mask =  (('latitude', 'longitude'), (xarray.values[0] != -9999) )
    xarray.coords['mask'] = mask
    parts = list(path.parts)
    parts[5] = 'lsm_' +parts[5]
    outfile = Path(*parts)
    # save netcdf
    xarray.to_netcdf(outfile, mode='w', encoding=encoding)

def sort_d_by_vals(d):
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[1])}
