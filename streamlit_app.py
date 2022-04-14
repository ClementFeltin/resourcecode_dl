from fileinput import filename
import streamlit as st
import pandas as pd
import plotly.express as px

import resourcecode

from utils import *
from data import *

#pd.options.plotting.backend = "plotly"

st.set_page_config(layout="wide")

st.title('ResourceCODE metocean data downloader')

texte = ['This app allows you to simply download csv metocean data from HOMERE hindcasts.\n',
'Please use it carefully.']
texte = ' '.join(texte)

st.write(texte)

st.write('The source code is available at [GitHub](https://github.com/ClementFeltin/resourcecode_dl). Feel free to share any issue or idea.')

latitude = st.sidebar.number_input('Latitude', 40., 50., 48.3, 0.01)
longitude = st.sidebar.number_input('Longitude', -10., 10., -4.6, 0.01)

selected_node = resourcecode.data.get_closest_point(
    latitude=latitude, longitude=longitude
)[0]

import plotly.express as px

df = pd.DataFrame(latitude=[latitude], longitude=[longitude])

fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", zoom=3, height=300)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


if st.button("Download dataset"):
    st.write('Download in progress')

    url = "https://resourcecode.ifremer.fr/explore?pointId=" + str(selected_node)# + "&startDateTime=2010-10-01T22%3A00%3A00.000Z&endDateTime=2012-09-30T22%3A00%3A00.000Z"

    client = resourcecode.Client()
    data = client.get_dataframe_from_url(
        url,
        parameters=("hs", "tp", "t02", "dir", "dp", "spr", "ucur", "vcur", "wlv", "uwnd", "vwnd", "dpt"),
    )


    data["wspd"], data["wdir"] = resourcecode.utils.zmcomp2metconv(data.uwnd, data.vwnd)
    data["uspd"], data["udir"] = resourcecode.utils.zmcomp2metconv(data.ucur, data.vcur)



    data = data[ws_cols].rename(dict(zip(ws_cols, ws_col_names)), axis=1)

    data["AAAA-MM-JJ"] = data.index.map(lambda x: str(x).split(" ")[0])
    data["HH-MM-SS"] = data.index.map(lambda x: str(x).split(" ")[1])

    period_min = pd.to_datetime(data["AAAA-MM-JJ"]).dt.year.min()
    period_max = pd.to_datetime(data["AAAA-MM-JJ"]).dt.year.max()

    data_ws = data[["AAAA-MM-JJ", "HH-MM-SS"] + ws_col_names]

    header = [f"Hydrodynamic parameters reconstituted on the {period_min} - {period_max} period",
    "Point {}".format(selected_node),
    f"Position lat, lon : {latitude}, {longitude}",
    f"Water depth / CD (m) : {data.depth.mean()}",
    ] + static_header

    file = "test.csv"

    csv_add_header(header=header,
                dataframe=data_ws.drop(["depth"], axis=1),
                filename=file)

    st.download_button("Save as csv", data=file, file_name=f"RSDL {selected_node}")


else:
     st.write('No dataset downloaded yet')




# cacher le "Made with streamlit
# https://www.kdnuggets.com/2021/07/streamlit-tips-tricks-hacks-data-scientists.html
hide_streamlit_style = """
	<style>
	/* This is to hide Streamlit footer */
	footer {visibility: hidden;}
	/*
	</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)