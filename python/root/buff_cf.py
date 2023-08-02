#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
print('-----------------  --------------------------')

import time
from pathlib import Path
import pandas as pd
import numpy as np
import geopandas as gpd

cwd = Path.cwd()
pathin = cwd.parent / 'data'
pathout = cwd.parent / 'processed'

print("Local current time :", time.asctime( time.localtime(time.time()) ))
#_________________________________
#
#input cf file
infile = 'TA_CommFront_1_2_w_streetnames_snapped.geojson'
cf_gdf = gpd.read_file(pathin / infile, encoding='utf-8')
print(cf_gdf)

cf_buff5_gdf = cf_gdf.copy()
cf_buff5_gdf.geometry = cf_gdf.buffer(5)
print(cf_buff5_gdf)

cf_buff25_gdf = cf_gdf.copy()
cf_buff25_gdf.geometry = cf_gdf.buffer(25)
print(cf_buff25_gdf)

cf_buff100_gdf = cf_gdf.copy()
cf_buff100_gdf.geometry = cf_gdf.buffer(100)
print(cf_buff100_gdf)

geojson_fileout = pathout / ('cf_1_2_buff5.geojson')
#cf_buff5_gdf.set_crs(epsg=2039, inplace=True)
print(geojson_fileout)
cf_buff5_gdf.to_file(geojson_fileout, driver="GeoJSON")

geojson_fileout = pathout / ('cf_1_2_buff25.geojson')
#cf_buff25_gdf.set_crs(epsg=2039, inplace=True)
print(geojson_fileout)
cf_buff25_gdf.to_file(geojson_fileout, driver="GeoJSON")

geojson_fileout = pathout / ('cf_1_2_buff100.geojson')
#cf_buff100_gdf.set_crs(epsg=2039, inplace=True)
print(geojson_fileout)
cf_buff100_gdf.to_file(geojson_fileout, driver="GeoJSON")

print("Local current time :", time.asctime( time.localtime(time.time()) ))
