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
st.markdown("This is the dataset we used")

df = pd.read_csv("singapore_housing_prices_750.csv")
st.write(df)

#Let's show a bar chart
region_sum_transaction = px.bar(df, 
x="Planning Region", 
y="Transacted Price ($)", 
title = "Transaction Price per Region")

st.plotly_chart(region_sum_transaction)

#Let's show a bar chart
type_sum_transaction = px.bar(df, 
x="Property Type", 
y="Transacted Price ($)", 
title = "Transaction Price per Property Type")

st.plotly_chart(type_sum_transaction)

#Let's show a scatter plot
area_unit_price = px.scatter(df,
x="Area (SQM)",
y="Unit Price ($ PSM)",
title="Correlation between Area and Unit Price")

st.plotly_chart(area_unit_price)

#Let's show a line chart
time_unit_price = px.line(df,
x="Sale Date",
y="Transacted Price ($)",
title="Transacted Price Across Time")

st.plotly_chart(time_unit_price)

#Let's show a histogram
area_histogram = px.histogram(df,
x="Area (SQM)")

st.plotly_chart(area_histogram)