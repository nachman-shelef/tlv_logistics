#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# segments_cf_format_abs_output.py
#
print('-----------------  --------------------------')

import time
from pathlib import Path
import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas.tools import sjoin
import osmnx as ox

cwd = Path.cwd()
pathin = cwd.parent / 'processed'
pathproc = cwd.parent / 'processed'
pathout = cwd.parent / 'processed'

print("Local current time :", time.asctime( time.localtime(time.time()) ))
#_________________________________
#
#input 
infile = 'segments_cf_poly_metrics.geojson'
metrics_gdf = gpd.read_file(pathproc / infile, encoding='utf-8')
print(metrics_gdf)
metrics_gdf.info()

del metrics_gdf['quarter']
#metrics_gdf.rename(columns={'_t_street_e': '_shemangli', '_t_street': '_t_rechov', }, inplace=True)

print(metrics_gdf)
metrics_gdf.info()
#print(metrics_gdf.columns)

metric_col_list = ['sum_hours_x_meters_buff100', 
                    'sum_weekly_delivery_freq_buff100', 
                    'sum_hours_x_meters_snap100', 
                    'sum_weekly_delivery_freq_snap100', 
                    'min_per_delivery_buff100', 
                    'min_per_delivery_snap100',
                    'd2s_buff100',
                    'd2s_snap100']
#print(metric_col_list)

#project from 2039 to crs 4326 for leaflet
metrics_gdf = ox.project_gdf(metrics_gdf, to_crs='epsg:4326')
print(metrics_gdf['geometry'])
metrics_gdf.info()

#output segments_cf_poly_metrics_abs_4326.geojson
geojson_fileout = pathout / ('segments_cf_poly_metrics_abs_4326.geojson')
print(geojson_fileout)
metrics_gdf.to_file(geojson_fileout, driver="GeoJSON")

# reformat as js and output
txtfilein = geojson_fileout
textfileout = pathout / ('tlv_logistics_s2d.js')
fw = open(textfileout, 'w', encoding="utf8")
with open(txtfilein, encoding="utf8") as f:
    header = f.readline()
    fw.write('tlv_logistics_s2d = ' + header)
    #print(header)
    for row in f.readlines():
        #print (row)
        fw.write(row)
fw.close()
print(textfileout)


print("Local current time :", time.asctime( time.localtime(time.time()) ))
