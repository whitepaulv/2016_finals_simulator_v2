import streamlit as st

# Initialize state
if "button_pressed" not in st.session_state:
    st.session_state.button_pressed = False

# Define the click handler
def handle_click():
    st.session_state.button_pressed = True

# Only show button if not yet pressed
if not st.session_state.button_pressed:
    st.button("Click me once", on_click=handle_click)
else:
    st.info("Button is gone now. Refresh to see it again.")