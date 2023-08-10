#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# segments_cf_count_points_in_poly.py
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
pathproc = cwd.parent / 'processed'
pathout = cwd.parent / 'processed'

print("Local current time :", time.asctime( time.localtime(time.time()) ))
#_________________________________
#

#input cf buff files
infile = 'cf_1_2_buff5.geojson'
cf_buff5_gdf = gpd.read_file(pathproc / infile, encoding='utf-8')
#print(cf_buff5_gdf)
infile = 'cf_1_2_buff25.geojson'
cf_buff25_gdf = gpd.read_file(pathproc / infile, encoding='utf-8')
#print(cf_buff25_gdf)
infile = 'cf_1_2_buff100.geojson'
cf_buff100_gdf = gpd.read_file(pathproc / infile, encoding='utf-8')
#print(cf_buff100_gdf)

#input supply file
infile = 'Trafic Signs Points prika ve teina v6s_ap.geojson'
supply_gdf = gpd.read_file(pathin / infile, encoding='utf-8')
#del supply_gdf['statusdate']
#del supply_gdf['lastupdate']
#print(supply_gdf)

#input supply snapped file
infile = 'Trafic Signs Points prika ve teina v5s_ap snap100 cf.geojson'
supply_snap_gdf = gpd.read_file(pathproc / infile, encoding='utf-8')
#del supply_snap_gdf['statusdate']
#del supply_snap_gdf['lastupdate']
#print(supply_snap_gdf)

#input demand file
infile = 'tlv_businesses_w_logistics_filtered.csv'
demand_gdf = gpd.read_file(pathin / infile, encoding='utf-8')
demand_gdf.set_crs(epsg=2039, inplace=True)
demand_gdf.rename(columns={'תדירות הפצות שבועית': 'weekly_delivery_freq'}, inplace=True)
demand_gdf['weekly_delivery_freq'] = demand_gdf['weekly_delivery_freq'].astype(float)
#print(demand_gdf.x_coord, demand_gdf.y_coord)
demand_gdf.geometry = gpd.points_from_xy(demand_gdf.x_coord, demand_gdf.y_coord)
#print(demand_gdf)
#demand_gdf.info()

#input demand snaped file
infile = 'tlv_businesses_w_logistics_filtered_snap100_cf.geojson'
demand_snap_gdf = gpd.read_file(pathproc / infile, encoding='utf-8')
demand_snap_gdf.rename(columns={'תדירות הפצות שבועית': 'weekly_delivery_freq'}, inplace=True)
demand_snap_gdf['weekly_delivery_freq'] = demand_snap_gdf['weekly_delivery_freq'].astype(float)

#=============================================

# sum supply and demand points in cf segments buff 100

polygons_contains = sjoin(cf_buff100_gdf[['id','geometry']], supply_gdf[['_hours_x_meters','geometry']], predicate='contains', how='left')
polygons_contains = polygons_contains.dropna()
#print (polygons_contains)
#polygons_contains.info()
#supply_in_cf_buff100_gdf = polygons_contains.groupby(['id'])['_hours_x_meters'].aggregate(['max','sum', 'count'])
supply_in_cf_buff100_gdf = polygons_contains.groupby(['id'])['_hours_x_meters'].aggregate(['sum'])
supply_in_cf_buff100_gdf.rename(columns={'sum': 'sum_hours_x_meters_buff100'}, inplace=True)
#print (supply_in_cf_buff100_gdf)
supply_in_cf_buff100_gdf = pd.merge(supply_in_cf_buff100_gdf, cf_buff100_gdf[['id','geometry']], on='id')
print (supply_in_cf_buff100_gdf)

polygons_contains = sjoin(cf_buff100_gdf[['id','geometry']], demand_gdf[['weekly_delivery_freq','geometry']], predicate='contains', how='left')
polygons_contains = polygons_contains.dropna()
#print (polygons_contains)
#polygons_contains.info()
#demand_in_cf_buff100_gdf = polygons_contains.groupby(['id'])['weekly_delivery_freq'].aggregate(['max','sum', 'count'])
demand_in_cf_buff100_gdf = polygons_contains.groupby(['id'])['weekly_delivery_freq'].aggregate(['sum'])
demand_in_cf_buff100_gdf.rename(columns={'sum': 'sum_weekly_delivery_freq_buff100'}, inplace=True)
#print (demand_in_cf_buff100_gdf)
demand_in_cf_buff100_gdf = pd.merge(demand_in_cf_buff100_gdf, cf_buff100_gdf[['id','geometry']], on='id')
print (demand_in_cf_buff100_gdf)

