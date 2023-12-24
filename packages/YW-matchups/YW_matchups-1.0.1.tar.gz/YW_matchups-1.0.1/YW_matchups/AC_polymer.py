


# Tool package for POLYMER


import netCDF4 as nc4
import ast
import numpy as np
import datetime as dt



# Get datetime object 
def get_datetime(sat_file):
    with nc4.Dataset(sat_file,"r") as nc:
        
        datetime_sat_string = nc.getncattr('sensing_time')
        format_string = '%Y-%m-%d %H:%M:%S'
        datetime_sat_obj = dt.datetime.strptime(datetime_sat_string, format_string)
    
    return datetime_sat_obj
    
    

# Read NC data 

def read_file(sat_file):
    
    with nc4.Dataset(sat_file,"r") as nc:
        tile_id = nc.getncattr('L1_TILE_ID')
        
        # wavelengths 
        # Currenlty only works for Sentinel-2!!!!!!
        sensor = tile_id[0:3]
        if sensor == 'S2A' or sensor == 'S2B':
            column_names = ['B1','B2','B3','B4','B5','B6','B7','B8','B8A','B11']
            if sensor == 'S2A': sensor = 'S2A_MSI'
            if sensor == 'S2B': sensor = 'S2B_MSI'
        
        bands = nc.getncattr('bands_rw')
        bands = ast.literal_eval(bands)
        
        # band names for extracting values
        band_names = ['Rw' + str(item) for item in bands]

        # dimension
        width = len(nc.dimensions['width']) # equivalent to 'pixels' before 
        height = len(nc.dimensions['height']) # equivalent to 'lines' before 

        # latlon
        lat = nc.variables['latitude'][:,:]
        lon = nc.variables['longitude'][:,:]

        # to store data
        rhow_data = np.ma.empty([len(bands),int(height),int(width)])

        for k in range(len(bands)):
            varname = band_names[k]
            rhow_data[k] = nc.variables[varname][:,:]
            
    return {'bands': band_names,            # variable names of the bands 
            'sensor': sensor,
            'column_names': column_names,   # column names for final output
            'width': width,                 # width of the data array
            'height': height,               # height of the data array
            'lat': lat,                     # 2d data array: latitude at [y,x]
            'lon': lon,                     # 2d data array: longitude at [y,x]
            'rhow_data': rhow_data}         # 3d data array: reflectance at [band, y, x]





















