#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# snap supply and demand points to cf up to 100m
# see - https://gis.stackexchange.com/questions/306838/snap-points-shapefile-to-line-shapefile-using-shapely
#
print('-----------------  --------------------------')

import time
from pathlib import Path
import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas.tools import sjoin

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

#input supply file
infile = 'Trafic Signs Points prika ve teina v6s_ap.geojson'
supply_gdf = gpd.read_file(pathin / infile, encoding='utf-8')
#del supply_gdf['statusdate']
#del supply_gdf['lastupdate']
print(supply_gdf)

#input demand file
infile = 'tlv_businesses_w_logistics_filtered.csv'
demand_gdf = gpd.read_file(pathin / infile, encoding='utf-8')
#print(demand_gdf.x_coord, demand_gdf.y_coord)
demand_gdf.geometry = gpd.points_from_xy(demand_gdf.x_coord, demand_gdf.y_coord)
print(demand_gdf)

#=============================================

#snap supply points to cf line segments
shply_line = cf_gdf.geometry.unary_union
buff = shply_line.buffer(100)
buff = gpd.GeoDataFrame(geometry=[buff])
point = supply_gdf.copy()
pointInPolys = sjoin(point,buff, how='left')
print(pointInPolys)
#pointInPolys.info()
point100 = pointInPolys.dropna()
#point100.info()
print(point100)
result2 =  point100.copy()
result2['geometry'] = result2.apply(lambda row:    shply_line.interpolate(shply_line.project( row.geometry)), axis=1)
print(result2)

#output snapped supply file
geojson_fileout = pathout / ('Trafic Signs Points prika ve teina v6s_ap snap100 cf.geojson')
print(geojson_fileout)
result2.to_file(geojson_fileout, driver="GeoJSON")

#=============================================

#snap demand points to cf line segments
shply_line = cf_gdf.geometry.unary_union
buff = shply_line.buffer(100)
buff = gpd.GeoDataFrame(geometry=[buff])
point = demand_gdf.copy()
pointInPolys = sjoin(point,buff, how='left')
print(pointInPolys)
#pointInPolys.info()
point100 = pointInPolys.dropna()
#point100.info()
print(point100)
result2 =  point100.copy()
result2['geometry'] = result2.apply(lambda row:    shply_line.interpolate(shply_line.project( row.geometry)), axis=1)
print(result2)

#output snapped demand file
geojson_fileout = pathout / ('tlv_businesses_w_logistics_filtered_snap100_cf.geojson')
print(geojson_fileout)
result2.set_crs(epsg=2039, inplace=True)
result2.to_file(geojson_fileout, driver="GeoJSON")


print("Local current time :", time.asctime( time.localtime(time.time()) ))
