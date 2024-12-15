## Packages ##
import xarray as xr
#from netCDF4 import Dataset, num2date
import cartopy
import cartopy.crs as ccrs
from cartopy.util import add_cyclic_point
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

#####################
## DATA PROCESSING ##
#####################

## Precipitation Data ##
start_date = datetime(2023, 12, 1, 6) #2023-12-01T:06:00:00
end_date = datetime(2024, 8, 1, 6) #2024-08-01T06:00:00

date_series = []

current_date = start_date
while current_date <= end_date:
    date_series.append(current_date.strftime('%Y%m%d%H'))
    date_series.append((current_date+relativedelta(days=15)).strftime('%Y%m%d%H'))
    current_date += relativedelta(months=1)
    
all_data_precip = []
    
for i in range(len(date_series)-1):
    start_date = date_series[i]
    end_date = date_series[i+1]
    data_lsp = xr.open_dataset(f"ERA5_Data/Precip_Output/e5.oper.fc.sfc.accumu.128_142_lsp.ll025sc.{start_date}_{end_date}.nc")
    data_cp = xr.open_dataset(f"ERA5_Data/Precip_Output/e5.oper.fc.sfc.accumu.128_143_cp.ll025sc.{start_date}_{end_date}.nc")
    
    data_lsp.load()
    data_cp.load()
    
    data_total_precip = data_lsp.drop_vars(list(data_lsp.data_vars))
    
    total_precip = data_lsp.LSP + data_cp.CP 
    
    total_precip.attrs = {
    'long_name': 'total precipitation',
    'short_name': 'tp',
    'units': 'm',
    'original_format': 'WMO GRIB 1 with ECMWF local table',
    'ecmwf_local_table': 'NaN',
    'ecmwf_parameter': 'NaN',
    'minimum_value': f"{total_precip.min()}",
    'maximum_value': f"{total_precip.max()}",
    'grid_specification': '0.25 degree x 0.25 degree from 90N to 90S and 0E to 359.75E (721 x 1440 Latitude/Longitude)'
    }
    
    bins = np.arange(0, 13, 6)
    data_binned = total_precip.groupby_bins('forecast_hour', bins).sum()
    first_half = data_binned.sel(forecast_hour_bins=slice(0,6)).reset_index('forecast_hour_bins', drop = True)
    second_half = data_binned.sel(forecast_hour_bins=slice(7,12)).reset_index('forecast_hour_bins', drop = True)
    second_half = second_half.assign_coords(forecast_initial_time=second_half.forecast_initial_time + np.timedelta64(6, 'h'))
    combined = xr.concat([first_half, second_half], dim='forecast_initial_time').squeeze()
    
    all_data_precip.append(combined)
    
total_precip = xr.concat(all_data_precip, dim = 'forecast_initial_time')
total_precip_USA = total_precip.sel(longitude = slice(360-135, 360-55), latitude = slice(60,15))

## Cleaning up the data before converting to netcdf
total_precip = total_precip.to_dataset(name='tp')
total_precip = total_precip.sortby('forecast_initial_time')
total_precip_USA = total_precip_USA.to_dataset(name = 'tp')
total_precip_USA = total_precip_USA.sortby('forecast_initial_time')

## Saving to netcdf
start_date = date_series[0] #2023-12-01T:06:00:00
end_date = date_series[-1] #2024-08-01T06:00:00

total_precip.to_netcdf(f'./Final_Data/ERA5_Total_Precipitation_{start_date}_{end_date}.nc')         
total_precip_USA.to_netcdf(f'./Final_Data/ERA5_Total_Precipitation_USA_{start_date}_{end_date}.nc')

####################################################################################################
####################################################################################################
## Temp Data ##
start_date = datetime(2024, 1, 1, 0) #2024-01-01T:00:00:00
end_date = datetime(2024, 8, 1, 0) #2024-08-01T00:00:00

date_series = []

current_date = start_date
while current_date <= end_date:
    date_series.append(current_date.strftime('%Y%m%d%H'))
    date_series.append((current_date+relativedelta(months=1)-relativedelta(hours=1)).strftime('%Y%m%d%H'))
    current_date += relativedelta(months=1)

all_data_temp = []
    
for i in range(0, len(date_series)-1, 2):
    # print(date_series[i], date_series[i+1])
    start_date = date_series[i]
    end_date = date_series[i+1]
    data_temp = xr.open_dataset(f"ERA5_Data/Temp_Output/e5.oper.an.sfc.128_167_2t.ll025sc.{start_date}_{end_date}.nc")
    
    data_temp.load()
    
    data_temp_sixth = data_temp.VAR_2T.isel(time=slice(0, None, 6))
    #print("1")
    all_data_temp.append(data_temp_sixth)
    
total_2t_temp = xr.concat(all_data_temp, dim = 'time')
total_2t_temp_USA = total_2t_temp.sel(longitude = slice(360-135, 360-55), latitude = slice(60,15))

## Cleaning up the data before converting
total_2t_temp = total_2t_temp.to_dataset(name = 't2m')
total_2t_temp = total_2t_temp.sortby('time')
total_2t_temp_USA = total_2t_temp_USA.to_dataset(name = 't2m')
total_2t_temp_USA = total_2t_temp_USA.sortby('time')

## Converting to netcdf
start_date = date_series[0] #2024-01-01T:00:00:00
end_date = date_series[-1] #2024-08-31T23:00:00

total_2t_temp.to_netcdf(f'./Final_Data/ERA5_2m_temp_{start_date}_{end_date}.nc')
total_2t_temp_USA.to_netcdf(f'./Final_Data/ERA5_2m_temp_USA_{start_date}_{end_date}.nc')

