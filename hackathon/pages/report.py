from dash import Dash, html, dcc
import dash
from datetime import date
from dash import Dash, dash_table, dcc, html, ctx
from dash.dependencies import Input, Output, State
from dash_canvas import DashCanvas
import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, callback, Input, Output
import plotly.express as px
from jupyter_dash import JupyterDash
import dash
from datetime import date
from dash import dcc,ctx
import dash_html_components as html
from dash.dependencies import Input, Output
from skimage import data
import json
import base64
import codecs
import os
from pdf2image import convert_from_path
import cv2
import glob
import numpy as np
import pandas as pd
from dash_canvas import DashCanvas
from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from pathlib import Path
from dash.exceptions import PreventUpdate
import joblib
import colorlover
dash.register_page(__name__, path_template="/report/<report_id>")

# Function for styling the table
def discrete_background_color_bins(df, n_bins=5, columns='all'):

    bounds = [i * (1.0 / n_bins) for i in range(n_bins+1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins+4)]['div']['RdYlGn'][2:-2][i - 1]
        color = 'black'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))

global df
global df_bio
global fig
df = pd.DataFrame()
df_bio = pd.DataFrame()
df['context_score']=1
print(os.path.join(os.getcwd(),'assets/page.jpg'))
img = cv2.imread(os.path.join(os.getcwd(),'assets/page.jpg'))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
fig = px.imshow(img)
fig.update_layout(dragmode="drawrect")
fig.update_layout(coloraxis_showscale=False)
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)
fig.update_layout(width=700, height=1000,margin=dict(l=0,r=1, b=1,t=1))
img_lst=[]

def layout(report_id=None):
    global df
    global df_bio
    global fig
    global img_lst
    global img_index
    
    img_lst = glob.glob(os.path.join(os.getcwd(),f'assets/{report_id}/**.jpg'))
    if report_id != None:
        df = pd.read_csv(os.path.join(os.getcwd(),f'assets/{report_id}/output.csv'))
        df_bio = pd.read_csv(os.path.join(os.getcwd(),f'Analysis.csv'))
        df_bio = df_bio.loc[:, ~df_bio.columns.str.contains('^Unnamed')]
        print(df_bio.head())
        df_bio['ABHA ID'] = df_bio['ABHA ID'].astype(str)
        df_bio = df_bio[df_bio['ABHA ID'] == str(report_id)]
        df_bio = df_bio.drop_duplicates(['ABHA ID'],keep='last')
        
        print(df.head())
        print(df_bio.head())
        
        print(img_lst)
    img_index=0
    if len(img_lst)>0:
        img = cv2.imread(img_lst[img_index])
    else:
        img = cv2.imread(os.path.join(os.getcwd(),'assets/page.jpg'))

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    fig = px.imshow(img)
    fig.update_layout(dragmode="drawrect")
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout(width=700, height=1000,margin=dict(l=0,r=1, b=1,t=1))
    #(styles, legend) = discrete_background_color_bins(df, columns=['context_score'])
    #styles.append({
    #        'if': {
    #            'filter_query': '{Is_Pdx} = "Yes"'
    #        },
    #        'backgroundColor': '#0074D9',
    #        'color': 'white'
    #    })
    #image
    #https://stackoverflow.com/questions/68747552/how-to-show-a-local-image-in-an-interactive-dash-with-python
#https://dash.plotly.com/annotations


    
    
    #layout
    screen= dbc.Row([
            
            dbc.Col([
                
                dbc.Row([
                    dbc.Col(dbc.Button('Previous' , id='previous' ),width=3),
                    dbc.Col(dbc.Button('Next' , id='next'),width=3)

                ],justify="between"),
                
                dcc.Graph(id="graph-picture", figure=fig)
            ],width=5),
                
     
            dbc.Col([
                dbc.Row([

                
                    dcc.Store(id="selected-rows", storage_type="memory"),
                    dcc.Store(id="flag-memory", storage_type="memory"),
                    html.H3('Patient Bio'),
                    dbc.Table.from_dataframe(df_bio, striped=True, bordered=True, hover=True),
                    html.H3('System Extracted Data'),
                    dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
                    
                ],)
                
            ],width=6)
    ])
    return screen


@callback(
    Output(component_id="graph-picture", component_property='figure'),
    [Input(component_id='next', component_property='n_clicks'),
     Input(component_id='previous', component_property='n_clicks')
    ],State(component_id='datatable-interactivity',component_property='markdown_options'),
    prevent_initial_call=True
)
def update_city_selected(n_next,n_previous,markdown):
    print(f'markdown = {markdown}')
    global img_index
    global img_lst
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    if button_id != None and button_id =='next':
        if (img_index+1 >= len(img_lst)):
            raise PreventUpdate
        else:
            img_index +=1
            print(f'clicked next {img_lst[img_index]}')
            img = cv2.imread(img_lst[img_index])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            fig = px.imshow(img)
            fig.update_layout(dragmode="drawrect")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            fig.update_layout(width=700, height=1000,margin=dict(l=0,r=1, b=1,t=1))
    if button_id != None and button_id =='previous':
        if (img_index <= 0):
            raise PreventUpdate
        else:
            
            img_index -=1
            print('clicked previous {img_lst[img_index]}')
            img = cv2.imread(img_lst[img_index])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            fig = px.imshow(img)
            fig.update_layout(dragmode="drawrect")
            fig.update_layout(coloraxis_showscale=False)
            fig.update_xaxes(showticklabels=False)
            fig.update_yaxes(showticklabels=False)
            fig.update_layout(width=700, height=1000,margin=dict(l=0,r=1, b=1,t=1))
        
    return fig

