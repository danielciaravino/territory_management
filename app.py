import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import dash_bootstrap_components as dbc
import os
import geojson
import geopandas as gpd
import plotly.graph_objects as go # or plotly.express as px
#fig = go.Figure() # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )

from dash import Dash, dcc, html

#import random
#color = "%06x" % random.randint(0, 0xFFFFFF)

#print (color)
#str("#"+color)
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT_PATH)



with open('myfile_henders.geojson', 'r') as file:
    geojson_data = geojson.load(file)

with open('myfile_shoff.geojson', 'r') as file:
    geojson_data_2 = geojson.load(file)


sample=pd.read_csv(ROOT_PATH+"/hen_shoff.csv")
lat=sample["customer_latitude"]
long=sample["customer_longitude"]
name=sample["customer_1_name"]
territory=sample['sales_territory_emp_name']
sample['terr_cust']="Customer: " + sample["customer_1_name"]+ "<br>" +   "Territory: "+sample["sales_territory_emp_name"]+ "<br>"+"Region: " +sample["sales_region_emp_name"]
ter_name=sample['terr_cust']

colorer=sample['color']

grouped=sample[['sales_territory_id','color']]
grouped=grouped.groupby(['sales_territory_id','color'])

customer_ids_only=sample[['customer_1_name','customer_id']]
customer_ids_only['label']=customer_ids_only['customer_id'].astype(str)+" - "+customer_ids_only['customer_1_name']
customer_ids_only['value']=customer_ids_only['customer_id']
customer_ids_only=pd.DataFrame(customer_ids_only,columns=['label','value'])
customer_ids_only=customer_ids_only.to_dict(orient='records')
#print(grouped.first())

territories=sample['sales_territory_id'].astype(str)+" - "+sample['sales_territory_emp_name']



#print(geojson_data_2)



fig = go.Figure(go.Scattermapbox(
    mode = "markers",
    lon = long, lat = lat,
    marker = {'size': 6, 'color': colorer},
    hoverinfo='text',
    hovertext=ter_name ))

fig.update_layout(
    mapbox = {
        'style': "open-street-map",
        'center': { 'lon': -80.99863, 'lat': 40.36},
        'zoom': 6, 'layers': [{
            'source': geojson_data,
            'type': 'fill','opacity': .9,  'below': "traces", 'color': "#3B51FF"},
            {
            'source': geojson_data_2,#3B51FF
            'type': 'fill','opacity': .9,  'below': "traces", 'color': "#A9DFBF"},
            ],
            },

    margin = {'l':0, 'r':0, 'b':0, 't':0},
    )


card_group = html.Div(
    [

        dbc.Row(
            [
                dbc.Col(dbc.Card("One of two columns")),
                dbc.Col(dbc.Card("One of two columns")),
            ]
        ),
        dbc.Row(dbc.Col(dbc.Card("A single column"))),
    ]
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

#fig.show()



#https://www.youtube.com/watch?v=_pd-TCvJ8bk
#https://dash.plotly.com/dash-ag-grid/enterprise-sidebar

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "12em",
    "padding": "2rem 1rem",
    "backgroundColor": "#2b2b2b",#"rgb(220, 0, 0)",
    "color":"#cfcfcf",
    "fontSize": "12px",
    "font": "roboto",
    "boxShadow": "5px 5px 5px 5px lightgrey"
}

CONTENT_STYLE ={
    "marginLeft": "18rem",
    "marginRight": "2rem",
    "padding": "2rem 1rem"
}

sidebar= html.Div(
    [
    html.H1(f"GFS Territory Management (P.O.C.)",style={"font-size": 20}),
    html.Hr(),
   # html.H3("&", style={"font-size": 16}),
    #html.Hr(),
    dbc.Nav(
        [dbc.NavLink("Territory Summary", href="/", active="exact"),
             dbc.NavLink("Customer Territory Movement", href="/page-one", active="exact"),
             dbc.NavLink("What-if Scenarios", href="/page-two", active="exact")
             ],
            vertical=True,
            pills=True,

        ),
    ],
    style=SIDEBAR_STYLE,
)

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
content=html.Div(id="page-content",style=CONTENT_STYLE)
app.layout=html.Div([dcc.Location(id="url"),sidebar,content])

