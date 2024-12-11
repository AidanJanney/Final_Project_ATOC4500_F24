#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
import xarray # for conversion to netcdf
import os

############################################################
## Back to the data rodeo, let's wrangle some reforecasts ##
############################################################
## Set up storage and filesystem
data_path = "/projects/aija9929/Final_Project_ATOC4500_F24/"

# Specify the directory name
directory_name = "S2S_Data"

# Create the directory
try:
    os.mkdir(f"{data_path}{directory_name}")
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")

## Access S2S Data through ECMWF Web API ##
server = ECMWFDataServer()

####################
## REAL TIME DATA ##
####################
########## Precipitation Data #########
# Control Forecast
server.retrieve({
    "class": "s2",
    "dataset": "s2s",
    "date": "2024-01-01/2024-02-01/2024-03-01/2024-04-01/2024-05-01/2024-06-01", # 1/1, 2/1, 3/1, 4/1, 5/1, 6/1
    "expver": "prod",
    "levtype": "sfc",
    "model": "glob",
    "origin": "ecmf",
    "param": "228228", # total percipitation param id
    "step": "0/6/12/18/24/30/36/42/48/54/60/66/72/78/84/90/96/102/108/114/120/126/132/138/144/150/156/162/168/174/180/186/192/198/204/210/216/222/228/234/240/246/252/258/264/270/276/282/288/294/300/306/312/318/324/330/336/342/348/354/360/366/372/378/384/390/396/402/408/414/420/426/432/438/444/450/456/462/468/474/480/486/492/498/504/510/516/522/528/534/540/546/552/558/564/570/576/582/588/594/600/606/612/618/624/630/636/642/648/654/660/666/672/678/684/690/696/702/708/714/720/726/732/738/744/750/756/762/768/774/780/786/792/798/804/810/816/822/828/834/840/846/852/858/864/870/876/882/888/894/900/906/912/918/924/930/936/942/948/954/960/966/972/978/984/990/996/1002/1008/1014/1020/1026/1032/1038/1044/1050/1056/1062/1068/1074/1080/1086/1092/1098/1104",
    "stream": "enfo",
    "time": "00:00:00",
    "type": "cf",
    "target": f"{data_path}S2S_Data/precip_control.grib"
})

data = xarray.open_dataset(f"{data_path}S2S_Data/precip_control.grib", engine='cfgrib')
data.to_netcdf(f"{data_path}S2S_Data/precip_control.nc")
print("\033[1;32m Sucessfully Retrieved Control Forecast Precipitation Data, accessible at:", f"{data_path}S2S_Data/precip_control.nc \033[0m")

# Perturbed Forecast
server.retrieve({
    "class": "s2",
    "dataset": "s2s",
    "date": "2024-01-01/2024-02-01/2024-03-01/2024-04-01/2024-05-01/2024-06-01",
    "expver": "prod",
    "levtype": "sfc",
    "model": "glob",
    "number": "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20",
    "origin": "ecmf",
    "param": "228228",
    "step": "0/6/12/18/24/30/36/42/48/54/60/66/72/78/84/90/96/102/108/114/120/126/132/138/144/150/156/162/168/174/180/186/192/198/204/210/216/222/228/234/240/246/252/258/264/270/276/282/288/294/300/306/312/318/324/330/336/342/348/354/360/366/372/378/384/390/396/402/408/414/420/426/432/438/444/450/456/462/468/474/480/486/492/498/504/510/516/522/528/534/540/546/552/558/564/570/576/582/588/594/600/606/612/618/624/630/636/642/648/654/660/666/672/678/684/690/696/702/708/714/720/726/732/738/744/750/756/762/768/774/780/786/792/798/804/810/816/822/828/834/840/846/852/858/864/870/876/882/888/894/900/906/912/918/924/930/936/942/948/954/960/966/972/978/984/990/996/1002/1008/1014/1020/1026/1032/1038/1044/1050/1056/1062/1068/1074/1080/1086/1092/1098/1104",
    "stream": "enfo",
    "time": "00:00:00",
    "type": "pf",
    "target": f"{data_path}S2S_Data/precip_perturbed.grib"
})

data = xarray.open_dataset(f"{data_path}S2S_Data/precip_perturbed.grib", engine='cfgrib')
data.to_netcdf(f"{data_path}S2S_Data/precip_perturbed.nc")
print("\033[1;32m Sucessfully Retrieved Perturbed Forecast Precipitation Data, accessible at:", f"{data_path}S2S_Data/precip_perturbed.nc \033[0m")

