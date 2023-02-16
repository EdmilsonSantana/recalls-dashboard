import dash_bootstrap_components as dbc

import dash
from components.layout import MainLayout, get_charts
from dash.dependencies import Input, Output
from model.recalls import Recalls

recalls = Recalls()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = MainLayout(app, recalls)

@app.callback(
    Output("recalls-count", "children"),
    Output("vehicles-count", "children"),
    Output("affected-units-count", "children"),
    Output("components-graph", "figure"),
    Output("recalls-reported-date-graph", "figure"),
    Output("affected-units-reported-date-graph", "figure"),
    Output("vehicle-components-graph", "figure"),
    Output("vehicle-year-graph", "figure"),
    Input("select-manufacturer", "value"),
    Input("reported-date-picker", "start_date"),
    Input("reported-date-picker", "end_date")
)
def update_layout(manufacturer: str, reported_start_date: str, reported_end_date: str) -> list:

    recalls.filter_by((reported_start_date, reported_end_date), manufacturer)

    return [
        recalls.recalls_count(),
        recalls.vehicle_models_count(),
        recalls.affected_units_count(),
        *get_charts(recalls)
    ]

if __name__ == "__main__":
    app.run_server(debug=True)
