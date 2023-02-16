import dash
import dash_bootstrap_components as dbc
from dash import html


def Header(name: str, app: dash.Dash) -> dbc.Row:
    logo = html.Img(
        src=app.get_asset_url("logo.png"), style={"height": 100, "margin-top": 10}
    )
    title = html.H2(name, style={"margin-top": 15})

    return dbc.Row([
        dbc.Row(dbc.Col(logo)),
        dbc.Row(dbc.Col(title))
    ])
