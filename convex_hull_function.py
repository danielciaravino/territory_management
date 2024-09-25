import plotly.graph_objects as go
import folium
from folium.plugins import BeautifyIcon
import pandas as pd
import numpy as np
import openrouteservice as ors
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import os
from scipy.spatial import ConvexHull, convex_hull_plot_2d
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from collections import Counter
from sklearn.cluster import KMeans
from datetime import datetime
from matplotlib.path import Path
import numpy as np
from shapely.geometry import MultiPolygon
from shapely.geometry import Polygon
from pandas_geojson.core import MultiPolygon as MP
import geopandas
from geojson import Point, Feature, FeatureCollection, dump

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)

#Lake St. Clair area: b#quxjob_fd3b890_191769c6ae5.csv

#Multiple territories: m#ultiple_territories.csv


#REMEMBER TO ADJUST THE OTHER LINE WAY DOWN IN THE CODE WITH THESE .CSVS (SEARCH AND REPALCE ALL IF CHANGING THE FILE)
#
#all_customers_sample.csv
#all_customers_sample_3_no_0.csv"
sample=pd.read_csv(ROOT_PATH+"/jason_shoffstall_region.csv")

customers_to_test = [3059]#[4159,3077] 

test_sample=sample[sample['sales_territory_id'].isin(customers_to_test)]
test_sample_geos=[test_sample['customer_longitude'],test_sample['customer_latitude']]

#print(test_sample)



#Pass this function a dataframe with at least the following columns:
#[]'sales_territory_id','customer_id','customer_longitude','customer_latitude']

# The function will return the sales territories centroids, with outliers removed, based on each
# respective sales territories convex hull.

def customer_centroids(input_data):
    terr_and_geos=input_data[['sales_territory_id','customer_id','customer_longitude','customer_latitude']]


    groups=terr_and_geos.groupby('sales_territory_id')
    keys=groups.groups.keys()

    territory_centroids=[]
    territory_polygons=[]


    #print(keys)
    for sales_territory in keys:
        #Pull in the customer ids, latitudes, and longitudes for each territory
        longitudes=(groups.get_group(sales_territory)['customer_longitude'])
        latitudes=(groups.get_group(sales_territory)['customer_latitude'])
        customer_id=(groups.get_group(sales_territory)['customer_id'])
        territory_id=(groups.get_group(sales_territory)['sales_territory_id'])

        #Create a data frame with each territory_id, customer and geos
        terr_and_geos=pd.DataFrame([territory_id,customer_id,longitudes,latitudes])
        #Transpose the data for proper rows and columns
        terr_and_geos=terr_and_geos.transpose()

        #Write to cs to verify the file is as expected for each territory
        #terr_and_geos.to_csv(str(sales_territory)+'.csv')

        df = terr_and_geos

        # Calculate Q1 and Q3 for the lat and longs
        Q1 = df.quantile(0.25)
        Q3 = df.quantile(0.75)
        IQR = Q3 - Q1

        #Tukey’s fences = 4 (would be 1.5 if we were calculating outliers here)
        # Using 4 here for even more extreme cases
        #https://aakinshin.net/posts/tukey-outlier-probability/
        lower_bound = Q1 - 4 * IQR
        upper_bound = Q3 + 4 * IQR

        # Filter out the outliers
        outliers_removed_df = df[~((df < lower_bound) | (df > upper_bound)).any(axis=1)]
        print(territory_id)
        
        outliers_removed_df_geos_only=outliers_removed_df[['customer_longitude','customer_latitude']]
        hull=ConvexHull(outliers_removed_df_geos_only)
        cx = np.mean(hull.points[hull.vertices,0])
        cy = np.mean(hull.points[hull.vertices,1])
        distinct_territory=territory_id.iloc[0]
        territory_centroids.append([distinct_territory,cx,cy])
        territory_polygons.append([distinct_territory,hull.points[hull.vertices,0],hull.points[hull.vertices,1],hull,hull.points[hull.vertices]])
        
    #print(territory_centroids)
    territory_centroids=pd.DataFrame(territory_centroids)
    #territory_centroids.to_csv(str(sales_territory)+'_no_out.csv')
    
    


    #Use the below code for timestamped data files
    #territory_centroids.to_csv(str(datetime.now())+'_territory_centroids.csv')
    
    territory_polygons=pd.DataFrame(territory_polygons)
    territory_polygons.columns=['terr','longs','lats','hull','path']
    #territory_polygons2=np.vstack((territory_polygons.iloc[:, 1], territory_polygons.iloc[:, 2])).T
    #print(territory_polygons)
    #territory_polygons.to_csv('_polygons.csv')

    iterator_check=[]

    for index, row in territory_polygons.iterrows():
        x=np.stack((row['longs'],row['lats']), axis=1)
        iterator_check.append(x)

    territory_polygons['coordinates']=iterator_check
    #print(territory_polygons)
    territory_polygons.to_csv('_polygons.csv')
    #print(type(iterator_check))
    #print(type(territory_polygons['coordinates'].tolist()))
    #territory_polygons=pd.DataFrame(territory_polygons)
    #print(territory_polygons)
    return territory_polygons


