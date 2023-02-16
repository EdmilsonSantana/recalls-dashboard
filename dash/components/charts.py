import plotly.express as px
from plotly.graph_objects import Figure
import pandas as pd


def get_bar_chart(x: pd.Series, y: pd.Series, title: str) -> Figure:
    if (len(x) == 0 or len(y) == 0):
        return {}

    return px.bar(
        x=x,
        y=y,
        labels={"x": "", "y": ""},
        color_discrete_sequence=px.colors.sequential.Blues_r,
        title=title,
        text_auto=True
    )


def get_horizontal_bar_chart(df: pd.DataFrame) -> Figure:
    if (df.empty):
        return {}

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
        hovertemplate='%{x:,}'
    )

    return fig


def get_line_chart(x: pd.Series, y: pd.Series, labels: dict, title: str) -> Figure:
    if (len(x) == 0 or len(y) == 0):
        return {}

    fig = px.line(
        y=y,
        x=x,
        labels=labels,
        color_discrete_sequence=px.colors.sequential.Blues_r,
        title=title
    )

    fig.update_layout(yaxis_title=None, xaxis_title=None)

    return fig

def get_scatter_plot(df: pd.DataFrame, x: str, y: str, color: str, title: str, labels: dict) -> Figure:
    if (df.empty):
        return {}

    fig = px.scatter(df, x=x, y=y, color=color, title=title, labels=labels)

    fig.update_layout(yaxis_title=None, xaxis_title=None)

    return fig

