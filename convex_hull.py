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

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)

#Lake St. Clair area:bquxjob_fd3b890_191769c6ae5.csv
#REMEMBER TO ADJUST THE OTHER LINE WITH THESE .CSVS
sample=pd.read_csv(ROOT_PATH+"/bquxjob_289ad542_19170a4884f.csv")

#Miami:
#/Users/dannyciaravino/Desktop/Workspace/territory_management/bquxjob_fd3b890_191769c6ae5.csv

geos_only=sample[['customer_longitude','customer_latitude']]
geos_only=geos_only.to_numpy()

print(geos_only) #[:,0])




hull=ConvexHull(geos_only)



plt.plot(geos_only[:,0], geos_only[:,1], 'o')
for simplex in hull.simplices:
    plt.plot(geos_only[simplex, 0], geos_only[simplex, 1], 'k-')

plt.plot(geos_only[hull.vertices,0], geos_only[hull.vertices,1], 'r--', lw=2)
plt.plot(geos_only[hull.vertices[0],0], geos_only[hull.vertices[0],1], 'ro')
#plt.show()

#print("divide")
#print(geos_only[hull.vertices])
as_list=geos_only[hull.vertices].tolist()
#print(as_list)

cx = np.mean(hull.points[hull.vertices,0])
cy = np.mean(hull.points[hull.vertices,1])

print (cx)
print (cy)





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