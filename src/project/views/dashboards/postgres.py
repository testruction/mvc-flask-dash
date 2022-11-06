# -*- coding: utf-8 -*-
import dash
from dash import dash_table, dcc, html
import plotly.express as px

from pandas import DataFrame

from project.controllers.postgres import PostgresApis

layout = html.Div([
    html.Div('Fakenames (Table)'), html.Br(),
    dcc.Input(id = 'input_text'), html.Br(), html.Br(),
    html.Div(id = 'target')
])

def init_postgres_dashboard(flask_server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(server=flask_server,
                         url_base_pathname="/fakenames/",
                         external_stylesheets=["/static/css/styles.css",
                                               "https://fonts.googleapis.com/css?family=Lato"])
   
    # Load DataFrame
    df = DataFrame.from_dict(PostgresApis.get_all())

    # Create Layout
    # fig = px.bar(df, x='cctype', y='' text='cctype', color='State')
    dash_app.layout = html.Div(
        children=[
            dcc.Graph(id="histogram-graph",
                      figure={
                        "data": [
                            {
                                "x": df["cctype"],
                                "y": df["statefull"],
                                # "text": df["State"],
                                # "customdata": df["CountryFull"],
                                # "name": "Fakenames",
                                "type": "histogram"
                            }
                        ],
                        "layout": {
                            "title": "Identities credit cards",
                            "height": 500,
                            "padding": 150
                        },
                    },
            ),
            create_data_table(df)
        ],
        id="dash-container"
    )
    return dash_app.server


def create_data_table(df):
    """Create Dash datatable from Pandas DataFrame."""
    table = dash_table.DataTable(
        id="dataset-table",
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict("records"),
        sort_action="native",
        sort_mode="native",
        page_size=300,
    )
    
    return table