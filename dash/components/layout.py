import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from model.recalls import Recalls
import components.charts as charts
from components.cards import CardsList
from components.header import Header
from components.inputs import DatePickerRange, Select
from components.sidebar import Sidebar


def MainLayout(app: dash.Dash, recalls: Recalls) -> html.Div:
    min_reported_date, max_reported_date = recalls.get_date_range()

    return html.Div([
        html.Div([Header("Recalls Dashboard", app)],
                 style={'padding': '10px'}),
        html.Hr(),
        dbc.Row([
            dbc.Col(Sidebar(recalls), width='4'),
            dbc.Col(dbc.Card(
                [
                    dbc.Row([
                        dbc.Col(
                            Select(
                                label='Manufacturer',
                                id='select-manufacturer',
                                options=recalls.manufacturers())
                        ),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(DatePickerRange(
                            label='Reported Date',
                            id='reported-date-picker',
                            min_reported_date=min_reported_date,
                            max_reported_date=max_reported_date
                        ))
                    ]),
                    html.Br(),
                    dbc.Row([dbc.Col(card) for card in CardsList()]),
                    html.Br(),
                    dcc.Graph(id="recalls-reported-date-graph"),
                    dcc.Graph(id="affected-units-reported-date-graph"),
                    dcc.Graph(id="components-graph"),
                    dcc.Graph(id="vehicle-components-graph"),
                    dcc.Graph(id="vehicle-year-graph")
                ],
                body=True
            ), width='8')
        ], style={'margin': 5})
    ])


def get_charts(recalls: Recalls) -> list:
    recalls_by_component_category = recalls.get_recalls_grouped_by_component_category()
    recalls_by_reported_date = recalls.get_recalls_grouped_by_month_and_year()
    affected_units_by_reported_date = recalls.get_affected_units_grouped_by_month_and_year()
    recalls_by_vehicle_and_component_category = recalls.get_recalls_by_vehicle_and_component_category()
    recalls_by_vehicle_and_year = recalls.get_recalls_by_vehicle_and_year()

    return [
        charts.get_bar_chart(
            x=recalls_by_component_category.index,
            y=recalls_by_component_category.values,
            title='Recalls count by component category'
        ),
        charts.get_line_chart(
            x=recalls_by_reported_date.index.to_timestamp(),
            y=recalls_by_reported_date.values,
            labels={"x": "Month / Year", "y": "Count"},
            title='Recalls count by reported date'
        ),
        charts.get_line_chart(
            x=affected_units_by_reported_date.index.to_timestamp(),
            y=affected_units_by_reported_date.values,
            labels={"x": "Month / Year", "y": "Affected Units"},
            title='Number of affected units by reported date'
        ),
        charts.get_scatter_plot(
            df=recalls_by_vehicle_and_component_category,
            x='RECALL_ID',
            y='VEHICLE_MODEL',
            color='COMPONENT_CATEGORY',
            title='Recalls count by component category and vehicle',
            labels={
                'RECALL_ID': 'Count',
                'VEHICLE_MODEL': 'Vehicle',
                'COMPONENT_CATEGORY': 'Component Category'},
        ),
        charts.get_scatter_plot(
            df=recalls_by_vehicle_and_year,
            x='RECALL_ID',
            y='VEHICLE_MODEL',
            color='VEHICLE_YEAR',
            title='Recalls count by vehicle model and year',
            labels={
                'RECALL_ID': 'Count',
                'VEHICLE_MODEL': 'Vehicle Model',
                'VEHICLE_YEAR': 'Vehicle Year'},
        )
    ]
