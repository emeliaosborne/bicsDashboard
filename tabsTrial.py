# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 15:01:27 2022

@author: Emelia
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

dfRegressions = pd.read_csv("regression_data.csv")
dfRegressions.columns = ['Industry/Size Band', 'Wave','Stock levels are higher than normal (%)',
                    'Stock levels are lower than normal (%)', 'Prices increased more than normal (%)',
                    'Prices decreased more than normal (%)', 'Demand increased more than normal (%)',
                    'Demand did not increase (%)']

mark_values = {11: '11', 13: '13', 15: '15', 17: '17',
               19: '19', 21: '21', 23: '23', 25: '25',
               27: '27', 29: '29', 31: '31', 42: '42',
               44: '44', 46: '46', 48: '48', 50: '50'}


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

dff = dfDict['Trading Status TS1 (WTD)']


dfStockLevels = pd.read_excel('dataTrial.xlsx', sheet_name=1)
dfExpenditure = pd.read_excel('dataTrial.xlsx', sheet_name=2)
myRegions2=json.load(open("uk_regions.geojson"))
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
dfStockLevels['id']=dfStockLevels['Region'].apply(lambda x: thisdict[x])
dfExpenditure['id']=dfExpenditure['Region'].apply(lambda x: thisdict[x])
myRegions2_rewound = rewind(myRegions2,rfc7946=False)

tab1_layout=[
   html.Div(id='graphC'),
   html.H1("BICS Regional Data", style={'text-align': 'center'}),

    dcc.Dropdown(id="selectAnswerC",
                 options=[
                     {"label": "Coronavirus (COVID-19) pandemic", "value": 'Coronavirus (COVID-19) pandemic'},
                     {"label": "End of the EU transition period", "value": 'End of the EU transition period'}
                     ],
                 multi=False,
                 value="Coronavirus (COVID-19) pandemic",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_containerC', children=[]),
#    html.Br(),

    dcc.Graph(id='graph1C', figure={}),
    dcc.Graph(id='graph2C', figure={})
]

waveList=['Wave ' + str(i) for i in range(52,0,-1)]


tab2_layout=[
   html.Div(id='graphB'),
   html.H1("BICS Industry/Size Data ", style={'text-align': 'center'}),
   html.H6("Notes: Not all questions were asked on all waves. Some data may be omitted if not enough responses were obtained for that category.", style={'text-align': 'center'}),
   
   
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
    
    dcc.Dropdown(id="selectWave",
                 options=[
                     {'label':i, 'value':i} for i in waveList],
                 multi=False,
                 value="Wave 52",
                 style={'width': "40%"}
                 ),
    
    dcc.Dropdown(id="byGroup",
                 options=[
                     {"label": "Industries", "value": 'Industries'},
                     {"label": "Size Bands", "value": 'Size Bands'},
                     {"label": "All", "value": 'All'}],
                 multi=False,
                 value="All",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_containerB1', children=[]),
    html.H2(id='output_containerB2', children=[], style={'text-align': 'center'}),
    html.Br(),

    dcc.Graph(id='myGraphB', figure={})
]

tab3_layout = [html.Div([
    html.Div([
        html.Pre(children="Regression",
                 style={"text-align": "center", "font-size": "100%", "color": "black"})
    ]),

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

    html.Div([
        dcc.RangeSlider(id='the_wave',
                        min=11,
                        max=50,
                        value=[11, 15],
                        marks=mark_values,
                        step=None)
    ], style={"width": "70%", "position": "absolute",
              "left": "5%"})

])]


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

@app.callback(
    [Output(component_id='output_containerC', component_property='children'),
     Output(component_id='graph1C', component_property='figure'),
    Output(component_id='graph2C', component_property='figure')],
    [Input(component_id='selectAnswerC', component_property='value')])
def update_graphC(option_slctdC):
    print(option_slctdC)
    print(type(option_slctdC))

    containerC = "Showing: {}".format(option_slctdC)

    # Plotly Express
    figure1C=px.choropleth(dfStockLevels, locations='id',geojson=myRegions2_rewound,
                      featureidkey="properties.objectid",
                      color=option_slctdC,range_color=(0.05,0.35),
                      color_continuous_scale='balance',
                      title="Impact to business's stock levels (Nov 21)"
                      ,hover_name='Region', template='plotly_dark')
    figure1C.update_geos(fitbounds="locations",visible = False)
    
    figure2C=px.choropleth(dfExpenditure, locations='id',geojson=myRegions2_rewound,
                      featureidkey="properties.objectid",
                      color=option_slctdC,range_color=(0.034,0.65),
                      color_continuous_scale='balance',
                      title="Impact to business's capital expenditure (Nov 21)"
                      ,hover_name='Region', template='plotly_dark')
    figure2C.update_geos(fitbounds="locations",visible = False)
    
    return containerC, figure1C, figure2C

@app.callback(
    [Output(component_id='output_containerB1', component_property='children'),
     Output(component_id='output_containerB2', component_property='children'),
     Output(component_id='myGraphB', component_property='figure')],
    [Input(component_id='selectIssue', component_property='value'),
     Input(component_id='selectWave', component_property='value'),
     Input(component_id='byGroup', component_property='value')])
def update_graphB(option_slctd1,option_slctd2,option_slctd3):
    global dff
    ctx = dash.callback_context
    theInput=ctx.triggered[0]['prop_id'].split('.')[0]
    print(theInput)
    print(option_slctd1 + option_slctd2 + option_slctd3)
    print(type(option_slctd2))
    
    containerB1 = "Showing: {}".format(option_slctd1+" "+option_slctd2+" "+option_slctd3)
    if theInput == 'selectIssue':
        
        dff=dfDict[option_slctd1]
        containerB2 = questionDict[option_slctd1]
        df2=dff.copy()
        colname = df2.columns[3]
        df2 = df2[df2["Wave"] == option_slctd2]
        if option_slctd3 == 'Industries':
            df2 = df2[:14]
        elif option_slctd3 == 'Size Bands':
            df2 = df2[14:20]
        # Plotly Express
        fig = px.bar(df2, x="Industry/Size band", y=colname)
        return containerB1,containerB2, fig
    else:
        
        df2=dff.copy()
        df2 = df2[df2["Wave"] == option_slctd2]
        
        
        if option_slctd3 == 'Industries':
            df2 = df2[:14]
        elif option_slctd3 == 'Size Bands':
            df2 = df2[14:20]

        colname = df2.columns[3]
        # Plotly Express
        fig = px.bar(df2, x="Industry/Size band", y=colname)
        return containerB1,dash.no_update, fig
        
     
@app.callback(
    Output('the_graph', 'figure'),
    [Input('the_wave', 'value')]
)
def update_graph(waves_chosen):
    # print(years_chosen)

    dffRegressions = dfRegressions[(dfRegressions['Wave'] >= waves_chosen[0]) & (dfRegressions['Wave'] <= waves_chosen[1])]
    # filter df rows where column year values are >=1985 AND <=1988
    dffRegressions = dffRegressions.groupby(["Industry/Size Band"], as_index=False)[["Stock levels are higher than normal (%)",
                                                               "Prices increased more than normal (%)"]].mean()
    # print (dff[:3])

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

    return (scatterplot)    

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