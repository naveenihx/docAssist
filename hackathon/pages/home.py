
from dash import Dash, html, dcc
import dash
from datetime import date
from dash import Dash, dash_table, dcc, html, ctx,callback
#from dash import html, dcc, callback, Input, Output
from dash.dependencies import Input, Output, State
from dash_canvas import DashCanvas
import dash_bootstrap_components as dbc
import pandas as pd
import os
def link(txnid):
    return f'[{txnid}](/report/{txnid})'
df_main = pd.read_csv(os.path.join(os.getcwd(),'Analysis.csv'))
#df_main = pd.read_csv('~/workspace/Research/hackathon/Analysis.csv')
df_main = df_main.loc[:, ~df_main.columns.str.contains('^Unnamed')]
df_main = df_main.drop_duplicates(['ABHA ID'],keep='last')
#df_main = data.drop(columns=['img_path', 's3_path'])
df_main['link']=df_main['ABHA ID'].apply(link)
dash.register_page(__name__)

layout = html.Div(children=[

#*************************************************************************************************************#            
        dbc.Row([ 
            dcc.Store(id="selected-rows", storage_type="memory"),
                    dcc.Store(id="flag-memory", storage_type="memory"),
                    dcc.Interval(
                        id='interval-component',
                        interval=1*1000, # in milliseconds
                        n_intervals=0
                    ),
                    dash_table.DataTable(
                    id='datatable-interactivity',
                    columns=[{'id': i, 'name': i, 'presentation': 'markdown'} if i == 'link' else
                        {"name": i, "id": i, "deletable": True, "selectable": True, "renamable": True} for i in df_main.columns
                    ],
                    data=df_main.to_dict('records'),
                    editable=False,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable="single",
                    #row_selectable="single",
                    row_deletable=False,
                    selected_columns=[],
                    selected_rows=[],
                    page_action="native",
                    page_current= 0,
                    page_size= 1000,
                    fixed_rows={'headers': True},
                    style_table={'overflowX': 'scroll','height': '1000px'},
                    style_cell={'textAlign': 'left',
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                'minWidth': '50px', 'width': '60px', 'maxWidth': '180px',},
                    style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'},
                    ),
        ])


])

@callback(Output('datatable-interactivity', 'data'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    df_main = pd.read_csv(os.path.join(os.getcwd(),'Analysis.csv'))
    #df_main = data.drop(columns=['img_path', 's3_path'])
    df_main['link']=df_main['ABHA ID'].apply(link)
    df_main = df_main.loc[:, ~df_main.columns.str.contains('^Unnamed')]
    df_main = df_main.drop_duplicates(['ABHA ID'],keep='last')
    return df_main.to_dict('records')
    