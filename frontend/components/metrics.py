import streamlit as st


def display_kpi(
    title,
    value,
    description=None,
):

    st.metric(
        label=title,
        value=value,
        help=description,
    )