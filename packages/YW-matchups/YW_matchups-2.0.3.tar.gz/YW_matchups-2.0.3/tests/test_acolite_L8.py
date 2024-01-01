# Go up by 2 directory and import 

import sys
import os.path as path
two_up =  path.abspath(path.join(__file__ ,"../.."))
sys.path.append(two_up)

import YW_matchups








# sat_file = '/Users/yw/Desktop/230613 AEC paper/231130 POLYMER/test_output_S2_60m.nc'


# sat_folder = '/Users/yw/Desktop/230613 AEC paper/231130 POLYMER'

sat_folder = '/Users/yw/Downloads/L8_out'
# sat_folder = '/Users/yw/Downloads'



is_file = '/Users/yw/Local_storage/GLORIA/6_output_L8_noRrs.csv'


out_file = '/Users/yw/Downloads/L8_out/text.csv'


test = YW_matchups.run(sat_folder, is_file, AC='ACOLITE', out_file=out_file, to_log = True)




'''
# Plot 

# Interactive mode
%matplotlib qt


test = sat_data['rhow_data']

test2 = test[0]



from matplotlib import pyplot as plt
plt.imshow(test, interpolation='nearest')
plt.show()

'''

