import plotly.express as px
import pandas as pd
from dash import dcc

def get_horizontal_bar_chart(df: pd.DataFrame) -> None:
    fig = px.bar(
        x=df.values,
        y=df.index,
        orientation='h',
        labels={"x": "", "y": ""},
        color_discrete_sequence=px.colors.sequential.Blues_r,
        height=800
    )

    fig.update_yaxes(
        categoryorder="total ascending",
        tickfont=dict(size=10)
    )

    fig.update_traces(
        hovertemplate = '%{x:,}'
    )

    return dcc.Graph(figure=fig, style={'height': '100%', 'width': '100%'})