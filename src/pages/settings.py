import streamlit as st
from src.jira_config import jira

def main():
    st.title("Settings")

    jira_email = st.text_input("Jira Email", value=jira['email'])
    jira_api_token = st.text_area("Jira API Token", value=jira['api_token'])
    jira_server = st.text_input("Jira Server", value=jira['server'])
    save_b = st.button("Save")
    if save_b:
        with open("src/jira_config.py", "w") as f:
            f.write(f"jira = {{\n\t'email': '{jira_email}',\n\t'api_token': '{jira_api_token}',\n\t'server': '{jira_server}'\n}}")
        st.success('Settings saved!', icon="✅")

