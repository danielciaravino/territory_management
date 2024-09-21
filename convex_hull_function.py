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

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)

#Lake St. Clair area: b#quxjob_fd3b890_191769c6ae5.csv

#Multiple territories: m#ultiple_territories.csv


#REMEMBER TO ADJUST THE OTHER LINE WAY DOWN IN THE CODE WITH THESE .CSVS (SEARCH AND REPALCE ALL IF CHANGING THE FILE)
sample=pd.read_csv(ROOT_PATH+"/multiple_territories.csv")



#Pass this function a dataframe with at least the following columns:
#[]'sales_territory_id','customer_id','customer_longitude','customer_latitude']

# The function will return the sales territories centroids, with outliers removed, based on each
# respective sales territories convex hull.

def customer_centroids(input_data):
    terr_and_geos=input_data[['sales_territory_id','customer_id','customer_longitude','customer_latitude']]


    groups=terr_and_geos.groupby('sales_territory_id')
    keys=groups.groups.keys()

    territory_centroids=[]


    #print(keys)
    for sales_territory in keys:
        #Pull in the customer ids, latitudes, and longitudes for each territory
        longitudes=(groups.get_group(sales_territory)['customer_longitude'])
        latitudes=(groups.get_group(sales_territory)['customer_latitude'])
        customer_id=(groups.get_group(sales_territory)['customer_id'])
        territory_id=(groups.get_group(sales_territory)['sales_territory_id'])
        terr_and_geos=pd.DataFrame([territory_id,customer_id,longitudes,latitudes])
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
        outliers_removed_df.to_csv(str(sales_territory)+'_no_out.csv')
        outliers_removed_df_geos_only=outliers_removed_df[['customer_longitude','customer_latitude']]
        hull=ConvexHull(outliers_removed_df_geos_only)
        cx = np.mean(hull.points[hull.vertices,0])
        cy = np.mean(hull.points[hull.vertices,1])
        distinct_territory=territory_id.iloc[0]
        territory_centroids.append([distinct_territory,cx,cy])
        ##outliers_removed_df_geos_only=outliers_removed_df_geos_only.tolist()

    territory_centroids=pd.DataFrame(territory_centroids)

    territory_centroids.to_csv(str(datetime.now())+'_territory_centroids.csv')


customer_centroids(sample)
    #

    # plt.plot(outliers_removed_df_geos_only[:,0], outliers_removed_df_geos_only[:,1], 'o')
    # for simplex in hull.simplices:
    #     plt.plot(outliers_removed_df_geos_only[simplex, 0], outliers_removed_df_geos_only[simplex, 1], 'k-')

    # plt.plot(outliers_removed_df_geos_only[hull.vertices,0], outliers_removed_df_geos_only[hull.vertices,1], 'r--', lw=2)
    # plt.plot(outliers_removed_df_geos_only[hull.vertices[0],0], outliers_removed_df_geos_only[hull.vertices[0],1], 'ro')
    # plt.show()









#     #Grab only the latitude and longitude values
#     geos_only=input_data['sales_territory_id','customer_longitude','customer_latitude']
#     geos_only=geos_only.to_numpy()

#     #Create and plot a convex hull based on these points
#     hull=ConvexHull(geos_only)

#     plt.plot(geos_only[:,0], geos_only[:,1], 'o')
#     for simplex in hull.simplices:
#         plt.plot(geos_only[simplex, 0], geos_only[simplex, 1], 'k-')

#     plt.plot(geos_only[hull.vertices,0], geos_only[hull.vertices,1], 'r--', lw=2)
#     plt.plot(geos_only[hull.vertices[0],0], geos_only[hull.vertices[0],1], 'ro')
    
#     #Calculate the centroid for each hull
#     cx = np.mean(hull.points[hull.vertices,0])
#     cy = np.mean(hull.points[hull.vertices,1])

#     #List out the verteces
#     verteces_list=geos_only[hull.vertices].tolist()

#     #Return the verteces












# geos_only=sample[['customer_longitude','customer_latitude']]
# #geos_only=geos_only.to_numpy()

# print(geos_only)

# # Convert to DataFrame for easier manipulation
# df = geos_only

# # Calculate Q1 and Q3 for both dimensions
# Q1 = df.quantile(0.25)
# Q3 = df.quantile(0.75)
# IQR = Q3 - Q1


# #Tukey’s fences = 4 (would be 1.5 if we were calculating outliers here)
# # Using 4 here for even more extreme cases
# #https://aakinshin.net/posts/tukey-outlier-probability/
# # Define outlier bounds
# lower_bound = Q1 - 4 * IQR
# upper_bound = Q3 + 4 * IQR

# # Filter out the outliers
# outliers_removed_df = df[~((df < lower_bound) | (df > upper_bound)).any(axis=1)]

# print(outliers_removed_df)




# geos_only_concat=geos_only
# geos_only_concat['concat']=(geos_only.iloc[:, 0].astype(str)+"_"+geos_only.iloc[:, 1].astype(str))
# geos_only_concat.columns=['long','lat','concat']
# core_points=pd.DataFrame((outliers_removed_df.iloc[:, 0].astype(str)+"_"+outliers_removed_df.iloc[:, 1].astype(str)))
# core_points.columns=['concat']

# outliers_removed=geos_only_concat[~geos_only_concat.concat.isin(core_points.concat)]
# print("full_list")
# print(geos_only_concat)
# print("outliers_removed")
# print(core_points)
# print("all outliers")
# print(outliers_removed)



# plt.scatter(outliers_removed.iloc[:, 0],outliers_removed.iloc[:, 1],color='red')
# plt.scatter(outliers_removed_df.iloc[:, 0],outliers_removed_df.iloc[:, 1],color='black')
# #plt.show()