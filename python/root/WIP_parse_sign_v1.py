#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# WIP**********************************

import time
from datetime import date
import pandas as pd
from pathlib import Path
#import json
import re

cwd = Path.cwd()
#print(cwd)
print("Local current time :", time.asctime( time.localtime(time.time()) ))
#

pathin = cwd.parent / 'data' 
pathout = cwd.parent / 'processed'

filepath = pathin / 'sign_text_test2.csv'


# set up regular expressions
# use https://regexper.com to visualise these if required
rx_dict = {
    'truck': re.compile(r'School = (?P<school>.*)\n'),
}




def _parse_line(line):
    """
    Do a regex search against all defined regexes and
    return the key and match result of the first matching regex

    """

    for key, rx in rx_dict.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None


out_list = []  # create an empty list to collect the data
# open the file and read through it line by line
with open(filepath, encoding="utf8") as f:
    line = f.readline()
    while line:
        print(line)
        
        # at each line check for a match with a regex
        key, match = _parse_line(line)

        # extract truck
        if key == 'truck':
            truck = match.group('truck')
        
        # create a dictionary containing this row of data
        row = {
            'Truck': truck
        }
        # append the dictionary to the data list
        out_list.append(row)
        
        
        # new line
        line = f.readline()
        
    print(out_list)