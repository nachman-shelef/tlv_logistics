#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# segments_cf_format_output.py
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
metrics_gdf.rename(columns={'_t_street_e': '_shemangli', '_t_street': '_t_rechov', }, inplace=True)

metrics_gdf['ids'] = metrics_gdf['_shemangli'] + '_' + metrics_gdf['id'].astype(str)
print(metrics_gdf)
metrics_gdf.info()


metric_col_list = ['sum_hours_x_meters_buff100', 
                    'sum_weekly_delivery_freq_buff100', 
                    'sum_hours_x_meters_snap100', 
                    'sum_weekly_delivery_freq_snap100', 
                    'min_per_delivery_buff100', 
                    'min_per_delivery_snap100']
#print(metric_col_list)

mean_list = []
std_list = []
mean_std_list=[]
for metric_col in metric_col_list :
    mean_std_list.append(list([metrics_gdf[metric_col].mean(), metrics_gdf[metric_col].std()]))

mean_std_df = pd.DataFrame({'metric': metric_col_list, 'mean_std': mean_std_list})
mean_std_df = mean_std_df.set_index('metric')
print(mean_std_df)

#output average_stdev.js
json_fileout = pathout / ('average_stdev.js')
print(json_fileout)
#mean_std_df.to_json(json_fileout)
json_str = mean_std_df.to_json()
json_str = json_str.replace('{"mean_std":{', 'var averageStdev = {\n').replace(']}}', ']\n};').replace('],"', '],\n"')
print(json_str)
nf = open(json_fileout, "w", encoding="utf8")
nf.write(json_str)
nf.close()
print(("Saved file: ", json_fileout))

# reformat metrics as norm 
for metric_col in metric_col_list :
    #print(metric_col)
    metrics_gdf['mean_'+ metric_col] = metrics_gdf[metric_col].mean()
    metrics_gdf['std_'+ metric_col] = metrics_gdf[metric_col].std()
    metrics_gdf['norm_'+ metric_col] = (metrics_gdf[metric_col] - metrics_gdf['mean_'+ metric_col]) / metrics_gdf['std_'+ metric_col]
    del metrics_gdf['mean_'+ metric_col]
    del metrics_gdf['std_'+ metric_col]
    del metrics_gdf[metric_col]

print(metrics_gdf)
metrics_gdf.info()

#project from 2039 to crs 4326 for leaflet
metrics_gdf = ox.project_gdf(metrics_gdf, to_crs='epsg:4326')
print(metrics_gdf['geometry'])
metrics_gdf.info()

#output segments_cf_poly_metrics_norm_4326.geojson
geojson_fileout = pathout / ('segments_cf_poly_metrics_norm_4326.geojson')
print(geojson_fileout)
metrics_gdf.to_file(geojson_fileout, driver="GeoJSON")

# reformat as js and output
txtfilein = geojson_fileout
textfileout = pathout / ('street_segments25.js')
fw = open(textfileout, 'w', encoding="utf8")
with open(txtfilein, encoding="utf8") as f:
    header = f.readline()
    fw.write('var ss_polys = ' + header)
    #print(header)
    for row in f.readlines():
        #print (row)
        fw.write(row)
fw.close()
print(textfileout)



print("Local current time :", time.asctime( time.localtime(time.time()) ))