# sum snapped supply and snapped demand points in cf segments buff 5

polygons_contains = sjoin(cf_buff5_gdf[['id','geometry']], supply_snap_gdf[['_hours_x_meters','geometry']], predicate='contains', how='left')
polygons_contains = polygons_contains.dropna()
#print (polygons_contains)
#polygons_contains.info()
#supply_in_cf_buff5_gdf = polygons_contains.groupby(['id'])['_hours_x_meters'].aggregate(['max','sum', 'count'])
supply_in_cf_buff5_gdf = polygons_contains.groupby(['id'])['_hours_x_meters'].aggregate(['sum'])
supply_in_cf_buff5_gdf.rename(columns={'sum': 'sum_hours_x_meters_snap100'}, inplace=True)
#print (supply_in_cf_buff5_gdf)
supply_in_cf_buff5_gdf = pd.merge(supply_in_cf_buff5_gdf, cf_buff5_gdf[['id','geometry']], on='id')
print (supply_in_cf_buff5_gdf)

polygons_contains = sjoin(cf_buff5_gdf[['id','geometry']], demand_snap_gdf[['weekly_delivery_freq','geometry']], predicate='contains', how='left')
polygons_contains = polygons_contains.dropna()
#print (polygons_contains)
#polygons_contains.info()
#demand_in_cf_buff5_gdf = polygons_contains.groupby(['id'])['weekly_delivery_freq'].aggregate(['max','sum', 'count'])
demand_in_cf_buff5_gdf = polygons_contains.groupby(['id'])['weekly_delivery_freq'].aggregate(['sum'])
demand_in_cf_buff5_gdf.rename(columns={'sum': 'sum_weekly_delivery_freq_snap100'}, inplace=True)
#print (demand_in_cf_buff5_gdf)
demand_in_cf_buff5_gdf = pd.merge(demand_in_cf_buff5_gdf, cf_buff5_gdf[['id','geometry']], on='id')
print (demand_in_cf_buff5_gdf)
#demand_in_cf_buff5_gdf.info()
"""
#output 
geojson_fileout = pathout / ('cf_buff5_gdf.geojson')
print(geojson_fileout)
cf_buff5_gdf.to_file(geojson_fileout, driver="GeoJSON")

#output 
geojson_fileout = pathout / ('supply_snap_gdf.geojson')
print(geojson_fileout)
supply_snap_gdf[['_hours_x_meters','geometry']].to_file(geojson_fileout, driver="GeoJSON")

#output 
geojson_fileout = pathout / ('demand_snap_gdf.geojson')
print(geojson_fileout)
demand_snap_gdf[['weekly_delivery_freq','geometry']].to_file(geojson_fileout, driver="GeoJSON")
"""

# collect sum point in poly metrics

segments_cf_poly_metrics_gdf = cf_buff25_gdf.copy()

segments_cf_poly_metrics_gdf = pd.merge(segments_cf_poly_metrics_gdf, supply_in_cf_buff100_gdf[['id','sum_hours_x_meters_buff100']], on='id', how='left')
segments_cf_poly_metrics_gdf['sum_hours_x_meters_buff100'] = segments_cf_poly_metrics_gdf['sum_hours_x_meters_buff100'].fillna(0.0)
print(segments_cf_poly_metrics_gdf)
segments_cf_poly_metrics_gdf.info()

segments_cf_poly_metrics_gdf = pd.merge(segments_cf_poly_metrics_gdf, demand_in_cf_buff100_gdf[['id','sum_weekly_delivery_freq_buff100']], on='id', how='left')
segments_cf_poly_metrics_gdf['sum_weekly_delivery_freq_buff100'] = segments_cf_poly_metrics_gdf['sum_weekly_delivery_freq_buff100'].fillna(0.0)
print(segments_cf_poly_metrics_gdf)
segments_cf_poly_metrics_gdf.info()

segments_cf_poly_metrics_gdf = pd.merge(segments_cf_poly_metrics_gdf, supply_in_cf_buff5_gdf[['id','sum_hours_x_meters_snap100']], on='id', how='left')
segments_cf_poly_metrics_gdf['sum_hours_x_meters_snap100'] = segments_cf_poly_metrics_gdf['sum_hours_x_meters_snap100'].fillna(0.0)
print(segments_cf_poly_metrics_gdf)
segments_cf_poly_metrics_gdf.info()

