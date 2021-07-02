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
st.markdown("From this bar chart, we can see that the Property Type with Highest Average Unit Price in Singapore is Apartments, followed by Condominiums, Detached Houses, Terrace Houses, Semi-Detached Houses, and lastly, Executive Condominium.")

#df3 = df.groupby(['Area (SQM)'])['Unit Price ($ PSF)'].mean().to_frame().reset_index()
#Let's show a scatter plot
#area_unit_price = px.scatter(df3,
#x="Area (SQM)",
#y="Unit Price ($ PSF)",
#title="Correlation between Area and Unit Price")

#st.plotly_chart(area_unit_price)

by_month = pd.to_datetime(df['Sale Date']).dt.to_period('M').value_counts().sort_index()
by_month.index = pd.PeriodIndex(by_month.index)
df_month = by_month.rename_axis('Sale Month').reset_index(name='counts')

trans = go.Figure(data=go.Scatter(x=df_month['Sale Month'].astype(dtype=str), 
                        y=df_month['counts'],
                        marker_color='indianred', text="counts"))
trans.update_layout({"title": 'Number of Transactions from Jan 2018 to Dec 2020',
                   "xaxis": {"title":"Months"},
                   "yaxis": {"title":"Number of transactions"},
                   "showlegend": False})

#df4 = df.groupby(['Sale Date'])['Unit Price ($ PSM)'].mean().to_frame().reset_index()
#Let's show a line chart
#time_unit_price = px.line(df4,
#="Sale Date",
#y="Unit Price ($ PSM)",
#title="Unit Price Across Time")

st.plotly_chart(trans)

st.markdown("The above line chart shows the number of transactions throughout 3 years from 2018 to 2020. We can see that the number of transactions of private properties in Singapore fluctuates quite drastically. This is because housing prices are affected by a lot of external factors such as interest rate, the macroeconomic condition, etc.")