import streamlit as st
from views.about import AboutView
from views.data import DataView
from views.charts import ChartsView

pages = st.source_util.get_pages('main.py')
new_page_names = {
  'app': 'NHTSA Recalls',
  'about': 'Sobre o projeto',
  'faq': 'FAQ',
}

for key, page in pages.items():
    if page['page_name'] in new_page_names:
        page['page_name'] = new_page_names[page['page_name']]

AboutView()
DataView()
ChartsView()
