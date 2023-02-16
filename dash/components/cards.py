import dash_bootstrap_components as dbc
from dash import html


def CardsList() -> list:
    return [
        dbc.Card(
            [
                html.H2(id='recalls-count', className="card-title"),
                html.P("Recalls count", className="card-text"),
            ],
            body=True,
            color="light",
        ),
        dbc.Card(
            [
                html.H2(id='vehicles-count', className="card-title"),
                html.P("Distinct vehicle models", className="card-text"),
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
