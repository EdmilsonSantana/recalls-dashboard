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


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

min_reported_date, max_reported_date = recalls.get_date_range()

content = dbc.Card(
    [
        dbc.Row([
            dbc.Col([
                dbc.Label('Manufacturer', html_for='select-manufacturer'),
                dbc.Select(id="select-manufacturer",
                           options=recalls.manufacturers(),
                           value='-')
            ]),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Label('Reported Date',
                          html_for='reported-date-picker'),
                dcc.DatePickerRange(
                    id='reported-date-picker',
                    min_date_allowed=min_reported_date,
                    max_date_allowed=max_reported_date,
                    initial_visible_month=min_reported_date,
                    start_date=min_reported_date,
                    end_date=max_reported_date,
                    style={"display": "block"}
                )
            ])
        ]),
        html.Br(),
        dbc.Row([dbc.Col(card) for card in get_cards()]),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph("recalls-reported-date-graph")),
            dbc.Col(dcc.Graph("affected-units-reported-date-graph"))
        ]),
        dbc.Row([dbc.Col(dcc.Graph("components-graph"))]),
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
    Output("recalls-count", "children"),
    Output("vehicles-count", "children"),
    Output("affected-units-count", "children"),
    Output("components-graph", "figure"),
    Output("recalls-reported-date-graph", "figure"),
    Output("affected-units-reported-date-graph", "figure"),
    Input("select-manufacturer", "value"),
    Input("reported-date-picker", "start_date"),
    Input("reported-date-picker", "end_date")
)
def update_layout(manufacturer: str, reported_start_date: str, reported_end_date: str) -> list:

    recalls.filter_by((reported_start_date, reported_end_date), manufacturer)

    by_component_category = recalls.get_component_category_count()
    recalls_by_reported_date = recalls.get_recalls_grouped_by_month_and_year()
    affected_units_by_reported_date = recalls.get_affected_units_grouped_by_month_and_year()

    by_component_category_fig = px.bar(
        x=by_component_category.index,
        y=by_component_category.values,
        labels={"x": "", "y": ""},
        color_discrete_sequence=px.colors.sequential.Blues_r,
        title='Recalls count by component category',
        text_auto=True
    )

    recalls_by_reported_date_fig = px.line(
        y=recalls_by_reported_date.values,
        x=recalls_by_reported_date.index.to_timestamp(),
        labels={"x": "Month / Year", "y": "Count"},
        color_discrete_sequence=px.colors.sequential.Blues_r,
        title='Recalls count by reported date'
    )

    recalls_by_reported_date_fig.update_layout(yaxis_title=None, xaxis_title=None)

    affected_units_by_reported_date_fig = px.line(
        y=affected_units_by_reported_date.values,
        x=affected_units_by_reported_date.index.to_timestamp(),
        labels={"x": "Month / Year", "y": "Affected Units"},
        color_discrete_sequence=px.colors.sequential.Blues_r,
        title='Number of affected units by reported date'
    )

    affected_units_by_reported_date_fig.update_layout(yaxis_title=None, xaxis_title=None)

    return [
        recalls.recalls_count(),
        recalls.vehicle_models_count(),
        recalls.affected_units_count(),
        by_component_category_fig,
        recalls_by_reported_date_fig,
        affected_units_by_reported_date_fig
    ]


if __name__ == "__main__":
    app.run_server(debug=True)
