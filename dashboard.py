import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#Title of dashboard
st.title("Singapore Private Property Dashboard")
st.markdown("This dashboard will visualize the current landscape of private properties in Singapore")

#Let's show the dataset
st.markdown("This is the dataset we used")

df = pd.read_csv("singapore_housing_prices.csv")
st.write(df)

df2 = df.groupby(['Planning Region'])['Unit Price ($ PSM)'].mean().to_frame().reset_index()
#Let's show a bar chart
region_sum_transaction = px.bar(df2, 
x="Planning Region", 
y="Unit Price ($ PSM)", 
title = "Average Unit Price ($ PSM) per Region")

st.plotly_chart(region_sum_transaction)
st.markdown("From this bar chart, we can see that the area with Highest Average Unit Price in Singapore is the Central Region, followed by the West Region, North East Region, East Region and lastly, the North Region.")

df1 = df.groupby(['Property Type'])['Unit Price ($ PSM)'].mean().to_frame().reset_index()
#Let's show a bar chart
type_sum_transaction = px.bar(df1, 
x="Property Type", 
y="Unit Price ($ PSM)", 
title = "Unit Price per Property Type")

st.plotly_chart(type_sum_transaction)
st.markdown("From this bar chart, we can see that the Property Type with Highest Average Unit Price in Singapore is Apartments, followed by Condominiums, Detached Houses, Terrace Houses, Semi-Detached Houses, and lastly, Executive Condominium."

#df3 = df.groupby(['Area (SQM)'])['Unit Price ($ PSF)'].mean().to_frame().reset_index()
#Let's show a scatter plot
#area_unit_price = px.scatter(df3,
#x="Area (SQM)",
#y="Unit Price ($ PSF)",
#title="Correlation between Area and Unit Price")

#st.plotly_chart(area_unit_price)

df4 = df.groupby(['Sale Date'])['Unit Price ($ PSM)'].mean().to_frame().reset_index()
#Let's show a line chart
time_unit_price = px.line(df4,
x="Sale Date",
y="Unit Price ($ PSM)",
title="Unit Price Across Time")

st.plotly_chart(time_unit_price)

#Let's show a histogram
#area_histogram = px.histogram(df,
#x="Area (SQM)")

#st.plotly_chart(area_histogram)