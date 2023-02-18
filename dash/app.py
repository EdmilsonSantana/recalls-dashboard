import dash_bootstrap_components as dbc
import dash
from layout import MainLayout
import pandas as pd
from callbacks import register_callbacks

df = pd.read_csv('data/recalls.csv', parse_dates=['REPORTED_DATE'])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = MainLayout(app, df)
register_callbacks(app, df)

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=8050, debug=True)
