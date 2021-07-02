import price_prediction
import understand_model
import dashboard
import streamlit as st

PAGES = {
    "Get price prediction": price_prediction,
    "Understand our Data": dashboard,
    "Understand our Model": understand_model,
}

st.sidebar.title('Singapore Private Property Price Prediction')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
