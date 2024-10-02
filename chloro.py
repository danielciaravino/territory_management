import plotly.express as px
import os
import geojson
import pandas as pd

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)


df = pd.read_csv(ROOT_PATH+"/all_customers_sample_3_no_0.csv")
with open('myfile.geojson', 'r') as file:
    geojson_ = geojson.load(file)

fig = px.choropleth_map(df, geojson=geojson,
                           center={"lat": 45.5517, "lon": -73.7073},
                           map_style="carto-positron", zoom=9)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()