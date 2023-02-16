import datetime

import dash_bootstrap_components as dbc
import pandas as pd
from dash import dcc, html
from dateutil.relativedelta import relativedelta
from model.recalls import Recalls

from components.charts import get_horizontal_bar_chart


def Sidebar(recalls: Recalls) -> html.Div:
    limit = 10
    last_year = datetime.datetime.now() - relativedelta(years=1)

    df_by_manufacturers = recalls.get_recalls_by_manufacturers(last_year, limit)
    df_by_vehicles = recalls.get_recalls_by_vehicles(last_year, limit)
    df_by_components = recalls.get_recalls_by_components(last_year, limit)

    return dbc.Card(
        dbc.CardBody(
            [
                html.H6("Most Popular Recalls (Last Year)",
                        className="card-subtitle"),
                html.Br(),
                dbc.Tabs(
                    [
                        dbc.Tab(
                            get_sidebar_graph(df_by_manufacturers),
                            label=f'Top {limit} Manufacturers'
                        ),
                        dbc.Tab(
                            get_sidebar_graph(df_by_vehicles),
                            label=f'Top {limit} Vehicles'
                        ),
                         dbc.Tab(
                            get_sidebar_graph(df_by_components),
                            label=f'Top {limit} Components'
                        ),
                    ]
                )
            ],
        ),
        style={'height': '100%'}
    )

def get_sidebar_graph(df: pd.DataFrame) -> dcc.Graph:
    return dcc.Graph(figure=get_horizontal_bar_chart(df), style={'height': '100%', 'width': '100%'})
