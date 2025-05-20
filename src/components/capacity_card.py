import streamlit as st
from streamlit_extras.badges import badge

# Componente visual para exibir métricas de capacidade

def capacity_card(title, value, unit, icon=None, color="#4F8BF9", description=None):
    card_style = f"""
        background: white;
        border-radius: 1.2rem;
        box-shadow: 0 2px 8px 0 rgba(0,0,0,0.08);
        padding: 1.5rem 1.5rem 1.2rem 1.5rem;
        margin-bottom: 1.2rem;
        border-left: 8px solid {color};
    """
    st.markdown(f"""
    <div style='{card_style}'>
        <div style='display: flex; align-items: center;'>
            {f"<span style='font-size:2.2rem;margin-right:0.7rem;'>{icon}</span>" if icon else ''}
            <div>
                <div style='font-size:1.1rem; color:#888;'>{title}</div>
                <div style='font-size:2.1rem; font-weight:700; color:{color};'>{value} <span style='font-size:1.1rem; color:#444;'>{unit}</span></div>
            </div>
        </div>
        {f"<div style='margin-top:0.5rem; color:#666; font-size:1rem;'>{description}</div>" if description else ''}
    </div>
    """, unsafe_allow_html=True) 