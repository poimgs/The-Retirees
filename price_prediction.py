import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import sklearn
import shap
import requests
import json
import pickle
import pandas as pd
from math import sin, cos, sqrt, atan2, radians

EMAIL = st.secrets["EMAIL"]
PASSWORD = st.secrets["PASSWORD"]

with open('finalized_model.pkl', 'rb') as file:
    model = pickle.load(file)

st.set_page_config(
    page_title="Singapore Private Property Price Prediction",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_token(EMAIL, PASSWORD):
    data = {
        'email': EMAIL,
        'password': PASSWORD
    }

    res = requests.post(
        'https://developers.onemap.sg/privateapi/auth/post/getToken', json=data)

    return res.json()['access_token']


def get_lat_long(address):
    url = "https://developers.onemap.sg/commonapi/search?returnGeom=Y&getAddrDetails=Y&pageNum=1&searchVal=" + address
    response = requests.get(url)
    data = json.loads(response.text)
    if data['found'] == 0:
        return -1, -1
    elif data['found'] > 0:
        results = data['results'][0]
        latitude, longitude = results['LATITUDE'], results['LONGITUDE']
        return float(latitude), float(longitude)


def get_distance(start_lat, end_lat, start_long, end_long):
    R = 6373.0

    start_lat = radians(start_lat)
    end_lat = radians(end_lat)
    start_long = radians(start_long)
    end_long = radians(end_long)

    dlon = end_long - start_long
    dlat = end_lat - start_lat

    a = sin(dlat / 2)**2 + cos(start_lat) * cos(end_lat) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def get_walking_distance(start_lat, start_long):
    read_mrt_lat_long = pd.read_csv('mrtsg.csv')
    distance = 100000000000000000000000000000000
    selected_lat = 0
    selected_long = 0

    for mrt in range(len(read_mrt_lat_long)):
        end_lat = read_mrt_lat_long['Latitude'].iloc[mrt]
        end_long = read_mrt_lat_long['Longitude'].iloc[mrt]

        current_distance = get_distance(
            start_lat, end_lat, start_long, end_long)

        if current_distance < distance:
            distance = current_distance
            selected_lat = end_lat
            selected_long = end_long

    TOKEN = get_token(EMAIL, PASSWORD)
    url = "https://developers.onemap.sg/privateapi/routingsvc/route?" + \
        "start=" + str(start_lat) + "," + str(start_long) + \
        "&end=" + str(end_lat) + "," + str(end_long) + \
        "&routeType=walk" + '&token=' + TOKEN
    response = requests.get(url)
    data = response.json()
    if 'error' not in data.keys():
        walking_distance = data['route_summary']['total_distance']
    else:
        walking_distance = 0

    return walking_distance


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


def st_shap(plot, height=None):
    shap_html = f"<head>{shap.getjs()}</head><body>{plot.html()}</body>"
    components.html(shap_html, height=height)


def shap_plot(model, transformed_user_input):
    column_names = ['Area (SQFT)', 'Floor', 'Remaining Tenure', 'Is Freehold',
                    'walk_distance', 'Condo_Apartment', 'Landed', 'East Region',
                    'North East Region', 'North Region', 'West Region', 'Resale',
                    'Sub Sale']
    X = pd.DataFrame(transformed_user_input, columns=column_names)
    explainer = shap.TreeExplainer(model.best_estimator_)
    shap_values = explainer.shap_values(X)

    st_shap(shap.force_plot(explainer.expected_value,
            shap_values[0, :], X.iloc[0, :]))


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
        walking_distance = get_walking_distance(latitude, longitude)

        if len(unit_num) > 0:
            # unit #01-01 gives you level 1
            floor_lvl = float(unit_num.split("-")[0][1:].lstrip("0"))
        else:
            floor_lvl = 1.0

        # Get result below here!
        if freehold == 'Yes':
            freehold = 1
        else:
            freehold = 0

        transformed_user_input = transform_user_input(
            area_sqft, floor_lvl, tenure, freehold, walking_distance, property_type, region, sale_type)
        predicted_unit_price = model.predict(transformed_user_input)[0]
        predicted_total_price = predicted_unit_price * area_sqft

        st.write(f'''
        We predict your house to be worth **${int(predicted_total_price):,}** (${int(predicted_unit_price)}/sqft)!

        Below are the factors that the model has considered for this prediction
        ''')

        shap_plot(model, transformed_user_input)
