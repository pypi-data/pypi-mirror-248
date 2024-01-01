# Go up by 2 directory and import 

import sys
import os.path as path
two_up =  path.abspath(path.join(__file__ ,"../.."))
sys.path.append(two_up)

import YW_matchups








sat_folder = '/Users/yw/Downloads/L8_out'

is_file = '/Users/yw/Local_storage/GLORIA/6_output_L8_noRrs.csv'


out_file = '/Users/yw/Downloads/L8_out/text.csv'





test = YW_matchups.run(sat_folder, is_file, AC='L2gen', out_file=out_file, to_log = False)




'''
# Plot 



k=0
varname = band_names[k]
test = nc.groups['geophysical_data'].variables[varname][:]


test = sat_data['rhow_data'][0]



from matplotlib import pyplot as plt
plt.imshow(test, interpolation='nearest')
plt.show()





'''

