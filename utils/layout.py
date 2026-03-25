# utils/layout.py

import streamlit as st

def style_task_card():
    return {
        "background_color": "#202736",
        "padding": "15px",
        "border_radius": "10px",
        "margin_bottom": "10px"
    }

def style_done_task():
    return {
        "background_color": "#555555",
        "color": "#dddddd",
        "padding": "15px",
        "border_radius": "10px",
        "margin_bottom": "10px"
    }