from dash.dependencies import Input, Output
from recalls import Recalls
from charts import RecallsCharts
import pandas as pd
import dash


def register_callbacks(app: dash.Dash, df: pd.DataFrame):

    @app.callback(
        Output("select-vehicle", "options"),
        Output("select-vehicle", "disabled"),
        Input("select-manufacturer", "value"),
    )
    def update_select_vehicle(manufacturer: str) -> list:
        recalls = Recalls(df)
        vehicle_models = recalls.get_vehicle_models(manufacturer)
        return [vehicle_models, not vehicle_models]

    @app.callback(
        Output("recalls-count", "children"),
        Output("vehicles-count", "children"),
        Output("affected-units-count", "children"),
        Output("recalls-and-affected-units-by-reported-date-graph", "figure"),
        Output("affected-units-distribution-graph", "figure"),
        Output("recalls-and-affected-units-by-component", "figure"),
        Output("recalls-and-affected-units-by-vehicle", "figure"),
        Output("recalls-distribution", "figure"),
        Output("manufacturers-table", "data"),
        Input("select-manufacturer", "value"),
        Input("select-vehicle", "value"),
        Input("reported-date-picker", "start_date"),
        Input("reported-date-picker", "end_date")
    )
    def update_cards_and_charts(
            manufacturer: str,
            vehicle: str,
            reported_start_date: str,
            reported_end_date: str) -> list:
        recalls = Recalls(df)

        recalls.filter_by(
            time_range=(reported_start_date, reported_end_date),
            manufacturer=manufacturer,
            vehicle_model=vehicle
        )

        charts = RecallsCharts(recalls)

        return [
            recalls.recalls_count(),
            recalls.vehicle_models_count(),
            recalls.affected_units_count(),
            charts.get_recalls_and_affected_units_by_reported_period_chart(),
            charts.get_affected_units_distribution_chart(),
            charts.get_recalls_and_affected_units_by_component_chart(),
            charts.get_recalls_and_affected_units_by_vehicle_chart(),
            charts.get_recalls_distribution_chart(),
            recalls.get_recalls_and_affected_units_by_manufacturer()
        ]
