import streamlit as st
import plotly.express as px


class ChartsView(object):
    def __init__(self):
        with st.container():
            st.header('Charts')
            self.view()

    def view(self):
        if 'recalls' in st.session_state:
            with st.container():
                df = st.session_state.recalls.get_data()
                group_by_year = df['RCDATE'].groupby(
                    df['RCDATE'].dt.year).count()
                fig = px.line(
                    x=group_by_year.index,
                    y=group_by_year.values,
                    labels={"x": "Ano", "y": "Recalls"},
                    title='Número de recalls'
                )
                fig.update_layout(yaxis_title=None, xaxis_title=None)

                st.plotly_chart(fig, use_container_width=True)
        else:
            st.write('Faça upload dos dados para visualizar os gráficos.')
