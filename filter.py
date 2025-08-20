'''
This script allows to get filter from file name and maps it to BHTOM filter.

'''

import re

filters = {"_B_" : "GaiaSP/B", "_V_" : "GaiaSP/V", "_R_" : "GaiaSP/R", "_U_" : "GaiaSP/I", "_R_" : "GaiaSP/I", 
        "_rs_" : "GaiaSP/r", "_gs_" : "GaiaSP/g", "_is_" : "GaiaSP/i", "_us_" : "GaiaSP/u", "_zs_" : "GaiaSP/z",
        " " : "GaiaSP/any"}

def get_filter(file):
    match = re.search(r'_([A-Za-z])_', file)
    if match:
        return match.group(0)
    else:
        return None

def BHTOM_filter(filter):
    return filters.get(filter)

print("TEST")
print(get_filter("2024-09-30_06-42-09_PKS0454-234_B_180.00s_1x1_0_0286_out.fits"))
print(BHTOM_filter(get_filter("2024-09-30_06-42-09_PKS0454-234_B_180.00s_1x1_0_0286_out.fits")))
