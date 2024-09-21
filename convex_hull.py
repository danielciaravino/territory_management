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

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)

#Lake St. Clair area:bquxjob_fd3b890_191769c6ae5.csv
#REMEMBER TO ADJUST THE OTHER LINE WITH THESE .CSVS
sample=pd.read_csv(ROOT_PATH+"/bquxjob_fd3b890_191769c6ae5.csv")

#Miami:
#/Users/dannyciaravino/Desktop/Workspace/territory_management/bquxjob_fd3b890_191769c6ae5.csv



geos_only=sample[['customer_longitude','customer_latitude']]
#geos_only=geos_only.to_numpy()

print(geos_only)

# Convert to DataFrame for easier manipulation
df = geos_only

# Calculate Q1 and Q3 for both dimensions
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1


#Tukey’s fences = 4 (would be 1.5 if we were calculating outliers here)
# Using 4 here for even more extreme cases
#https://aakinshin.net/posts/tukey-outlier-probability/
# Define outlier bounds
lower_bound = Q1 - 4 * IQR
upper_bound = Q3 + 4 * IQR

# Filter out the outliers
outliers_removed_df = df[~((df < lower_bound) | (df > upper_bound)).any(axis=1)]

print(outliers_removed_df)




geos_only_concat=geos_only
geos_only_concat['concat']=(geos_only.iloc[:, 0].astype(str)+"_"+geos_only.iloc[:, 1].astype(str))
geos_only_concat.columns=['long','lat','concat']
core_points=pd.DataFrame((outliers_removed_df.iloc[:, 0].astype(str)+"_"+outliers_removed_df.iloc[:, 1].astype(str)))
core_points.columns=['concat']

outliers_removed=geos_only_concat[~geos_only_concat.concat.isin(core_points.concat)]
print("full_list")
print(geos_only_concat)
print("outliers_removed")
print(core_points)
print("all outliers")
print(outliers_removed)








plt.scatter(outliers_removed.iloc[:, 0],outliers_removed.iloc[:, 1],color='red')
plt.scatter(outliers_removed_df.iloc[:, 0],outliers_removed_df.iloc[:, 1],color='black')
plt.show()

# plt.show()


# hull=ConvexHull(geos_only)



# plt.plot(geos_only[:,0], geos_only[:,1], 'o')
# for simplex in hull.simplices:
#     plt.plot(geos_only[simplex, 0], geos_only[simplex, 1], 'k-')

# plt.plot(geos_only[hull.vertices,0], geos_only[hull.vertices,1], 'r--', lw=2)
# plt.plot(geos_only[hull.vertices[0],0], geos_only[hull.vertices[0],1], 'ro')
# plt.show()

# #print("divide")
# #print(geos_only[hull.vertices])
# as_list=geos_only[hull.vertices].tolist()
# #print(as_list)

# cx = np.mean(hull.points[hull.vertices,0])
# cy = np.mean(hull.points[hull.vertices,1])

# print("Centroid")
# print (cx)
# print (cy)





# rng = np.random.default_rng()
# points = rng.random((30, 2))   # 30 random points in 2-D
# print(points)
# # hull = ConvexHull(points)
# # plt.plot(points[:,0], points[:,1], 'o')
# # for simplex in hull.simplices:
# #     plt.plot(points[simplex, 0], points[simplex, 1], 'k-')
# print(type(geos_only))
# print(type(points))

                  
                
# plt.plot(points[hull.vertices,0], points[hull.vertices,1], 'r--', lw=2)
# plt.plot(points[hull.vertices[0],0], points[hull.vertices[0],1], 'ro')
# plt.show()





# def geos_to_hull(input_data):

#     #Grab only the latitude and longitude values
#     geos_only=sample[['customer_longitude','customer_latitude']]
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
        


        # #DBSCAN method - not going to be used
# model=DBSCAN(eps=0.2,min_samples=5).fit(geos_only)

# outlier_df=pd.DataFrame(geos_only)

# # Printing total number of values for each label
# print(Counter(model.labels_))

# # Printing DataFrame being considered as Outliers -1
# print(outlier_df[model.labels_ == -1])

# # Printing and Indicating which type of object outlier_df is
# print(type(outlier_df))

# # Exporting this DataFrame to CSV
# #outlier_df[model.labels_ == -1].to_csv("dbscan-outliers.csv")
# #print(outlier_df)

# outliers_only=outlier_df[model.labels_ == -1]

# geos_only_concat=geos_only
# geos_only_concat['concat']=(geos_only.iloc[:, 0].astype(str)+"_"+geos_only.iloc[:, 1].astype(str))
# geos_only_concat.columns=['long','lat','concat']
# outliers_only_concat=pd.DataFrame((outliers_only.iloc[:, 0].astype(str)+"_"+outliers_only.iloc[:, 1].astype(str)))
# outliers_only_concat.columns=['concat']

# outliers_removed=geos_only_concat[~geos_only_concat.concat.isin(outliers_only_concat.concat)]
# print("full_list")
# print(geos_only_concat)
# print("listofoutliers")
# print(outliers_only_concat)
# print("no outliers")
# print(outliers_removed)