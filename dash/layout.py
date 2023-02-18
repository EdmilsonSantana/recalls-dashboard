import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
from recalls import Recalls
import pandas as pd
from datetime import date
import dash_loading_spinners as dls


def MainLayout(app: dash.Dash, df: pd.DataFrame) -> html.Div:
    recalls = Recalls(df)
    min_reported_date, max_reported_date = recalls.get_date_range()
    manufacturers = recalls.get_manufacturers()

    return html.Div([
        Header(app),
        Card([
            dbc.Row([
                dbc.Col(
                    Select(
                        label='Manufacturer',
                        id='select-manufacturer',
                        options=manufacturers,
                        value=manufacturers[0]
                    )
                ),
                dbc.Col(
                    Select(
                        label='Vehicle Model',
                        id='select-vehicle',
                    )
                ),
            ]),
            dbc.Row([
                    dbc.Col(DatePickerRange(
                        label='Reported Date',
                        id='reported-date-picker',
                        min_reported_date=min_reported_date,
                        max_reported_date=max_reported_date
                    ))
                    ], style={'margin-top': 10}),
            dbc.Row([dbc.Col(dls.Hash((card)))
                    for card in CardsList()], style={'margin-top': 10})
        ]),
        Card([
            html.H6("Manufacturer details"),
            dls.Hash(
                dash_table.DataTable(
                    id='manufacturers-table',
                    virtualization=True,
                    fixed_rows={'headers': True},
                    style_table={'height': 300},
                    style_cell={
                        'textAlign': 'left',
                        'overflow': 'hidden',
                        'textOverflow': 'ellipsis',
                        'maxWidth': 0
                    },
                    sort_action='native',
                    style_as_list_view=True,
                )
            )
        ]),
        Card([
            dbc.Row([
                dbc.Col(
                    dls.Hash(dcc.Graph(id="recalls-and-affected-units-by-reported-date-graph"))),
                dbc.Col(
                    dls.Hash(dcc.Graph(id="affected-units-distribution-graph"))),
            ])
        ]),
        Card([
            dbc.Row([
                dbc.Col(
                    dls.Hash(dcc.Graph(id="recalls-distribution"))),
                dbc.Col(
                    dls.Hash(dcc.Graph(id="recalls-and-affected-units-by-vehicle")))
            ])
        ]),
        Card([
            dbc.Row([
                dbc.Col(
                    dls.Hash(dcc.Graph(id="recalls-and-affected-units-by-component"))),
            ])
        ]),
    ])


def Header(app: dash.Dash) -> dbc.Row:
    logo = html.Img(
        src=app.get_asset_url("logo.png"), style={"height": 100}
    )

    return html.Div([
        dbc.Row([
            dbc.Row(dbc.Col(logo)),
        ]),
    ], style={"margin": 10})


def CardsList() -> list:
    return [
        dbc.Card(
            [
                html.H2(id='recalls-count', className="card-title"),
                html.P("Recalls", className="card-text"),
            ],
            body=True,
            color="light",
        ),
        dbc.Card(
            [
                html.H2(id='vehicles-count', className="card-title"),
                html.P("Distinct vehicles", className="card-text"),
            ],
            body=True,
            color="dark",
            inverse=True,
        ),
        dbc.Card(
            [
                html.H2(id='affected-units-count', className="card-title"),
                html.P("Vehicle units affected", className="card-text"),
            ],
            body=True,
            color="primary",
            inverse=True,
        ),
    ]


def Card(children: list) -> dbc.Card:
    return dbc.Card(children=children, style={'margin': 5}, body=True)


def DatePickerRange(label: str, id: str, min_reported_date: date, max_reported_date: date) -> list:
    return [
        dbc.Label(label, html_for=id),
        dcc.DatePickerRange(
            id=id,
            min_date_allowed=min_reported_date,
            max_date_allowed=max_reported_date,
            initial_visible_month=min_reported_date,
            start_date=min_reported_date,
            end_date=max_reported_date,
            style={"display": "block"}
        )
    ]


def Select(label: str, id: str, **kwargs) -> list:
    return [
        dbc.Label(label, html_for=id),
        dbc.Select(id=id, **kwargs)
    ]
