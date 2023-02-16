from datetime import date
import dash_bootstrap_components as dbc
from dash import dcc


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


def Select(label: str, id: str, options: list) -> list:
    return [
        dbc.Label(label, html_for=id),
        dbc.Select(id=id, options=options, value='-')
    ]
