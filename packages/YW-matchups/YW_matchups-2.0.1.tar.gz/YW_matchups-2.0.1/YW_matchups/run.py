

# Strategy: throw everything here, put them into modules if too long or when necessary 







### Introduction 

# find matchups, mean and median for each of the window sizes 
# sensor in the last column 


### Problem

# POLYMER no sensing time for L8, therefore add a day to the time window 
# should be okay because L8 rarely visits the same place two days in a row





import numpy as np
import sys
import glob, os
import pyproj
import datetime as dt
import pandas as pd
import time
import warnings
from importlib.metadata import version

from . import AC_polymer
from . import AC_acolite
from . import AC_l2gen





def run(sat_folder=None, is_file=None, AC=None, out_file=None, to_log = True):
    
    
    ### Settings to be included later 
    time_window_minutes = 360 
    max_dist = 100
    
    
    # make it adaptive to sensor resolution ??
    # window_size = 3
    window_size = [1, 3, 5, 7]
    
    
    ### Print all metadata/settings and save them in a txt file
    
    if to_log: 
        # Start logging in txt file
        orig_stdout = sys.stdout
        
        log_file = out_file.replace(".csv", ".txt")
        # log_file = 'tmart_log_' + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time())) + '.txt'
    
        class Logger:
            def __init__(self, filename):
                self.console = sys.stdout
                self.file = open(filename, 'w')
                self.file.flush()
            def write(self, message):
                self.console.write(message)
                self.file.write(message)
            def flush(self):
                self.console.flush()
                self.file.flush()
    
        sys.stdout = Logger(log_file)
        
    
    # Metadata
    print('YW_matchups version: ' + str(version('YW_matchups')))
    print('System time: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    print('sat_folder: ' + str(sat_folder))
    print('In-situ file: ' + str(is_file))
    print('AC: ' + str(AC))
    print('out_file: ' + str(out_file))
    if to_log: print('log_file: ' + str(log_file))
    
    # Settings 
    print('window_size: ' + str(window_size))
    print('time_window_minutes: ' + str(time_window_minutes))
    print('max_dist: ' + str(max_dist))
    
    
    # Read in-situ data 
    df_is = pd.read_csv(is_file)
    dt_is_string = list(df_is.loc[:,"GLORIA_time"])
    dt_is_obj = [dt.datetime.strptime(dt_is_string[d],"%Y-%m-%dT%H:%M")for d in list(range(len(dt_is_string)))]
    
    
    
    
    ### find all NC files 
    
    # Keywords for .nc files 
    if AC=='POLYMER' or AC=='L2gen': 
        AC_file = '*.nc'
    elif AC=='ACOLITE':
        AC_file = '*L2W.nc'
    else: 
        sys.exit('Unknown AC algorithm')
    
    # Find them in the directory and subdirectory 
    # https://stackoverflow.com/questions/18394147/how-to-do-a-recursive-sub-folder-search-and-return-files-in-a-list
    sat_files = [y for x in os.walk(sat_folder) for y in glob.glob(os.path.join(x[0], AC_file))]
    
    # Output 
    df_output = pd.DataFrame()
    
    
    ### Loop through each of the sat_files
    
    for sat_i, sat_file in enumerate(sat_files): 
        
        print('\n{}/{}'.format(sat_i, len(sat_files)))
        print('Processing: {}'.format(sat_file))
        
        
        # Read datetime, for different AC
        if AC=='POLYMER': 
            dt_sat_obj, add_a_day = AC_polymer.get_datetime(sat_file)
        elif AC=='ACOLITE':
            dt_sat_obj, add_a_day = AC_acolite.get_datetime(sat_file)
        elif AC=='L2gen':
            dt_sat_obj, add_a_day = AC_l2gen.get_datetime(sat_file)

        # add a day for POLYMER L8 because we don't have the sensing time 
        # L2gen L8 missing datetime when no data returned
        # this is okay because L8 doesn't visit the same place two days in a row
        if add_a_day: time_window_minutes = time_window_minutes + 1440




        # Indices of in-situ data that match the sat datetime  
        is_matches = [ind for ind, s in enumerate(dt_is_obj) if abs((dt_sat_obj - s).total_seconds()/60) <= time_window_minutes]
        
        
        # If there are no matching records, skip to next satellite file.
        if len(is_matches)==0:
            print("No matches for this file within the time limit. Next...\n\n")
            continue
        elif len(is_matches) > 1:
            print('Number of matchups: ' + str(len(is_matches)))
        
        
        ### Read NC data, for different AC
        if AC=='POLYMER': 
            sat_data = AC_polymer.read_file(sat_file)
        elif AC=='ACOLITE':
            sat_data = AC_acolite.read_file(sat_file)
        elif AC=='L2gen':
            sat_data = AC_l2gen.read_file(sat_file)
        
        
        ### Loop through indices and row numbers of in-situ matchups
        
        for ind, row in enumerate(is_matches):
            print('Processing in-situ match {}, row {} in spreadsheet'.format(ind, row))
            
            ### Identify distances 
            
            in_situ_lat = df_is.loc[row,"lat"]
            in_situ_lon = df_is.loc[row,"lon"]
            
            # Project X and Y in meters, centred at the in-situ measurement 
            proj = pyproj.Proj(proj="gnom", ellps="WGS84", lat_0=in_situ_lat,
                               lon_0=in_situ_lon, datum="WGS84", units="m")
            x, y = proj(sat_data['lon'], sat_data['lat'])
            in_situ_x, in_situ_y = proj(in_situ_lon, in_situ_lat)
            
            # Calculate distance and indices of the closest 
            dist = np.sqrt((x - in_situ_x)**2 + (y - in_situ_y)**2)
            
            # Pixels within the max distance, True/False
            within_max_dist = dist < max_dist
            
            # Are there any valid pixels left?
            if np.sum(within_max_dist)==0:
                print("No pixels within acceptable distance (",max_dist,"m ). Next...\n")
                continue
            
            ### Find closest and extract values 
            
            indices_closest = np.argwhere(dist == np.min(dist))
            
            line = indices_closest[0][0]
            pixel = indices_closest[0][1]
            
            # extract the row as a series 
            row_temp = df_is.iloc[row]
            
            # Loop through window size 
            for ws in window_size: 
            
                # Get pixel coordinates of window around the matching point.
                # (v = vertical/line, h = horizontal/pixel)
                v1 = np.int32(line - ((ws-1)/2))
                v2 = np.int32(line + ((ws+1)/2))
                h1 = np.int32(pixel - ((ws-1)/2))
                h2 = np.int32(pixel + ((ws+1)/2))
                
                # Trim edges of window if they're on the edge of the grid.
                line_start,line_end = max(0, v1), min(sat_data['height'], v2)
                # Window pixel start, pixel end.
                pixel_start,pixel_end = max(0, h1), min(sat_data['width'], h2)
                
                # Extract all values in this window
                rhow_data_window = sat_data['rhow_data'][:,line_start:line_end,pixel_start:pixel_end]
                
                # Column names 
                columns_mean    = ['mean_'+item+'_ws'+str(ws) for item in sat_data['column_names']]
                columns_median  = ['median_'+item+'_ws'+str(ws) for item in sat_data['column_names']]
                
                # Suppress mean/median of empty slice
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", category=RuntimeWarning)
                
                    # Mean and median values per band 
                    rhow_data_mean      = np.nanmean(rhow_data_window, axis=(1,2))
                    rhow_data_median    = np.nanmedian(rhow_data_window, axis=(1,2))
                
                # if rhow_data_mean.mask.all(): 
                #     print('All pixels are masked in the window.')
                #     continue
                
                # Add values to data frame
                row_mean    = pd.Series(data=rhow_data_mean,    index=columns_mean)
                row_median  = pd.Series(data=rhow_data_median,  index=columns_median)
                row_temp = pd.concat([row_temp, row_mean, row_median], axis=0)

            # Add sensor
            row_temp['sensor'] = sat_data['sensor']

            # Add to dataframe             
            df_output = pd.concat([df_output,row_temp.to_frame().T])
            
    # Stop logging 
    if to_log: sys.stdout = orig_stdout
    
    # Output dataframe 
    df_output.to_csv(out_file, index=False)

    return 0
    
    
    
    
    
    
    
    
    
    
    
    
    










