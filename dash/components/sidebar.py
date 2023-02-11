import dash_bootstrap_components as dbc
from model.recalls import Recalls
from dash import html
from components.graphs import get_horizontal_bar_chart
import datetime
from dateutil.relativedelta import relativedelta

def get_sidebar(recalls: Recalls) -> html.Div:

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
                            get_horizontal_bar_chart(df_by_manufacturers),
                            label=f'Top {limit} Manufacturers'
                        ),
                        dbc.Tab(
                            get_horizontal_bar_chart(df_by_vehicles),
                            label=f'Top {limit} Vehicles'
                        ),
                         dbc.Tab(
                            get_horizontal_bar_chart(df_by_components),
                            label=f'Top {limit} Components'
                        ),
                    ]
                )
            ],
        ),
        style={'height': '100%'}
    )
