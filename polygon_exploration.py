import plotly.graph_objects as go
import folium
from folium.plugins import BeautifyIcon
import pandas as pd
import numpy as np
import openrouteservice as ors
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import os



fig = go.Figure(go.Scattermapbox(
    mode = "markers",
    lon = [-86.71882985714285], lat = [34.66257514285714],
    marker = {'size': 20, 'color': ["cyan"]}))

fig.update_layout(
    mapbox = {
        'style': "open-street-map",
        'center': { 'lon': -86.71882985714285, 'lat': 34.66257514285714},
        'zoom': 12, 'layers': [{
            'source': {
                'type': "FeatureCollection",
                'features': [{
                    'type': "Feature",
                    'geometry': {
                        'type': "MultiPolygon",
                        'coordinates': [[[[-86.920145, 34.541112], [-86.688281, 34.495338], [-86.540088, 34.643883], [-86.627419, 34.726417], [-86.680999, 34.746218], [-86.714229, 34.755443], [-86.860648, 34.729615]]]]
                    }
                }]
            },
            'type': 'fill', 'opacity': 0.3, 'below': "traces", 'color': "royalblue"}]},
    margin = {'l':0, 'r':0, 'b':0, 't':0})

fig.show()
