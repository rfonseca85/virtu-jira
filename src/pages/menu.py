import streamlit as st
from streamlit_option_menu import option_menu
import src.pages.project_cost as project_cost
import src.pages.project_scope as project_scope
import src.pages.settings as settings

def page():

    # CSS style definitions
    custom_css = f"""
    <style>
        [data-testid="stSidebarNav"]::before {{
            content: "Virtu.jira";
            margin-left: 40px;
            font-size: 30px;
            position: relative;
            top: 50px;
            color: #8b8b8e;
        }}
        
        .st-emotion-cache-lrlib {{
            max-height: 100vh;
            list-style: none;
            overflow: overlay;
            margin: 0px;
            padding-top: 5rem;
            padding-bottom: 1rem;
        }}
        
        .stDeployButton {{
            visibility: hidden;
        }}
        footer {{
            visibility: hidden;
        }}
        
        .marks  {{
            width: 95%;
        }}
        
        # .st-emotion-cache-vk3wp9 {{
        #     background-color: white;
        # }}
        
        .st-emotion-cache-ztfqz8 {{
            visibility: hidden;
        }}
        
        [data-testid="stFileUploader"] {{
            width: 95%;
        }}
        
        [data-testid="stFileUploadDropzone"] {{
            background-color: #F0F0F0;
        }}
        
        .st-emotion-cache-1q7spjk {{
            width: 95%;
            color: black;
        }}

        .st-emotion-cache-1wmy9hl {{
            max-width: 1100px;
        }}

        .st-emotion-cache-2lh61o {{
            width: 100%;
        }}
                 
    </style>
    """

    # Use the CSS in Streamlit
    st.markdown(custom_css, unsafe_allow_html=True)


    with st.sidebar:
        # CSS style definitions
        company_name = "Virtu.jira"
        menu_selected = option_menu(company_name, ["Project Cost", "Project Scope (TBD)", 'Settings'],
                                    icons=['currency-dollar', 'bar-chart', "gear"],
                                    menu_icon="rocket-takeoff", default_index=0, orientation="vertical")
        
    
    if menu_selected == "Project Cost":
        return project_cost.main()
    elif menu_selected == "Project Scope (TBD)":
        return project_scope.main()
    elif menu_selected == "Settings":
        return settings.main()
    else:
        return st.write("Error")
    




