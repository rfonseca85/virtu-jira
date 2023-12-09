import streamlit as st
import src.pages.menu as menu
# Return the selected Page content
st.set_page_config(
    page_title="Virtu.jira",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded",
)

menu.page()