polys=customer_centroids(sample)

testing=np.array(polys.iloc[:, 5]).tolist()
#testing=tuple(testing)
testing_ids=polys.iloc[:, 0]

# print(polygons_out )
# print(type(polygons_out ))



#This works for shapely

# Convert each polygon from numpy array to a tuple of tuples
polygons = [tuple(map(tuple, poly)) for poly in testing]

# Ensure each polygon is closed by repeating the first point at the end
polygons = [poly + (poly[0],) for poly in polygons]  # Closing the polygons

# Create the MultiPolygon
multi_polygon = MultiPolygon([Polygon(poly) for poly in polygons])

# Output to verify
#print()
x=geopandas.GeoSeries(multi_polygon, index=testing_ids).__geo_interface__
#print(geopandas.GeoSeries(multi_polygon, index=testing_ids).__geo_interface__)

## multipolygon = MP(multi_polygon,
##                             properties=testing_ids
##                     )
## multipolygon




point = Point((-115.81, 37.24))

features = []
features.append(Feature(geometry=point, properties={"country": "Spain"}))

# add more features...
# features.append(...)

feature_collection = FeatureCollection(features)

with open('myfile_shoffstall.geojson', 'w') as f:
   dump(x, f)





#print(type(polys))
#print(polys.iloc[:, 4])
# print("boom")
# a=polys.iloc[0:1, 4]
# a=a.tolist()
# print(a)
# print(type(a))
# quick=Path(a)
# print("quck")
# print(quick)
# print(quick.contains_point((1,2)))
# print("bang")
#polys['path'].contains_point((1,2))






        #reset_index_table=outliers_removed_df_geos_only.reset_index()
        ##outliers_removed_df_geos_only=outliers_removed_df_geos_only.tolist()
        #vertices_list=outliers_removed_df_geos_only[hull.vertices].to_list()
        #print(reset_index_table)
        #print("second")
        #print("clear")
        #print(reset_index_table.iloc[hull.vertices, :])


    #territory_centroids=pd.DataFrame(territory_centroids)

    #territory_centroids.to_csv(str(datetime.now())+'_territory_centroids.csv')









#Run the below line on the sample for testing
# customer_centroids(sample)
    








# multipolygon = MP(geometry=[[[[-10.0, 10.0], [-10.0, -10.0], [10.0, -10.0], [10.0, 10.0], [-10.0, 10.0]]],[[[-20.0, 20.0], [-20.0, -20.0], [20.0, -20.0], [20.0, 20.0],[-20.0, 20.0]]]]
#                     ,properties={'ID':1}
#                     )
# print(multipolygon)