@app.callback(Output("page-content","children"), [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == f"/":
        return html.Div([html.Div(html.H2("Territory Summary",style={'textAlign': 'center', 'font-size':30,'color':"rgb(220, 0, 0)","font":"roboto"}), id="title"),

                       
                       
    dcc.Graph(figure=fig,config={'scrollZoom':True},style={'height':'60vh','width':'100%'}),
    html.H3('Helpful Information:',style={'textAlign': 'center',"font":"roboto",'font-size':14}),
    html.P('The individual points represent customers, colored by territory. Hover over a customer for more info. The polygons represent sales territories without outliers. Polygons are colored by sales region.',style={'textAlign': 'center',"font":"roboto",'font-size':12}),
    
])
    







  
    
    #html.Col(dcc.Graph(figure=fig,config={'scrollZoom':True},style={'height':'60vh','width':'50%'})),html.Col(dcc.Graph(figure=fig,config={'scrollZoom':True},style={'height':'60vh','width':'50%'}))#,html.Div([#html.Div(html.H2("What-if Planning Scenarios",style={'textAlign': 'center', 'font-size':30,'color':"rgb(220, 0, 0)","font":"roboto"}), id="title"),
            
    # html.H3('Helpful Information:',style={'textAlign': 'center',"font":"roboto",'font-size':20}),
    # html.P('The individual points represent customers, colored by territory. Hover over a customer for more info. The polygons represent sales territories without outliers. Polygons are colored by sales region.',style={'textAlign': 'center',"font":"roboto",'font-size':20}),
    # html.Div(dcc.Checklist(customer_ids_only,id='customer_dropdown'), style = {"overflow-y":"scroll",
    #                "overflow-x":'hidden',
    #                "height": '500px',
    #                'font-size': 18 ,
    #                },id="checklist_holder"),
    #                html.P("To search for a customer, on Windows: press CTRL + F; on Mac: Command + F", style={"font-weight": "italics","font-size":12,"font":"roboto",'textAlign': 'center'}),

    #                html.Col(html.H2("What-if Planning Scenarios",style={'textAlign': 'center', 'font-size':30,'color':"rgb(220, 0, 0)","font":"roboto"}), id="title"),

                       
                       
    # dcc.Graph(figure=fig,config={'scrollZoom':True},style={'height':'60vh','width':'50%'}),
    # html.H3('Helpful Information:',style={'textAlign': 'center',"font":"roboto",'font-size':20}),
    # html.P('The individual points represent customers, colored by territory. Hover over a customer for more info. The polygons represent sales territories without outliers. Polygons are colored by sales region.',style={'textAlign': 'center',"font":"roboto",'font-size':20}),
    # html.Div(dcc.Checklist(customer_ids_only,id='customer_dropdown'), style = {"overflow-y":"scroll",
    #                "overflow-x":'hidden',
    #                "height": '500px',
    #                'font-size': 18 ,
    #                },id="checklist_holder"),
    #                html.P("To search for a customer, on Windows: press CTRL + F; on Mac: Command + F", style={"font-weight": "italics","font-size":12,"font":"roboto",'textAlign': 'center'}),
#])
    












    elif pathname == f"/page-one":
        return html.Div([html.Div(html.H2("Customer Territory Movement",style={'textAlign': 'center', 'font-size':30,'color':"rgb(220, 0, 0)","font":"roboto"}), id="title"),dbc.Row(
            [
                dbc.Col(dbc.Card([
                    html.H2("Prior to Move",style={'textAlign': 'center', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto"}),
                    dcc.Graph(figure=fig,config={'scrollZoom':True},style={'height':'60vh','width':'100%'}),
                    html.H2("Select Customers to Move:",style={'textAlign': 'center', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto"}),
                    html.Div(dcc.Checklist(customer_ids_only,id='customer_dropdown'), style = {"overflow-y":"scroll",
                   "overflow-x":'hidden',
                   "height": '200px',
                   'font-size': 12 ,
                   },id="checklist_holder"),
                   html.P("To search for a customer, on Windows: CTRL + F; on Mac: Command + F", style={"font-weight": "italics","font-size":12,"font":"roboto",'textAlign': 'center'}),
            ])),
                 dbc.Col(dbc.Card([
                    html.H2("After Move",style={'textAlign': 'center', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto"}),
                    dcc.Graph(figure=fig,config={'scrollZoom':True},style={'height':'60vh','width':'100%'}),
                    html.H2("Select Sales Territory to Move to:",style={'textAlign': 'center', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto"}),
                    dcc.Dropdown(territories,value=territories[0],style={'font-size':12}, id='territory-dropdown'),
            ]))
            ]),
            html.Center(html.Button("Submit Changes", id="update_btn",style={'font-size':20,"font":"roboto","font-weight": "bold","padding":"10px"}),style={"padding":"40px"},id="button_holder"),])
    f
    elif pathname == f"/page-two":
        return html.Div([html.Div(html.H2("What-if Planning",style={'textAlign': 'center', 'font-size':30,'color':"rgb(220, 0, 0)","font":"roboto"}), id="title"),dbc.Row(
            [
                dbc.Col(dbc.Card([
                    html.H2("Current State",style={'textAlign': 'center', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto"}),
                    dcc.Graph(figure=fig,config={'scrollZoom':True},style={'height':'60vh','width':'100%'}),
                    html.H2("What-if we increased market share by: x%",style={'textAlign': 'right', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto","padding":"30px"}),
                    html.H2("What-if we converted the following percentage of prospects: x%",style={'textAlign': 'right', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto","padding":"30px"}),
                    html.H2("What-if we increased existing customer sales by: x%",style={'textAlign': 'right', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto","padding":"30px"}),
                    html.H2("What-if we expanded by the following percent in this territory: x%",style={'textAlign': 'right', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto","padding":"30px"}),
                     html.H2("What-if we increased our existing customer menu share by: x%",style={'textAlign': 'right', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto","padding":"30px"}),

                    

                    

            ])),
            #Need to fix:
            #Need to align dropdowns with better logic
                 dbc.Col(dbc.Card([
                    html.H2("What-if",style={'textAlign': 'center', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto"}),
                    dcc.Graph(figure=fig,config={'scrollZoom':True},style={'height':'60vh','width':'100%'}),
                    # dcc.Dropdown(["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"],"0%",style={'textAlign': 'left', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto","padding":"15px"}, id='ms'),
                    # dcc.Dropdown(["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"],"0%",style={'textAlign': 'left', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto","padding":"14px"}, id='ps'),
                    # dcc.Dropdown(["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"],"0%",style={'textAlign': 'left', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto","padding":"14px"}, id='cs'),
                    # dcc.Dropdown(["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"],"0%",style={'textAlign': 'left', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto","padding":"14px"}, id='ts'),
                    # dcc.Dropdown(["0%","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%"],"0%",style={'textAlign': 'left', 'font-size':20,'color':"rgb(220, 0, 0)","font":"roboto","padding":"15px"}, id='ms'),
            ]))
            ])])



server=app.server
# app.layout = 
# 
# html.Div([html.Div(html.H2("Gordon Food Service Territory Management P.O.C.",style={'textAlign': 'center', 'font-size':30,'color':"rgb(220, 0, 0)","font":"roboto"}), id="title"),
                       
                       
#     dcc.Graph(figure=fig,config={'scrollZoom':True},style={'height':'60vh','width':'100%'}),
#     html.H3('Helpful Information:',style={'textAlign': 'center',"font":"roboto",'font-size':20}),
#     html.P('The individual points represent customers, colored by territory. Hover over a customer for more info. The polygons represent sales territories without outliers. Polygons are colored by sales region.',style={'textAlign': 'center',"font":"roboto",'font-size':20}),
#     html.Div(dcc.Checklist(customer_ids_only,id='customer_dropdown'), style = {"overflow-y":"scroll",
#                    "overflow-x":'hidden',
#                    "height": '500px',
#                    'font-size': 18 ,
#                    },id="checklist_holder"),
#                    html.P("To search for a customer, on Windows: press CTRL + F; on Mac: Command + F", style={"font-weight": "italics","font-size":12,"font":"roboto",'textAlign': 'center'}),
# ])

# print("Done")


if __name__ == "__main__":
    app.run(debug=True)
    