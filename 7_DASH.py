# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 09:05:03 2023

@author: User
"""

# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update

# Create a dash application
app = dash.Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read the airline data into pandas dataframe
spacex_df =  pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv', 
                            encoding = "ISO-8859-1",
                            dtype = str)

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Application layout
app.layout = html.Div(children=[ 
                                # TASK1: Add title to the dashboard
                                # Enter your code below. Make sure you have correct formatting.
                                html.H1('SpaceX launch success', style={'textAlign':'center', 'color':'#503D36', 'font-size': 24}),
                                # REVIEW2: Dropdown creation
                                # Create an outer division 
                                html.Div([
                                    # Add an division
                                    html.Div([
                                        # Create an division for adding dropdown helper text for report type
                                        html.Div(
                                            [
                                            html.H2('Launch Sites:', style={'margin-right': '2em'}),
                                            ]
                                        ),
                                        # TASK2: Add a dropdown
                                        dcc.Dropdown(id='site-dropdown', 
                                                    options=[
                                                     {'label': 'All Sites', 'value': 'ALL'},
                                                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                     ],
                                             value='ALL',
                                                    placeholder='Select a Launch Site heree',
                                                    searchable=True,
                                                    style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}),
                                    # Place them next to each other using the division style
                                    ], style={'display':'flex'}
                                    ),
                                    
                                    html.Br(),

                                    # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                    # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                    html.Div(dcc.Graph(id='success-pie-chart')),
                                    html.Br(),
                                    
                                    html.P("Payload range (Kg):"),
                                    
                                    # TASK 3: Add a slider to select payload range
                                    #dcc.RangeSlider(id='payload-slider',...)
                                    dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload]
                                                ),

                                    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ]),
                            ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Success Count for all launch sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df=spacex_df[spacex_df['Launch Site'] == entered_site]
        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig=px.pie(filtered_df, values='class count', names='class', title=f"Total Success Launches for site {entered_site}")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                [Input(component_id='site-dropdown', component_property='value'),
                Input(component_id='payload-slider', component_property='value')])
def scatter(entered_site,payload):
    filtered1_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
    if entered_site=='ALL':
        fig=px.scatter(filtered1_df, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Success count on Payload mass for all sites')
        return fig
    else:
        fig=px.scatter(filtered1_df[filtered1_df['Launch Site']==entered_site], x='Payload Mass (kg)', y='class', color='Booster Version Category', title="Success count on Payload mass for site {entered_site}")
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
                                    
                                    
                                    
                                    
                                    
                                    
                                    