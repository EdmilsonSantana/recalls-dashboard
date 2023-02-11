import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
from model.recalls import Recalls
from components.cards import get_cards
from components.sidebar import get_sidebar

recalls = Recalls()


def Header(name, app):
    logo = html.Img(
        src=app.get_asset_url("logo.png"), style={"height": 100, "margin-top": 10}
    )
    title = html.H2(name, style={"margin-top": 15})

    return dbc.Row([
        dbc.Row(dbc.Col(logo)),
        dbc.Row(dbc.Col(title))
    ])


def LabeledSelect(label, **kwargs):
    return html.Div([
        dbc.Label(label, html_for=kwargs['id']),
        dbc.Select(**kwargs)
    ])


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

graphs = [
    dcc.Graph("components-graph")
]

content = dbc.Card(
    [
        dbc.Row(LabeledSelect(
            id="select-manufacturer",
            options=recalls.manufacturers(),
            value='-',
            label="Manufacturer",
        )),
        html.Br(),
        dbc.Row([dbc.Col(card) for card in get_cards()]),
        html.Br(),
        dbc.Row([dbc.Col(graph) for graph in graphs]),
    ],
    body=True
)

app.layout = html.Div([
    html.Div([Header("Recalls Dashboard", app)], style={'padding': '10px'}),
    html.Hr(),
    dbc.Row([
        dbc.Col(get_sidebar(recalls), width='4'),
        dbc.Col(content, width='8')
    ], style={'margin': 5})
])


@app.callback(
    [Output("recalls-count", "children"),
     Output("vehicles-count", "children"),
     Output("affected-units-count", "children"),
     Output("components-graph", "figure")],
    Input("select-manufacturer", "value"),
)
def update_layout(value: str) -> list:

    recalls.filter_by(value)

    by_component_category = recalls.get_component_category_count()

    fig = px.bar(
        x=by_component_category.index,
        y=by_component_category.values,
        labels={"x": "", "y": ""},
        color_discrete_sequence=px.colors.sequential.Blues_r,
        title='Recalls count by component category',
        text_auto=True
    )

    return [
        recalls.recalls_count(),
        recalls.vehicle_models_count(),
        recalls.affected_units_count(),
        fig
    ]


if __name__ == "__main__":
    app.run_server(debug=True)
