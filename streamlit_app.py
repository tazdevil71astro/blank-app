import streamlit as st

from astropy.time import Time
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_body, get_sun
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import datetime

from app_functions import transfo_date_to_isostr

#Definition site observation : tour de Belem à Lisbonne
site_lat = 38.67201
site_long = -9.23275
site_alt = 10
site_utc_offset = 0

ARO = EarthLocation(lat = site_lat * u.deg,
                    lon = site_long * u.deg,
                    height = site_alt * u.m)

# Widget Choix date initialisée à la date du jour
today_date = datetime.date.today()

input_date = st.date_input("Choisir une nuit d'observation :",
                datetime.date(today_date.year,
                    today_date.month, 
                    today_date.day),
                format = "DD/MM/YYYY")


#Transformation de la date sélectionnée au format str isot pour utilisation dans le graphe
st.write("Nuit choisie format date :", input_date)
st.write("Nuit choisie format str isot :", transfo_date_to_isostr(input_date))



Day_obs = transfo_date_to_isostr(input_date)



# Chargement fichier des cibles dans un data frame
pd_infos_cibles = pd.read_csv("TEST_IMPORT_EPHEMERIDES.csv",sep = ";")
                              

st.title("🎈 Graphique cible Nuit🎈")

T_Day_obs_utc = Time(Day_obs,format ='isot',scale ='utc') - site_utc_offset*u.hour #UTC
T_Day_obs_np64 = np.datetime64(Day_obs)

#creation des heures d'obs (16h - 9h) ramenées en utc
delta = np.arange(240,1261,1) * u.minute
times_day_obs_utc = T_Day_obs_utc + delta


date_range_heure = np.arange(T_Day_obs_np64+np.timedelta64(240,'m'), T_Day_obs_np64+np.timedelta64(1261,'m'), np.timedelta64(1, 'm'))

fig = go.Figure()

frame_date = AltAz(obstime=T_Day_obs_utc + delta, location=ARO)

#Parcours du fichier lu pour tracer les altitudes de toutes les cibles
for j in range(2):
    tmp_cible_coord = SkyCoord(float(pd_infos_cibles['RA'][j].replace(',','.')),
                               float(pd_infos_cibles['DEC'][j].replace(',','.')),
                               unit="deg")
    tmp_cible_altaz = tmp_cible_coord.transform_to(frame_date)
    fig.add_trace(go.Scatter(x=date_range_heure, y=tmp_cible_altaz.alt,mode='lines',
                        name = pd_infos_cibles['Cible'][j] + "- lune à 70°"))
   
#fig.update_layout(plot_bgcolor='white')
fig.update_yaxes(range=[0, 90])


st.plotly_chart(fig)
