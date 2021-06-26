import price_prediction
import streamlit as st

PAGES = {
    "Get price prediction": price_prediction
}

st.sidebar.title('Singapore Private Property Price Prediction')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()