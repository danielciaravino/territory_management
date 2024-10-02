import plotly.graph_objects as go
import folium
from folium.plugins import BeautifyIcon
import pandas as pd
import numpy as np
import openrouteservice as ors
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import os
import geojson
import geopandas as gpd
#import random
#color = "%06x" % random.randint(0, 0xFFFFFF)

#print (color)
#str("#"+color)
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)



with open('myfile_henderson.geojson', 'r') as file:
    geojson_data = geojson.load(file)

with open('myfile_shoff.geojson', 'r') as file:
    geojson_data_2 = geojson.load(file)


sample=pd.read_csv(ROOT_PATH+"/hen_shoff.csv")
lat=sample["customer_latitude"]
long=sample["customer_longitude"]
name=sample["customer_1_name"]
territory=sample['sales_territory_emp_name']
sample['terr_cust']="Customer: " + sample["customer_1_name"]+" Territory: "+sample["sales_territory_emp_name"]
ter_name=sample['terr_cust']

colorer=sample['color']

grouped=sample[['sales_territory_id','color']]
grouped=grouped.groupby(['sales_territory_id','color'])

#print(grouped.first())




#print(geojson_data_2)



fig = go.Figure(go.Scattermapbox(
    mode = "markers",
    lon = long, lat = lat,
    marker = {'size': 8, 'color': colorer},
    hovertext=ter_name))

fig.update_layout(
    mapbox = {
        'style': "open-street-map",
        'center': { 'lon': -80.629863, 'lat': 39.106629},
        'zoom': 6, 'layers': [{
            'source': geojson_data,
            'type': 'fill','opacity': 0.9,  'below': "traces", 'color': "#E6B0AA"},
            {
            'source': geojson_data_2,
            'type': 'fill','opacity': 0.9,  'below': "traces", 'color': "#A9DFBF"},
            ],
            },

    margin = {'l':0, 'r':0, 'b':0, 't':0},
    )




# fig.update_layout(
#         mapbox = {
#         'style': "open-street-map",
#         'center': { 'lon': -86.71882985714285, 'lat': 34.66257514285714},
#         'zoom': 12, 'layers': [{
#             'source': {
#                 'type': "FeatureCollection",
#                 'features': [{
#                     'type': "Feature",
#                     'geometry': {
#                         'type': "MultiPolygon",
#                         'coordinates': [[[[-88.920145, 34.541112], [-88.688281, 34.495338], [-88.540088, 34.643883], [-88.627419, 34.726417], [-88.680999, 34.746218], [-88.714229, 34.755443], [-88.860648, 34.729615]]]]
#                     }
#                 }]
#             },
#             'type': 'fill', 'opacity': 0.3, 'below': "traces", 'color': "red"}]},
#     margin = {'l':0, 'r':0, 'b':0, 't':0})

fig.show()