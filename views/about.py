import streamlit as st


class AboutView(object):
    def __init__(self):
        st.set_page_config(page_title='NHTSA Recalls')
        with st.container():
            st.image('./assets/logo.png')
            st.title('NHTSA Recalls')
            st.write('''O objetivo deste dashboard é fornecer uma visão rápida e 
                abrangente dos dados de recalls da NHTSA e ajudá-lo a descobrir
                quais componentes estão envolvidos em recalls mais frequentemente.''')
            st.write(
                'Você pode fazer download do arquivo **FLAT_RCL.zip** na seção de recalls no [portal](https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL.zips) da NHTSA')
