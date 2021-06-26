import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#Title of dashboard
st.title("Singapore Private Property Dashboard")
st.markdown("This dashbaord will visualize the current landscaape of private properties in Singapore")

#Let's show the dataset
df = pd.read_csv(singapore_housing_prices_750.csv)
st.write(df)
