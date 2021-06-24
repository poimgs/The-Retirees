import streamlit as st
import requests
import json

st.set_page_config(
    page_title="Singapore Private Property Price Prediction",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
    )


def get_lat_long(address):
    url = "https://developers.onemap.sg/commonapi/search?returnGeom=Y&getAddrDetails=Y&pageNum=1&searchVal=" + address
    response = requests.get(url)
    data = json.loads(response.text)
    if data['found'] == 0:
        return -1, -1
    elif data['found'] > 0:
        results = data['results'][0]
        latitude, longitude = results['LATITUDE'], results['LONGITUDE']
        return latitude, longitude


def app():
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    with st.form('Form1'):
        cols = st.beta_columns((2,1))
        address = cols[0].text_input(label='Address', value='6 Shunfu Road')
        unit_num = cols[1].text_input(label='Unit number', value='#01-01')

        cols = st.beta_columns(3)
        property_type = cols[0].selectbox('Property Type', ('Apartment/ Condo', 'Executive Condo', 'Other Landed Properties'))
        sale_type = cols[1].selectbox('Type of Sale', ('New Sale', 'Resale', 'Sub Sale'))
        region = cols[2].selectbox('Region', ('North', 'North East', 'East', 'West', 'Central'))
        
        area_sqft = st.number_input('Area SQFT')
        

        cols = st.beta_columns((1,2))
        freehold = cols[0].radio('Freehold', ('Yes','No'))
        tenure = cols[1].number_input('Remaining Tenure (If not freehold)', format ='%d', step=1)

        submit_button = st.form_submit_button(label='Submit')
        if submit_button:
            latitude, longitude = get_lat_long(address) 
            # need to calculate walking distance to nearest MRT

            if len(unit_num) > 0:
                floor_lvl = float(unit_num.split("-")[0][1:].lstrip("0")) # unit #01-01 gives you level 1
                
                
            
       
