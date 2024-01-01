


# Tool package for POLYMER


import netCDF4 as nc4
import ast
import numpy as np
import datetime as dt
import math
import sys



# Get datetime object 
def get_datetime(sat_file):
    with nc4.Dataset(sat_file,"r") as nc:
        
        print('test')
        
        try: 
            datetime_sat_string = nc.getncattr('time_coverage_start')
            datetime_sat_string = datetime_sat_string[:-5]
            format_string = '%Y-%m-%dT%H:%M:%S'
            datetime_sat_obj = dt.datetime.strptime(datetime_sat_string, format_string)
            add_a_day = False
            
        # in case 'time_coverage_start' is missing in the nc file
        except: 
            # product_name = nc.getncattr('product_name')[17:25]
            # format_string = '%Y%m%d'
            # datetime_sat_obj = dt.datetime.strptime(product_name, format_string)   
            # add_a_day = True
            sys.exit('L2gen processing problem')
        
    return [datetime_sat_obj, add_a_day]
    
    

# Read NC data 

def read_file(sat_file):
    
    with nc4.Dataset(sat_file,"r") as nc:
        
        # L2gen outputs use valid_min and valid_max which is problematic sometimes...
        # Disable masks to deal with this 
        nc.set_auto_mask(False)
        
        
        ### Read data 
        
        instrument = nc.getncattr('instrument')
        platform = nc.getncattr('platform')
        
        # wavelengths 
        if instrument == 'MSI':
            column_names = ['B1','B2','B3','B4','B5','B6','B7','B8']
            if platform == 'Sentinel-2A': 
                sensor = 'S2A_MSI'
                bands = [443,492,560,665,704,740,783,835]
                
            elif platform == 'Sentinel-2B': 
                sensor = 'S2B_MSI'
                bands = [442,492,559,665,704,739,780,835]
        
        elif instrument == 'OLI':
            column_names = ['B1','B2','B3','B4']
            bands = [443,482,561,655]
            sensor = 'L8_OLI'
        
        
        # band names for extracting values
        band_names = ['Rrs_' + str(item) for item in bands]

        # dimension
        width = len(nc.dimensions['pixels_per_line']) # equivalent to 'pixels' before 
        height = len(nc.dimensions['number_of_lines']) # equivalent to 'lines' before 

        # latlon
        lat = nc.groups['navigation_data'].variables['latitude'][:,:]
        lon = nc.groups['navigation_data'].variables['longitude'][:,:]

        # to store data
        rhow_data = np.ma.empty([len(bands),int(height),int(width)])

        for k in range(len(bands)):
            varname = band_names[k]
            
            # extract attributes 
            v_attributes = nc.groups['geophysical_data'].variables[varname].__dict__
            v_fill = float(v_attributes['_FillValue'])
            v_scale = float(v_attributes['scale_factor'])
            v_add = float(v_attributes['add_offset'])
            
            # apply mask manually 
            mask_value = (v_fill * v_scale + v_add) * 0.99
            
            arr_temp = nc.groups['geophysical_data'].variables[varname][:,:]
            arr_temp[arr_temp < mask_value] = np.nan
            
            ### Check L8 processing, if the same !!!
            
            rhow_data[k] = arr_temp * math.pi
            
    return {'bands': band_names,            # variable names of the bands 
            'sensor': sensor,
            'column_names': column_names,   # column names for final output
            'width': width,                 # width of the data array
            'height': height,               # height of the data array
            'lat': lat,                     # 2d data array: latitude at [y,x]
            'lon': lon,                     # 2d data array: longitude at [y,x]
            'rhow_data': rhow_data}         # 3d data array: reflectance at [band, y, x]





















