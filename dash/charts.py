import plotly.express as px
from plotly.graph_objects import Figure
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from recalls import Recalls


class RecallsCharts(object):
    def __init__(self, recalls: Recalls) -> None:
        self.recalls = recalls

    def get_recalls_and_affected_units_by_reported_period_chart(self) -> Figure:
        by_recalls_and_affected_units = self.recalls.get_recalls_and_affected_units_by_reported_period()

        if (by_recalls_and_affected_units.empty):
            return {}

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
        x = by_recalls_and_affected_units.index.to_timestamp()

        fig.add_trace(
            go.Scatter(
                line=dict(color=px.colors.qualitative.T10[0]),
                x=x,
                y=by_recalls_and_affected_units['RECALL_ID'],
                name='Recalls',
                showlegend=False
            ),
            row=1,
            col=1
        )

        fig.add_trace(
            go.Scatter(
                line=dict(color=px.colors.qualitative.T10[1]),
                x=x,
                y=by_recalls_and_affected_units['AFFECTED_UNITS'],
                name='Vehicle units',
                showlegend=False
            ),
            row=2,
            col=1
        )

        fig.update_layout(
            title_text='Number of recalls and affected vehicle units by reported date'
        )

        y_titles = {'x': 'Recalls', 'x2': 'Vehicle units'}
        fig.for_each_yaxis(lambda y: y.update(title=y_titles[y.anchor]))

        return fig

    def get_recalls_and_affected_units_by_component_chart(self):
        recalls_and_affected_units_by_component = self.recalls.get_recalls_and_affected_units_by_component()

        if (recalls_and_affected_units_by_component.empty):
            return {}

        fig = px.bar(
            recalls_and_affected_units_by_component,
            color_discrete_sequence=px.colors.qualitative.T10,
            x="COMPONENT_NAME",
            y="VALUE",
            color='COMPONENT_CATEGORY',
            facet_row='CHART_TYPE',
            title='Number of recalls and affected vehicle units by component',
            labels={"COMPONENT_CATEGORY": 'Component Category',
                    "COMPONENT_NAME": 'Component Name'}
        )

        fig.for_each_annotation(lambda a: a.update(text=''))

        y_titles = {'x2': 'Recalls', 'x': 'Vehicle units'}
        fig.for_each_yaxis(lambda y: y.update(title=y_titles[y.anchor]))

        fig.update_yaxes(matches=None)
        fig.update_layout(hovermode="x")
        fig.update_traces(hovertemplate=None)

        return fig

    def get_affected_units_distribution_chart(self) -> Figure:
        reported_recalls_and_affected_units = self.recalls.get_reported_recalls_and_affected_units()

        if (reported_recalls_and_affected_units.empty):
            return {}

        fig = px.violin(
            reported_recalls_and_affected_units,
            y='AFFECTED_UNITS',
            labels={'AFFECTED_UNITS': 'Vehicle units'},
            color_discrete_sequence=px.colors.qualitative.T10,
            title='Number of affected vehicle units distribution'
        )

        fig.update_layout(yaxis_title=None, xaxis_title=None)

        return fig

    def get_recalls_and_affected_units_by_vehicle_chart(self) -> Figure:
        recalls_and_affected_units_by_vehicle = self.recalls.get_recalls_and_affected_units_by_vehicle()

        if (recalls_and_affected_units_by_vehicle.empty):
            return {}

        fig = make_subplots(rows=2, cols=1)
        x = recalls_and_affected_units_by_vehicle['VEHICLE']
        manufacturer = recalls_and_affected_units_by_vehicle['MANUFACTURER']
        recalls_mean = recalls_and_affected_units_by_vehicle['RECALL_ID'].median()
        affected_units_mean = recalls_and_affected_units_by_vehicle['AFFECTED_UNITS'].median()

        fig.add_trace(
            go.Scatter(
                line=dict(color=px.colors.qualitative.T10[0]),
                x=x,
                y=recalls_and_affected_units_by_vehicle['RECALL_ID'],
                mode='markers',
                name='Recalls',
                hovertemplate='<b>Recalls</b>: %{y}' +
                '<br><b>Vehicle</b>: %{x}<br>' +
                '<b>Manufacturer</b>: %{text}',
                text=manufacturer,
                showlegend=False
            ),
            row=1,
            col=1
        )

        fig.add_trace(
            go.Scatter(
                line=dict(color=px.colors.qualitative.T10[1]),
                x=x,
                y=recalls_and_affected_units_by_vehicle['AFFECTED_UNITS'],
                mode='markers',
                name='Vehicle units',
                hovertemplate='<b>Vehicle Units</b>: %{y:.2f}' +
                '<br><b>Vehicle</b>: %{x}<br>' +
                '<b>Manufacturer</b>: %{text}',
                text=manufacturer,
                showlegend=False
            ),
            row=2,
            col=1
        )

        fig.add_hline(
            y=recalls_mean,
            line_width=3,
            row=1,
            col=1,
            line_dash="dash",
            annotation_text="Recalls median")

        fig.add_hline(
            y=affected_units_mean,
            line_width=3,
            row=2,
            col=1,
            line_dash="dash",
            annotation_text="Vehicle units median")

        fig.update_layout(
            title_text='Number of recalls and affected vehicle units by vehicle',
        )

        y_titles = {'x': 'Recalls', 'x2': 'Vehicle units'}
        fig.for_each_yaxis(lambda y: y.update(title=y_titles[y.anchor]))

        fig.update_xaxes(showticklabels=False, categoryorder="total descending")

        return fig

    def get_recalls_distribution_chart(self) -> Figure:
        recalls_distribution = self.recalls.get_recalls_distribution()

        if (recalls_distribution.empty):
            return {}

        fig = px.scatter(
            recalls_distribution,
            y='VEHICLE_MODEL',
            x='AFFECTED_UNITS',
            hover_name='RECALL_ID',
            hover_data=['MANUFACTURER', 'REPORTED_DATE'],
            color_discrete_sequence=px.colors.qualitative.T10,
            labels={'VEHICLE_MODEL': 'Recalled vehicles',
                    'AFFECTED_UNITS': 'Vehicle units',
                    'MANUFACTURER': 'Manufacturer',
                    'REPORTED_DATE': 'Reported Date'},
            title='Recalls distribution by number of affected units and vehicles recalled'
        )

        return fig
