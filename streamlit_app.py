import streamlit as st

from astropy.time import Time
import astropy.units as u
from astropy.coordinates import AltAz, EarthLocation, SkyCoord, get_body, get_sun
import numpy as np
import pandas as pd
import plotly.graph_objects as go



st.title("🎈 My new Streamlit app🎈")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
