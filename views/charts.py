import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class ChartsView(object):
    def __init__(self):
        with st.container():
            st.header('Charts')
            self.view()

    def view(self):
        if 'recalls' in st.session_state:
            with st.container():
                df = st.session_state.recalls.get_data()
                df_manufacturers = st.session_state.recalls.get_data(True)

                # Total de recalls por ano
                df_year_and_id = df[['RCDATE', 'CAMPNO']].drop_duplicates()
                group_by_year = df_year_and_id['RCDATE'].groupby(
                    df_year_and_id['RCDATE'].dt.year).count()
                fig = px.line(
                    x=group_by_year.index,
                    y=group_by_year.values,
                    labels={"x": "Ano", "y": "Recalls"},
                    title='Número de recalls por ano para fabricante'
                )
                fig.update_layout(yaxis_title=None, xaxis_title=None)
                st.plotly_chart(fig, use_container_width=True)

                # Total de recalls por ano
                group_by_manufacturer = df[['COMPNAME_GROUP', 'CAMPNO']].drop_duplicates(
                ).groupby('COMPNAME_GROUP').count()
                group_by_manufacturer.reset_index(inplace=True)

                trace1 = go.Bar(
                    x=group_by_manufacturer['COMPNAME_GROUP'],
                    y=group_by_manufacturer['CAMPNO'],
                    name='Bar Plot',
                    marker=dict(color=px.colors.sequential.Blues_r[0]),
                )

                manufacturer_avg = (df_manufacturers[[
                                             'COMPNAME_GROUP', 'CAMPNO']]
                                             .drop_duplicates()
                                             .groupby('COMPNAME_GROUP').avg())
               manufacturer_avg = manufacturer_avg[manufacturer_avg['COMPNAME_GROUP'].isin(group_by_manufacturer['COMPNAME_GROUP'])]
                
                avg_components = manufacturer_avg[]['COMPNAME_GROUP']
                trace2 = go.Scatter(
                    x=,
                    y=df['cumulative_perc'],
                    name='Cumulative Percentage',
                    yaxis='y2'
                )

                """fig2 = px.bar(
                    group_by_manufacturer,
                    x='COMPNAME_GROUP',
                    y='CAMPNO',
                    labels={"COMPNAME_GROUP": "", "CAMPNO": ""},
                    title=f"Número de recalls por categoria",
                    text_auto=True
                )
                fig2.update_layout(hovermode=False)
                fig2.update_xaxes(categoryorder="total descending")"""

                fig2 = make_subplots(specs=[[{"secondary_y": True}]])

                fig2.add_trace(trace1)

                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.write('Faça upload dos dados para visualizar os gráficos.')
