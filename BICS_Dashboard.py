# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 15:01:27 2022

@author: Emelia

Credit to these two youtube videos for instructing some elements of this code:
    https://www.youtube.com/watch?v=aJmaw3QKMvk
    https://www.youtube.com/watch?v=hSPmj7mK6ng
GeoJson data from:
    https://www.kaggle.com/datasets/dorianlazar/uk-regions-geojson
"""

#install pandas
import json
from geojson_rewind import rewind
import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
app = dash.Dash(__name__)

#Regressions data frame
dfRegressions = pd.read_csv("regression_data.csv")
dfRegressions.columns = ['Industry/Size Band', 'Wave','Stock levels are higher than normal (%)',
                    'Stock levels are lower than normal (%)', 'Prices increased more than normal (%)',
                    'Prices decreased more than normal (%)', 'Demand increased more than normal (%)',
                    'Demand did not increase (%)']

mark_values = {11: '11', 13: '13', 15: '15', 17: '17',
               19: '19', 21: '21', 23: '23', 25: '25',
               27: '27', 29: '29', 31: '31', 42: '42',
               44: '44', 46: '46', 48: '48', 50: '50'}


#Get data frames for the industry/size tab and questions to dislpay.
questionDict={}
dfDict={}

dfDict['Trading Status TS1 (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Trading Status TS1 (WTD)', header = 1)
questionDict['Trading Status TS1 (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Trading Status TS1 (WTD)', nrows=0).columns[0]
dfDict['Supply Chains TS (WTD) (1)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Supply Chains TS (WTD) (1)', header = 1)
questionDict['Supply Chains TS (WTD) (1)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Supply Chains TS (WTD) (1)', nrows=0).columns[0]
dfDict['Transition Costs TS (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Transition Costs TS (WTD)', header = 1)
questionDict['Transition Costs TS (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Transition Costs TS (WTD)', nrows=0).columns[0]
dfDict['EU Access TS (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='EU Access TS (WTD)', header = 1)
questionDict['EU Access TS (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='EU Access TS (WTD)', nrows=0).columns[0]
dfDict['Intra UK Procurement (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Intra UK Procurement (WTD)', header = 1)
questionDict['Intra UK Procurement (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Intra UK Procurement (WTD)', nrows=0).columns[0]
dfDict['Prices Bought TS (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Prices Bought TS (WTD)', header = 1)
questionDict['Prices Bought TS (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Prices Bought TS (WTD)', nrows=0).columns[0]
dfDict['Prices Sold TS (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Prices Sold TS (WTD)', header = 1)
questionDict['Prices Sold TS (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Prices Sold TS (WTD)', nrows=0).columns[0]
dfDict['Increase in Demand TS (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Increase in Demand TS (WTD)', header = 1)
questionDict['Increase in Demand TS (WTD)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Increase in Demand TS (WTD)', nrows=0).columns[0]
dfDict['Worker Shortage (WTD) (1)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Worker Shortage (WTD) (1)', header = 1)
questionDict['Worker Shortage (WTD) (1)']=pd.read_excel('bicswave52final-edited.xlsx', sheet_name='Worker Shortage (WTD) (1)', nrows=0).columns[0]

#Set a data frame to load up when industry/size tab is first opened.
dff = dfDict['Trading Status TS1 (WTD)']

#Data frames for regional tab.
dfStockLevels = pd.read_excel('dataTrial.xlsx', sheet_name=1)
dfExpenditure = pd.read_excel('dataTrial.xlsx', sheet_name=2)

#Region border data for map.
myRegions2=json.load(open("uk_regions.geojson"))

#Assign correct border to each region.
thisdict = {
    "North East":1,
    "North West":2,
    "Yorkshire & the Humber":3,
    "East Midlands":4,
    "West Midlands":5,
    "East of England":6,
    "London":7,
    "South East":8,
    "South West":9,
    "Northern Ireland":10,
    "Scotland":11,
    "Wales":12,
    "England":13,
    "UK":14
}

#Add new column that links to region number.
dfStockLevels['id']=dfStockLevels['Region'].apply(lambda x: thisdict[x])
dfExpenditure['id']=dfExpenditure['Region'].apply(lambda x: thisdict[x])

#Border info was 'backwards' so change that.
myRegions2_rewound = rewind(myRegions2,rfc7946=False)

#Defines layout for first tab.
tab1_layout=[
   html.Div(id='graphC'),
   
   #Title
   html.H1("BICS Regional Data", style={'text-align': 'center'}),

    #Dropdown
    dcc.Dropdown(id="selectAnswerC",
                 options=[
                     {"label": "Coronavirus (COVID-19) pandemic", "value": 'Coronavirus (COVID-19) pandemic'},
                     {"label": "End of the EU transition period", "value": 'End of the EU transition period'}
                     ],
                 multi=False,
                 value="Coronavirus (COVID-19) pandemic",
                 style={'width': "40%"}
                 ),
    
    #To display users choice.
    html.Div(id='output_containerC', children=[]),

    #The two graphs
    dcc.Graph(id='graph1C', figure={}),
    dcc.Graph(id='graph2C', figure={})
]

#Making a list of the waves to put into dropdown.
waveList=['Wave ' + str(i) for i in range(52,0,-1)]

#Defines layout for second tab.
tab2_layout=[
   html.Div(id='graphB'),
   
   #Title
   html.H1("BICS Industry/Size Data ", style={'text-align': 'center'}),
   
   #Note
   html.H6("Notes: Not all questions were asked on all waves. Some data may be omitted if not enough responses were obtained for that category.", style={'text-align': 'center'}),
   
   #Dropdown to choose question
    dcc.Dropdown(id="selectIssue",
                 options=[
                     {"label": "Trading Status", "value": 'Trading Status TS1 (WTD)'},
                     {"label": "Supply Chains", "value": 'Supply Chains TS (WTD) (1)'},
                     {"label": "Transition Costs", "value": 'Transition Costs TS (WTD)'},
                     {"label": "EU Access", "value": 'EU Access TS (WTD)'},
                     {"label": "Intra UK Procurement", "value": 'Intra UK Procurement (WTD)'},
                     {"label": "Prices Bought", "value": 'Prices Bought TS (WTD)'},
                     {"label": "Prices Sold", "value": 'Prices Sold TS (WTD)'},
                     {"label": "Increase in Demand", "value": 'Increase in Demand TS (WTD)'},
                     {"label": "Worker Shortage", "value": 'Worker Shortage (WTD) (1)'}
                     ],
                 multi=False,
                 value="Trading Status TS1 (WTD)",
                 style={'width': "40%"}
                 ),
    
    #Dropdown to choose wave.
    dcc.Dropdown(id="selectWave",
                 options=[
                     {'label':i, 'value':i} for i in waveList],
                 multi=False,
                 value="Wave 52",
                 style={'width': "40%"}
                 ),
        
    #Dropdown to choose to view by industry or size or all.
    dcc.Dropdown(id="byGroup",
                 options=[
                     {"label": "Industries", "value": 'Industries'},
                     {"label": "Size Bands", "value": 'Size Bands'},
                     {"label": "All", "value": 'All'}],
                 multi=False,
                 value="All",
                 style={'width': "40%"}
                 ),
    
    #Displays what options the user has chosen.
    html.Div(id='output_containerB1', children=[]),
    
    #Displays Survey Question.
    html.H2(id='output_containerB2', children=[], style={'text-align': 'center'}),
    
    #Gap
    html.Br(),

    #Bar chart.
    dcc.Graph(id='myGraphB', figure={})
]


#Defines layout for third tab.
tab3_layout = [html.Div([
    html.Div([
        #Title
        html.Pre(children="Regression",
                 style={"text-align": "center", "font-size": "100%", "color": "black"})
    ]),

    html.Div([
        #Graph
        dcc.Graph(id='the_graph')
    ]),

    html.Div([
        #Slider
        dcc.RangeSlider(id='the_wave',
                        min=11,
                        max=50,
                        value=[11, 15],
                        marks=mark_values,
                        step=None)
    ], style={"width": "70%", "position": "absolute",
              "left": "5%"})

])]


#Defines full layout (tabs and tab names).
app.layout = html.Div(
   children=[
      dcc.Tabs(
         id='tabs', value=1, children=[
            dcc.Tab(label='Regional', value=1),
            dcc.Tab(label='Industry/Size', value=2),
            dcc.Tab(label='Regressions', value=3)
            ]
      ),
   html.Div(id='tab-output')
   ]
)

#Callback to update choropleth maps.
#Inputs: dropdown on maps tab
#Outputs: Two choropleth maps, container for text with option chosen.
@app.callback(
    [Output(component_id='output_containerC', component_property='children'),
     Output(component_id='graph1C', component_property='figure'),
    Output(component_id='graph2C', component_property='figure')],
    [Input(component_id='selectAnswerC', component_property='value')])

#So this is triggered whenever input changes.
def update_graphC(option_slctdC):
    
    #This helps to check on console whether correct actions are happening.
    print(option_slctdC)
    print(type(option_slctdC))
    
    #Update options chosen.
    containerC = "Showing: {}".format(option_slctdC)

    #Update first choropleth map.
    figure1C=px.choropleth(dfStockLevels, locations='id',geojson=myRegions2_rewound,
                      featureidkey="properties.objectid",
                      color=option_slctdC,range_color=(0.05,0.35),
                      color_continuous_scale='balance',
                      title="Impact to business's stock levels (Nov 21)"
                      ,hover_name='Region', template='plotly_dark')
    figure1C.update_geos(fitbounds="locations",visible = False)
    
    #Update second choropleth map.
    figure2C=px.choropleth(dfExpenditure, locations='id',geojson=myRegions2_rewound,
                      featureidkey="properties.objectid",
                      color=option_slctdC,range_color=(0.034,0.65),
                      color_continuous_scale='balance',
                      title="Impact to business's capital expenditure (Nov 21)"
                      ,hover_name='Region', template='plotly_dark')
    figure2C.update_geos(fitbounds="locations",visible = False)
    
    #Output Changes
    return containerC, figure1C, figure2C

#Callback to update bar chart on industry/size tab.
#Inputs: 3 dropdowns on industry/size tab.
#Outputs: Bar chart, container for text with option chosen, 
#container for question from survey.
@app.callback(
    [Output(component_id='output_containerB1', component_property='children'),
     Output(component_id='output_containerB2', component_property='children'),
     Output(component_id='myGraphB', component_property='figure')],
    [Input(component_id='selectIssue', component_property='value'),
     Input(component_id='selectWave', component_property='value'),
     Input(component_id='byGroup', component_property='value')])

#This is triggered whenever any of the 3 input changes.
def update_graphB(option_slctd1,option_slctd2,option_slctd3):
    global dff
    
    #Keeps track of which dropdown was changed.
    ctx = dash.callback_context
    theInput=ctx.triggered[0]['prop_id'].split('.')[0]
    
    #This helps to check on console whether correct actions are happening.
    print(theInput)
    print(option_slctd1 + option_slctd2 + option_slctd3)
    print(type(option_slctd2))
    
    #Update options chosen.
    containerB1 = "Showing: {}".format(option_slctd1+" "+option_slctd2+" "+option_slctd3)
    
    #Run this if question needs to be changed as a new dataframe should be loaded.
    if theInput == 'selectIssue':
        
        #Get correct dataframe and question.
        dff=dfDict[option_slctd1]
        containerB2 = questionDict[option_slctd1]
        
        #Get answer that we are going to plot.
        df2=dff.copy()
        colname = df2.columns[3]
        
        #Filter to wave chosen.
        df2 = df2[df2["Wave"] == option_slctd2]
        
        #Filter to industry or size if needed.
        if option_slctd3 == 'Industries':
            df2 = df2[:14]
        elif option_slctd3 == 'Size Bands':
            df2 = df2[14:20]
        
        #Update bar chart.
        fig = px.bar(df2, x="Industry/Size band", y=colname)
        
        #Output updates
        return containerB1,containerB2, fig
    else:
        
        #Filter to wave chosen.
        df2=dff.copy()
        df2 = df2[df2["Wave"] == option_slctd2]
        
        #Filter to industry or size if needed.
        if option_slctd3 == 'Industries':
            df2 = df2[:14]
        elif option_slctd3 == 'Size Bands':
            df2 = df2[14:20]
        
        #Get answer that we are going to plot.
        colname = df2.columns[3]
        
        #Update bar chart.
        fig = px.bar(df2, x="Industry/Size band", y=colname)
        
        #Output updates - no update to question as that is not changing.
        return containerB1,dash.no_update, fig
        
#Callback to update graph on regressions tab.
#Inputs: Wave slider.
#Outputs: Graph.     
@app.callback(
    Output('the_graph', 'figure'),
    [Input('the_wave', 'value')]
)

#This is triggered when the input changes.
def update_graph(waves_chosen):
    
    #Filter dataframe by waves chosen.
    dffRegressions = dfRegressions[(dfRegressions['Wave'] >= waves_chosen[0]) & (dfRegressions['Wave'] <= waves_chosen[1])]
    # filter df rows where column year values are >=1985 AND <=1988
    dffRegressions = dffRegressions.groupby(["Industry/Size Band"], as_index=False)[["Stock levels are higher than normal (%)",
                                                               "Prices increased more than normal (%)"]].mean()
   
    #Change graph.
    scatterplot = px.scatter(
        data_frame=dffRegressions,
        x="Stock levels are higher than normal (%)",
        y="Prices increased more than normal (%)",
        hover_data=['Industry/Size Band'],
        hover_name="Industry/Size Band",
        height=550,
        trendline='ols'
    )
    scatterplot.update_traces(textposition='top center')
    
    #Output updated graph
    return (scatterplot)    

#Callback to update which tab is showing.
#Inputs: Tab choice.
#Outputs: Layout.
@app.callback(
	Output('tab-output', 'children'),
	[Input('tabs', 'value')])

def show_content(value):
    print(value)
    if value==1:
        return tab1_layout
    elif value==2:
        return tab2_layout
    elif value==3:
        return tab3_layout
    else:
        html.Div()

app.run_server()