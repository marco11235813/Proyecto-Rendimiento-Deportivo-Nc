import streamlit as st

st.set_page_config(page_title="Rendimiento Deportivo KPIs", layout="wide")

html_code = """
<div style='display: flex; flex-direction: column; align-items: center;'>
    <h1>Rendimiento Deportivo KPIs</h1>
    <iframe title="nocountry_rendimientodeportivo_kpis" width="600" height="373.5" 
    src="https://app.powerbi.com/view?r=eyJrIjoiOTI0OGM3MzUtNzIzZi00ODI0LTllNTItMmM2ZDRjNTljZWI0IiwidCI6ImRmODY3OWNkLWE4MGUtNDVkOC05OWFjLWM4M2VkN2ZmOTVhMCJ9" 
    frameborder="0" allowFullScreen="true"></iframe>
</div>
"""

st.markdown(html_code, unsafe_allow_html=True)

