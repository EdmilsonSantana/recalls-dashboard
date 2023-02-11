import streamlit as st
from data.recalls import Recalls


class DataView(object):
    def __init__(self):
        with st.container():
            st.header('Data Processing')
            self.view()

    def on_change_upload_file(self):
        if st.session_state.file_uploader is not None:
            with st.spinner('Processando dados...'):
                st.session_state.recalls = Recalls(
                    st.session_state.file_uploader)

    def view(self):
        with st.container():
            st.file_uploader('Upload FLAT_RCL.txt',
                             key='file_uploader',
                             type=['.txt'],
                             on_change=self.on_change_upload_file)

        with st.container():
            if 'recalls' in st.session_state:
                data_time_range = st.session_state.recalls.get_date_range()

                time_range = st.slider(
                    'Período de análise', data_time_range[0], data_time_range[1], (data_time_range[0], data_time_range[1]))

                manufacturer = st.selectbox("Fabricante",
                                            options=st.session_state.recalls.get_manufacturers())

                available_vehicles = st.session_state.recalls.get_vehicles_by_manufacturer(manufacturer)
                vehicle = st.selectbox("Veículo",
                                       options=['-', *available_vehicles])

                if (time_range or manufacturer):
                    with st.spinner('Buscando...'):
                        self.get_details(time_range, manufacturer, vehicle)

    def get_details(self, time_range, manufacturer, vehicle):
        df = st.session_state.recalls.filter_by(
            time_range, manufacturer, vehicle)

        if (df is None):
            st.info('No data found', icon="ℹ️")
        else:
            with st.container():
                st.dataframe(df)
                st.download_button(
                    label="Download",
                    data=df.to_csv().encode('utf-8'),
                    file_name='recalls.csv',
                    mime='text/csv',
                )
