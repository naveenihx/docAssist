from dash import Dash, html, dcc
import dash
from datetime import date
from dash import Dash, dash_table, dcc, html, ctx
from dash.dependencies import Input, Output, State
from dash_canvas import DashCanvas
import dash_bootstrap_components as dbc
import pandas as pd
import os
print('this is the path')
print(os.path.join(os.getcwd(),'assets/page.jpg'))
app = Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'IHX Hospital Doctor Dashboard'
for page in dash.page_registry.values():
    print(page["relative_path"])
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="https://ihx.in/images/IHX-logo.png", height="25px")),
                        dbc.Col(dbc.NavbarBrand("IHX Hospital Doctor Dashboard", className="ms-2")),
                    ],
                    align="left",
                    className="g-0",
                ),
                # href="https://plotly.com",
                style={"textDecoration": "none",'textAlign':'left'},
            ),

        ]
    ),
    # color="dark",
    dark=False,
)

app.layout = html.Div([
    
    navbar,
    dbc.Container([
    dash.page_container
    ],fluid=True)
])

if __name__ == '__main__':
    #app.run_server(debug=True)
    app.run_server(debug=True,host='0.0.0.0',port=8320)