import streamlit as st

def init_session():
    if 'groups' not in st.session_state:
        st.session_state.groups = []
    if 'group_values' not in st.session_state:
        st.session_state.group_values = {}