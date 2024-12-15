# Data and Code Availability
All of the code used to produce figures and results is available in this public repository. We used data from the [Subseasonal-to-Seasonal (S2S) Dataset](https://apps.ecmwf.int/datasets/data/s2s/levtype=sfc/type=cf/) and the [ECMWF Reanalysis v5 (ERA5) Dataset](https://www.ecmwf.int/en/forecasts/dataset/ecmwf-reanalysis-v5). The S2S data is publicly available and the ERA5 data was retrieved from [NCAR's Research Data Archive](https://rda.ucar.edu/datasets/d633000/). All of the specifications of the data we used can be found within the code in this repository (contact me if you would like a specific list of dates and parameters). Additionally, our specific datasets are stored on CU Research Computing's System in the following directory: `/projects/aija9929/Final_Project_ATOC4500_F24`.

# Contents

- Folder:`S2S_Data` — contains the GRIB files directly from ECMWF S2S Dataset and the converted netCDF files for the same data
    - `precip_output.nc` contains the [accumulated precipitation from the beginning of the forecast](https://confluence.ecmwf.int/display/S2S/S2S+Total+Precipitation). To get the precipitation for each day, we want to take a difference for each day (e.g. tp(1/20) - tp(1/19) = precipitation for day 20.
    - `temp_output.nc` contains the [instantaneous surface temperature values](https://confluence.ecmwf.int/display/S2S/S2S+Surface+Air+Temperature) (2-meters above the ground for ECMWF). These measurements are taken every size hours at 00, 06, 12, and 18z (12am, 6am, 12pm, and 6pm).
- `ECMWF_Retrieval.py` — script to retrieve data from the ECMWF S2S data servers and convert it to netCDF format
    - More details below in the **Retrieving ECMWF Data** section
    - Needs to be run with a custom python environment/kernel that has ecmwf-api-client, eccodes, and cfgrib installed
- `S2S_data.ipynb` — (pretty much) blank notebook set up for data analysis (should be editable by all of us, we can also definitely figure out a different way to collaborate on it)!
- `S2S_visualization.ipynb` — blank notebook for graphing and other assorted things (thought it might be nice to have multiple notebooks set up)
- `S2S_Data_Handling.yaml` — config file for a conda environment that has all the necessary packages to run the ECMWF_Retrieval.py script. WARNING: some of the packages are very large (specifically eccodes?) if you do install this, use mamba instead of conda (more info below).

# Retrieving ECMWF S2S Data - [Dataset Link](https://apps.ecmwf.int/datasets/data/s2s-realtime-instantaneous-accum-ecmf/levtype=sfc/type=cf/)

I am super happy to retrieve whatever new data we might want because it’s kinda weird to set up, but I thought it would be useful to include details here!

### Setting Up ECMWF Account and API Key

- Create an account at https://www.ecmwf.int/
- After logging in, go to this site to get your API key: https://api.ecmwf.int/v1/key/

**Installing API Key**

1. Copy the content cell of the previous site, it should look something like this:

```bash
{
    "url"   : "https://api.ecmwf.int/v1",
    "key"   : "dhgf18327456mjbckjwgef75skjdf097",
    "email" : "aidan.janney@colorado.edu"
}
```

1. In research computing’s system, go to your home directory (either by typing `cd` into the command line or in JupyterHub File selector, go to `/home/<identikey>`)
2. Make a new file named `.ecmwfapirc` in your home directory (this can be done with the Jupyter hub interface, but I would recommend using the touch command (i.e. `touch .ecmwfapirc` )
3. Paste the contents that you copied from the API key website into this file, save it, and you are done!

### Setting Up Conda Environment to Run ECMWF_Retrieval Script

Back in the Final Project folder (`/projects/aija9929/Final_Project_ATOC4500_F24`)

- There is a file `S2S_Data_Handling.yaml` that gives conda information on which packages we need to have installed to retrieve the ECMWF data.
    - Some of the packages are really large, and they max out the memory if installed with conda, so instead use the mambaforge module
- In the command line run the following commands:
    
    ```bash
    module load mambaforge
    mamba env create -f S2S_Data_Handling.yaml
    ```
    
- It should successfully install all the necessary packages, but it might take some time!

### Retrieving the Data

- Now that everything has been configured, we can run the data retrieval script
- Run `ECMWF_Retrieval.py` from the command line with

```bash
conda activate S2S_Data_Handling
python ECMWF_Retrieval.py
```

- To get different dates and variables, consult the dataset site from above: https://apps.ecmwf.int/datasets/data/s2s-realtime-instantaneous-accum-ecmf/levtype=sfc/type=cf/
