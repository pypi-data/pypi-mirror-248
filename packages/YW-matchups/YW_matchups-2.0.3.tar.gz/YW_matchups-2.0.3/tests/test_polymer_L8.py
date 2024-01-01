# Go up by 2 directory and import 

import sys
import os.path as path
two_up =  path.abspath(path.join(__file__ ,"../.."))
sys.path.append(two_up)

import YW_matchups






sat_folder = '/Users/yw/Downloads/test_polymer'
is_file = '/Users/yw/Local_storage/GLORIA/6_output_L8_noRrs.csv'
out_file = '/Users/yw/Downloads/test_polymer/text.csv'






test = YW_matchups.run(sat_folder, is_file, AC='POLYMER', out_file=out_file, to_log = True)






'''
# Plot 

from matplotlib import pyplot as plt
plt.imshow(test3, interpolation='nearest')
plt.show()

'''

