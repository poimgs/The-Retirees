import streamlit as st
import sklearn
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


def transform_user_input(area, floor, remaining_tenure, is_freehold, walking_distance, property_type, region, type_of_sale):
    transformed_input = [area, floor, remaining_tenure,
                         is_freehold, walking_distance]

    if property_type == "Apartment or Condominium":
        transformed_input.append(1)
        transformed_input.append(0)
    elif property_type == "Executive Condominium":
        transformed_input.append(0)
        transformed_input.append(0)
    else:
        transformed_input.append(0)
        transformed_input.append(1)
    if region == "East":
        transformed_input.append(1)
        transformed_input.append(0)
        transformed_input.append(0)
        transformed_input.append(0)
    elif region == "North East":
        transformed_input.append(0)
        transformed_input.append(1)
        transformed_input.append(0)
        transformed_input.append(0)
    elif region == "North":
        transformed_input.append(0)
        transformed_input.append(0)
        transformed_input.append(1)
        transformed_input.append(0)
    elif region == "West":
        transformed_input.append(0)
        transformed_input.append(0)
        transformed_input.append(0)
        transformed_input.append(1)
    else:
        transformed_input.append(0)
        transformed_input.append(0)
        transformed_input.append(0)
        transformed_input.append(0)
    if type_of_sale == "Resale":
        transformed_input.append(1)
        transformed_input.append(0)
    elif type_of_sale == "Sub Sale":
        transformed_input.append(0)
        transformed_input.append(1)
    else:
        transformed_input.append(0)
        transformed_input.append(0)

    return [transformed_input]


def app():
    st.write(
        '<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    with st.form('Form1'):
        cols = st.beta_columns((2, 1))
        address = cols[0].text_input(label='Address', value='6 Shunfu Road')
        unit_num = cols[1].text_input(label='Unit number', value='#01-01')

        cols = st.beta_columns(3)
        property_type = cols[0].selectbox(
            'Property Type', ('Apartment/ Condo', 'Executive Condo', 'Other Landed Properties'))
        sale_type = cols[1].selectbox(
            'Type of Sale', ('New Sale', 'Resale', 'Sub Sale'))
        region = cols[2].selectbox(
            'Region', ('North', 'North East', 'East', 'West', 'Central'))

        area_sqft = st.number_input('Area SQFT')

        cols = st.beta_columns((1, 2))
        freehold = cols[0].radio('Freehold', ('Yes', 'No'))
        tenure = cols[1].number_input(
            'Remaining Tenure (If not freehold)', format='%d', step=1)

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        latitude, longitude = get_lat_long(address)
        # need to calculate walking distance to nearest MRT

        if len(unit_num) > 0:
            # unit #01-01 gives you level 1
            floor_lvl = float(unit_num.split("-")[0][1:].lstrip("0"))

        # Get result below here!
        if freehold == 'Yes':
            freehold = 1
        else:
            freehold = 0

        st.write('We are still a work in progress, come back in a week and you will be able to see your how much your house is worth!')
