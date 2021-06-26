import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

data_url = ("The-Retirees/singapore_housing_prices_750.xlsx")
def load_data():
    df = pd.read_excel(data_url)
    return df

#Title of dashboard
st.title("Singapore Private Property Dashboard")
st.markdown("This dashbaord will visualize the current landscaape of privaate properties in Singapore")

#Let's show the dataset
st.write(df)
