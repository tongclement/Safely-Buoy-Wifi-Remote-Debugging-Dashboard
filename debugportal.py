import time  # to simulate a real time data, time loop

import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development
import geopy.distance # distance to home point
import requests
import datetime

st.set_page_config(
    page_title="Real-Time Buoy Dashboard",
    page_icon="✅",
    layout="wide",
)

# read csv from a github repo
#dataset_url = "https://raw.githubusercontent.com/Lexie88rus/bank-marketing-analysis/master/bank.csv"

time.sleep(5) #allow user to switch from public to local network

# get df
telemetry = requests.get('http://192.168.4.1')
print(telemetry.text)
telemetryjson=telemetry.json()
telemetryjson.update({"time":datetime.datetime.utcnow().isoformat()})

#Add distance to home point calculated by python
current_lat=telemetryjson.get("Current Lat")
current_long=telemetryjson.get("Current Long")
home_lat=telemetryjson.get("Home Lat")
home_long=telemetryjson.get("Home Long")
current_pos = (current_lat, current_long)
home_pos = (home_lat, home_long)
print(current_pos)
calculated_distnace_to_home=geopy.distance.geodesic(current_pos, home_pos).m
telemetryjson.update({"Dist To Home":calculated_distnace_to_home})

print(telemetryjson)
telemdf = pd.DataFrame(telemetryjson, index=[datetime.datetime.now().isoformat()])

# dashboard title
st.title("SafelyBuoy Real Time Dashboard")

# top-level filters

# creating a single-element container
placeholder = st.empty()


# near real-time / live feed simulation
while True:
    telemetry = requests.get('http://192.168.4.1')
    telemetryjson = telemetry.json()
    telemetryjson.update({"time": datetime.datetime.utcnow().isoformat()})

    # Add distance to home point calculated by python
    current_lat = telemetryjson.get("Current Lat")
    current_long = telemetryjson.get("Current Long")
    home_lat = telemetryjson.get("Home Lat")
    home_long = telemetryjson.get("Home Long")
    current_pos = (current_lat, current_long)
    home_pos = (home_lat, home_long)
    print(current_pos)
    calculated_distnace_to_home = geopy.distance.geodesic(current_pos, home_pos).m
    telemetryjson.update({"Dist To Home": calculated_distnace_to_home})

    print(telemetryjson)

    tobeappended = pd.DataFrame(telemetryjson, index=[datetime.datetime.now().isoformat()])
    telemdf = pd.concat([telemdf, tobeappended])
    print(f"telemdf {telemdf}")
    dftail= telemdf.tail(1)
    print(f"dftail {dftail}")
    current_hdg = dftail["Current Hdg"].values[0]
    target_hdg = dftail["Target Hdg"].values[0]
    current_vel = dftail["Current vel"].values[0]
    target_vel = dftail["Target vel"].values[0]
    mtr_pct=dftail["Current Motor Setting"].values[0]
    rudder_config=dftail["Rudder Config Var"].values[0]
    current_lat=dftail["Current Lat"].values[0]
    current_long=dftail["Current Long"].values[0]
    home_lat=dftail["Home Lat"].values[0]
    home_long=dftail["Home Long"].values[0]
    print(type(target_hdg))


    with placeholder.container():
        # create three columns
        kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

        # fill in those three columns with respective metrics or KPIs
        kpi1.metric(
            label="Current Heading",
            value=round(current_hdg,2),
            delta=round(target_hdg-current_hdg,2),
        )

        kpi2.metric(
            label="Target Heading",
            value=round(target_hdg,2)
        )

        kpi3.metric(
            label="Current Velocity",
            value=f"{current_vel} m/s",
            delta=target_vel-current_vel,
        )

        kpi4.metric(
            label="Target Velocity",
            value=f"{target_vel} m/s",
        )

        kpi5.metric(
            label="Distance To Home (m)",
            value=calculated_distnace_to_home,
        )

        kpi6, kpi7, kpi8, kpi9, kpi10 = st.columns(5)
        kpi6.metric(
            label="Motor Power Setting (%)",
            value=mtr_pct,
        )

        kpi7.metric(
            label="Rudder Deflection",
            value=round(rudder_config,3),
            help="50 = neutral"
        )

        # create two columns for charts
        fig_col1, fig_col2, fig_col3 = st.columns(3)
        with fig_col1:
            st.markdown("### Distance To Home")
            fig = px.line(data_frame=telemdf, x="time", y="Dist To Home",)
            st.write(fig)

        with fig_col2:
            st.markdown("### Heading")
            fig2 = px.line(data_frame=telemdf, x="time", y="Current Hdg")
            st.write(fig2)

        with fig_col3:
            st.markdown("### Velocity")
            fig3 = px.line(data_frame=telemdf, x="time", y="Current vel")
            st.write(fig3)

        fig_col4, fig_col5, fig_col6 = st.columns(3)
        with fig_col4:
            st.markdown("### Motor Power Setting")
            fig4 = px.line(data_frame=telemdf, x="time", y="Dist To Home")
            st.write(fig4)

        with fig_col5:
            st.markdown("### Target Heading")
            fig5 = px.line(data_frame=telemdf, x="time", y="Target Hdg")
            st.write(fig5)

        with fig_col6:
            st.markdown("### Target Velocity")
            fig6 = px.line(data_frame=telemdf, x="time", y="Target vel")
            st.write(fig6)

        fig_col7, fig_col8, fig_col9 = st.columns(3)
        with fig_col7:
            st.markdown("### Rudder Deflection")
            fig7 = px.line(data_frame=telemdf, x="time", y="Rudder Config Var")
            st.write(fig7)


        st.markdown("### Telemtry Dataframe")
        st.dataframe(telemdf)
        time.sleep(0.25)


#reference
#official streamlit documentation: https://blog.streamlit.io/how-to-build-a-real-time-live-dashboard-with-streamlit/#1-how-to-import-the-required-libraries-and-read-input-data