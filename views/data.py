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
                st.session_state.recalls = Recalls(st.session_state.file_uploader)

    def view(self):
        with st.container():
            st.file_uploader('Upload FLAT_RCL.txt',
                             key='file_uploader',
                             type=['.txt'],
                             on_change=self.on_change_upload_file)

        with st.container():
            if 'recalls' in st.session_state:
                manufacturer = st.selectbox("Manufacturer",
                                            st.session_state.recalls.get_manufacturers())
                recall_id = st.selectbox("Recall ID",
                                         st.session_state.recalls.get_ids_by_manufacturer(manufacturer))
                if (manufacturer):
                    with st.spinner('Buscando...'):
                        self.get_details(manufacturer, recall_id)

    def get_details(self, manufacturer, recall_id):
        df = st.session_state.recalls.filter_by(manufacturer, recall_id)

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