########## 2-Meter Temperature Data #########
# Control Forecast
server.retrieve({
    "class": "s2",
    "dataset": "s2s",
    "date": "2024-01-01/2024-02-01/2024-03-01/2024-04-01/2024-05-01/2024-06-01",
    "expver": "prod",
    "levtype": "sfc",
    "model": "glob",
    "origin": "ecmf",
    "param": "167", # 2-meter temp param id
    "step": "0-24/24-48/48-72/72-96/96-120/120-144/144-168/168-192/192-216/216-240/240-264/264-288/288-312/312-336/336-360/360-384/384-408/408-432/432-456/456-480/480-504/504-528/528-552/552-576/576-600/600-624/624-648/648-672/672-696/696-720/720-744/744-768/768-792/792-816/816-840/840-864/864-888/888-912/912-936/936-960/960-984/984-1008/1008-1032/1032-1056/1056-1080/1080-1104",
    "stream": "enfo",
    "time": "00:00:00",
    "type": "cf",
    "target": f"{data_path}S2S_Data/temp_control.grib"
})

data = xarray.open_dataset(f"{data_path}S2S_Data/temp_control.grib", engine='cfgrib')
data.to_netcdf(f"{data_path}S2S_Data/temp_control.nc")
print("\033[1;32m Sucessfully Retrieved Control 2-meter Temperature Data, accessible at:", f"{data_path}S2S_Data/temp_control.nc \033[0m")

# Perturbed Forecast
server.retrieve({
    "class": "s2",
    "dataset": "s2s",
    "date": "2024-01-01/2024-02-01/2024-03-01/2024-04-01/2024-05-01/2024-06-01",
    "expver": "prod",
    "levtype": "sfc",
    "model": "glob",
    "number": "1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18/19/20",
    "origin": "ecmf",
    "param": "167",
    "step": "0-24/24-48/48-72/72-96/96-120/120-144/144-168/168-192/192-216/216-240/240-264/264-288/288-312/312-336/336-360/360-384/384-408/408-432/432-456/456-480/480-504/504-528/528-552/552-576/576-600/600-624/624-648/648-672/672-696/696-720/720-744/744-768/768-792/792-816/816-840/840-864/864-888/888-912/912-936/936-960/960-984/984-1008/1008-1032/1032-1056/1056-1080/1080-1104",
    "stream": "enfo",
    "time": "00:00:00",
    "type": "pf",
    "target": f"{data_path}S2S_Data/temp_perturbed.grib"
})

data = xarray.open_dataset(f"{data_path}S2S_Data/temp_perturbed.grib", engine='cfgrib')
data.to_netcdf(f"{data_path}S2S_Data/temp_perturbed.nc")
print("\033[1;32m Sucessfully Retrieved Perturbed 2-meter Temperature Data, accessible at:", f"{data_path}S2S_Data/temp_perturbed.nc \033[0m")