segments_cf_poly_metrics_gdf = pd.merge(segments_cf_poly_metrics_gdf, demand_in_cf_buff5_gdf[['id','sum_weekly_delivery_freq_snap100']], on='id', how='left')
segments_cf_poly_metrics_gdf['sum_weekly_delivery_freq_snap100'] = segments_cf_poly_metrics_gdf['sum_weekly_delivery_freq_snap100'].fillna(0.0)
print(segments_cf_poly_metrics_gdf)
segments_cf_poly_metrics_gdf.info()

# collect derived metrics

def min_per_delivery_buff100(row):
    s = row['sum_hours_x_meters_buff100']
    d = row['sum_weekly_delivery_freq_buff100']
    if d > 0 : # demand > 0, supply >= 0
        return (60.0*s/6.0) / d
    elif s == 0: # demand == 0, supply == 0
        print(s, d, -2)
        return -2
    else: # demand == 0, supply > 0
        print(s, d, -1)
        return -1
segments_cf_poly_metrics_gdf['min_per_delivery_buff100'] = segments_cf_poly_metrics_gdf.apply(min_per_delivery_buff100, axis=1)

def min_per_delivery_snap100(row):
    s = row['sum_hours_x_meters_snap100']
    d = row['sum_weekly_delivery_freq_snap100']
    if d > 0 : # demand > 0, supply >= 0
        return (60.0*s/6.0) / d
    elif s == 0: # demand == 0, supply == 0
        print(s, d, -2)
        return -2
    else: # demand == 0, supply > 0
        print(s, d, -1)
        return -1
segments_cf_poly_metrics_gdf['min_per_delivery_snap100'] = segments_cf_poly_metrics_gdf.apply(min_per_delivery_snap100, axis=1)

def d2s_buff100(row):
    s = row['sum_hours_x_meters_buff100']*3/6 # assume 6meters and 20min to get weekly delevery supply
    d = row['sum_weekly_delivery_freq_buff100']
    if s > 0 : # demand >= 0, supply > 0
        return  d / s
    elif d == 0: # demand == 0, supply == 0
        print(s, d, -2)
        return -2
    else: # demand > 0, supply == 0
        print(s, d, -1)
        return -1
segments_cf_poly_metrics_gdf['d2s_buff100'] = segments_cf_poly_metrics_gdf.apply(d2s_buff100, axis=1)

def d2s_snap100(row):
    s = row['sum_hours_x_meters_snap100']*3/6 # assume 6meters and 20min to get weekly delevery supply
    d = row['sum_weekly_delivery_freq_snap100']
    if s > 0 : # demand >= 0, supply > 0
        return  d / s
    elif d == 0: # demand == 0, supply == 0
        print(s, d, -2)
        return -2
    else: # demand > 0, supply == 0
        print(s, d, -1)
        return -1
segments_cf_poly_metrics_gdf['d2s_snap100'] = segments_cf_poly_metrics_gdf.apply(d2s_snap100, axis=1)

"""
segments_cf_poly_metrics_gdf['min_per_delivery_buff100'] = (60.0*segments_cf_poly_metrics_gdf['sum_hours_x_meters_buff100']/6.0)/segments_cf_poly_metrics_gdf['sum_weekly_delivery_freq_buff100'] 
segments_cf_poly_metrics_gdf['min_per_delivery_buff100'] = segments_cf_poly_metrics_gdf['min_per_delivery_buff100'].fillna(0.0)
segments_cf_poly_metrics_gdf['min_per_delivery_snap100'] = (60.0*segments_cf_poly_metrics_gdf['sum_hours_x_meters_snap100']/6.0)/segments_cf_poly_metrics_gdf['sum_weekly_delivery_freq_snap100'] 
segments_cf_poly_metrics_gdf['min_per_delivery_snap100'] = segments_cf_poly_metrics_gdf['min_per_delivery_snap100'].fillna(0.0)

segments_cf_poly_metrics_gdf.replace([np.inf, -np.inf], 0, inplace=True)
"""
print(segments_cf_poly_metrics_gdf)
segments_cf_poly_metrics_gdf.info()

#output 
geojson_fileout = pathout / ('segments_cf_poly_metrics.geojson')
print(geojson_fileout)
segments_cf_poly_metrics_gdf.to_file(geojson_fileout, driver="GeoJSON")

print("Local current time :", time.asctime( time.localtime(time.time()) ))