####################################################################################################
####################################################################################################
'''
#####################
## REFORECAST DATA ##
#####################
########## Precipitation Data #########
# Control Forecast
server.retrieve({
    "class": "s2",
    "dataset": "s2s",
    "date": "2024-01-01",
    "expver": "prod",
    "hdate": "2023-01-01",
    "levtype": "sfc",
    "model": "glob",
    "origin": "ecmf",
    "param": "228228",
    "step": "0/6/12/18/24/30/36/42/48/54/60/66/72/78/84/90/96/102/108/114/120/126/132/138/144/150/156/162/168/174/180/186/192/198/204/210/216/222/228/234/240/246/252/258/264/270/276/282/288/294/300/306/312/318/324/330/336/342/348/354/360/366/372/378/384/390/396/402/408/414/420/426/432/438/444/450/456/462/468/474/480/486/492/498/504/510/516/522/528/534/540/546/552/558/564/570/576/582/588/594/600/606/612/618/624/630/636/642/648/654/660/666/672/678/684/690/696/702/708/714/720/726/732/738/744/750/756/762/768/774/780/786/792/798/804/810/816/822/828/834/840/846/852/858/864/870/876/882/888/894/900/906/912/918/924/930/936/942/948/954/960/966/972/978/984/990/996/1002/1008/1014/1020/1026/1032/1038/1044/1050/1056/1062/1068/1074/1080/1086/1092/1098/1104",
    "stream": "enfh",
    "time": "00:00:00",
    "type": "cf",
    "target": f"{data_path}S2S_Data/precip_refcst_control.grib"
})
data = xarray.open_dataset(f"{data_path}S2S_Data/precip_refcst_control.grib", engine='cfgrib')
data.to_netcdf(f"{data_path}S2S_Data/precip_refcst_control.nc")
print(f"{"*"*40}\n Sucessfully Retrieved Control Reforecast Precipitation Data, accessible at:", f"{data_path}S2S_Data/precip_refcst_control.nc \n {"*"*40}")

# Perturbed Forecast
server.retrieve({
    "class": "s2",
    "dataset": "s2s",
    "date": "2024-01-01",
    "expver": "prod",
    "hdate": "2023-01-01",
    "levtype": "sfc",
    "model": "glob",
    "number": "1/2/3/4/5/6/7/8/9/10",
    "origin": "ecmf",
    "param": "228228",
    "step": "0/6/12/18/24/30/36/42/48/54/60/66/72/78/84/90/96/102/108/114/120/126/132/138/144/150/156/162/168/174/180/186/192/198/204/210/216/222/228/234/240/246/252/258/264/270/276/282/288/294/300/306/312/318/324/330/336/342/348/354/360/366/372/378/384/390/396/402/408/414/420/426/432/438/444/450/456/462/468/474/480/486/492/498/504/510/516/522/528/534/540/546/552/558/564/570/576/582/588/594/600/606/612/618/624/630/636/642/648/654/660/666/672/678/684/690/696/702/708/714/720/726/732/738/744/750/756/762/768/774/780/786/792/798/804/810/816/822/828/834/840/846/852/858/864/870/876/882/888/894/900/906/912/918/924/930/936/942/948/954/960/966/972/978/984/990/996/1002/1008/1014/1020/1026/1032/1038/1044/1050/1056/1062/1068/1074/1080/1086/1092/1098/1104",
    "stream": "enfh",
    "time": "00:00:00",
    "type": "pf",
    "target": f"{data_path}S2S_Data/precip_refcst_perturbed.grib"
})
data = xarray.open_dataset(f"{data_path}S2S_Data/precip_refcst_perturbed.grib", engine='cfgrib')
data.to_netcdf(f"{data_path}S2S_Data/precip_refcst_perturbed.nc")
print("Sucessfully Retrieved Perturbed Reforecast Precipitation Data, accessible at:", f"{data_path}S2S_Data/precip_refcst_perturbed.nc")

########## 2-Meter Temperature Data #########
# Control Forecast
server.retrieve({
    "class": "s2",
    "dataset": "s2s",
    "date": "2024-01-01",
    "expver": "prod",
    "hdate": "2023-01-01",
    "levtype": "sfc",
    "model": "glob",
    "origin": "ecmf",
    "param": "167",
    "step": "0-24/24-48/48-72/72-96/96-120/120-144/144-168/168-192/192-216/216-240/240-264/264-288/288-312/312-336/336-360/360-384/384-408/408-432/432-456/456-480/480-504/504-528/528-552/552-576/576-600/600-624/624-648/648-672/672-696/696-720/720-744/744-768/768-792/792-816/816-840/840-864/864-888/888-912/912-936/936-960/960-984/984-1008/1008-1032/1032-1056/1056-1080/1080-1104",
    "stream": "enfh",
    "time": "00:00:00",
    "type": "cf",
    "target": f"{data_path}S2S_Data/temp_refcst_control.grib"
})
data = xarray.open_dataset(f"{data_path}S2S_Data/temp_refcst_control.grib", engine='cfgrib')
data.to_netcdf(f"{data_path}S2S_Data/temp_refcst_control.nc")
print("Sucessfully Retrieved Control Reforecast 2-Meter Temperature Data, accessible at:", f"{data_path}S2S_Data/temp_refcst_control.nc")

# Perturbed Forecast
server.retrieve({
    "class": "s2",
    "dataset": "s2s",
    "date": "2024-01-01",
    "expver": "prod",
    "hdate": "2023-01-01",
    "levtype": "sfc",
    "model": "glob",
    "number": "1/2/3/4/5/6/7/8/9/10",
    "origin": "ecmf",
    "param": "167",
    "step": "0-24/24-48/48-72/72-96/96-120/120-144/144-168/168-192/192-216/216-240/240-264/264-288/288-312/312-336/336-360/360-384/384-408/408-432/432-456/456-480/480-504/504-528/528-552/552-576/576-600/600-624/624-648/648-672/672-696/696-720/720-744/744-768/768-792/792-816/816-840/840-864/864-888/888-912/912-936/936-960/960-984/984-1008/1008-1032/1032-1056/1056-1080/1080-1104",
    "stream": "enfh",
    "time": "00:00:00",
    "type": "pf",
    "target": f"{data_path}S2S_Data/temp_refcst_perturbed.grib"
})
data = xarray.open_dataset(f"{data_path}S2S_Data/temp_refcst_perturbed.grib", engine='cfgrib')
data.to_netcdf(f"{data_path}S2S_Data/temp_refcst_perturbed.nc")
print("Sucessfully Retrieved Perturbed Reforecast 2-Meter Temperature Data, accessible at:", f"{data_path}S2S_Data/temp_refcst_perturbed.nc")
'''
