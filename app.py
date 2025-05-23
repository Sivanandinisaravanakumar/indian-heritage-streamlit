import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="India's Cultural Heritage Portal",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <div style='text-align: center;'>
        <img src='https://upload.wikimedia.org/wikipedia/commons/4/4e/Taj_Mahal_in_March_2004.jpg' width='60%' style='border-radius: 10px; box-shadow: 2px 2px 8px #ccc;'/>
        <h1 style='color:#6C63FF; margin-bottom:0;'>🇮🇳 India's Cultural Heritage Portal 🇮🇳</h1>
        <h4 style='color:#444; margin-top:0;'>Explore Monuments, Museums, Art, and Tourism</h4>
    </div>
    <hr style='border:1px solid #6C63FF;'>
""", unsafe_allow_html=True)

st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Cultural Heritage Sites",
        "Monuments",
        "Museums",
        "Art & Artists",
        "Tourism Trends",
        "All Maps"
    ]
)

@st.cache_data
def load_and_clean_csv(filename):
    df = pd.read_csv(filename)
    # Clean column names: lowercase and strip spaces
    df.columns = df.columns.str.strip().str.lower()
    return df

def has_lat_lon(df):
    return set(['latitude', 'longitude']).issubset(df.columns)

def map_if_possible(df):
    if has_lat_lon(df):
        df = df.dropna(subset=['latitude', 'longitude'])
        st.map(df[['latitude', 'longitude']], use_container_width=True)
    else:
        st.info("No map data available (latitude/longitude columns missing).")

if page == "Home":
    st.markdown("""
        <div style='text-align: center;'>
            <p style='font-size:20px; color:#444;'>Welcome to India's most comprehensive cultural heritage portal.<br>
            Use the sidebar to explore UNESCO sites, famous monuments, museums, traditional art, and tourism trends.</p>
        </div>
    """, unsafe_allow_html=True)
    st.image(
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=900&q=60",
        use_container_width=True
    )
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("Tip: Use the sidebar to navigate between sections!")

elif page == "Cultural Heritage Sites":
    st.subheader("UNESCO Cultural Heritage Sites of India")
    df = load_and_clean_csv("cultural_heritage.csv")
    state = st.selectbox("Filter by State", ["All"] + sorted(df["state"].unique()))
    if state != "All":
        df = df[df["state"] == state]
    tab1, tab2 = st.tabs(["🗺️ Map", "📋 Table"])
    with tab1:
        map_if_possible(df)
    with tab2:
        st.dataframe(df, use_container_width=True)
    st.markdown("### Sites by State")
    if "state" in df.columns:
        chart = alt.Chart(df).mark_bar().encode(
            y=alt.Y('state:N', sort='-x'),
            x='count():Q',
            color='state:N'
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

elif page == "Monuments":
    st.subheader("Famous Monuments of India")
    df = load_and_clean_csv("monuments_data.csv")
    state = st.selectbox("Filter by State", ["All"] + sorted(df["state"].unique()))
    if state != "All":
        df = df[df["state"] == state]
    tab1, tab2 = st.tabs(["🗺️ Map", "📋 Table"])
    with tab1:
        map_if_possible(df)
    with tab2:
        st.dataframe(df, use_container_width=True)
    st.markdown("### Monuments by State")
    if "state" in df.columns:
        chart = alt.Chart(df).mark_bar().encode(
            y=alt.Y('state:N', sort='-x'),
            x='count():Q',
            color='state:N'
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

elif page == "Museums":
    st.subheader("Museums of India")
    df = load_and_clean_csv("museum_data.csv")
    state = st.selectbox("Filter by State", ["All"] + sorted(df["state"].unique()))
    if state != "All":
        df = df[df["state"] == state]
    tab1, tab2 = st.tabs(["🗺️ Map", "📋 Table"])
    with tab1:
        map_if_possible(df)
    with tab2:
        st.dataframe(df, use_container_width=True)
    if "state" in df.columns:
        chart = alt.Chart(df).mark_bar().encode(
            y=alt.Y('state:N', sort='-x'),
            x='count():Q',
            color='state:N'
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

elif page == "Art & Artists":
    st.subheader("Indian Art Forms & Artists")
    df = load_and_clean_csv("art_data.csv")
    region = st.selectbox("Filter by Region", ["All"] + sorted(df["region"].unique()))
    if region != "All":
        df = df[df["region"] == region]
    tab1, tab2 = st.tabs(["🗺️ Map", "📋 Table"])
    with tab1:
        map_if_possible(df)
    with tab2:
        st.dataframe(df, use_container_width=True)
    if "region" in df.columns:
        chart = alt.Chart(df).mark_bar().encode(
            y=alt.Y('region:N', sort='-x'),
            x='count():Q',
            color='region:N'
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

elif page == "Tourism Trends":
    st.subheader("Tourism in India (2018–2025)")
    df = load_and_clean_csv("tourism_data.csv")
    st.dataframe(df, use_container_width=True)
    if "year" in df.columns and "domestic_tourists_million" in df.columns:
        st.line_chart(df.set_index('year')['domestic_tourists_million'])
    if "year" in df.columns and "international_tourists_million" in df.columns:
        st.line_chart(df.set_index('year')['international_tourists_million'])
    if "year" in df.columns and "foreign_exchange_earnings_usd_billion" in df.columns:
        st.line_chart(df.set_index('year')['foreign_exchange_earnings_usd_billion'])

elif page == "All Maps":
    st.subheader("Combined Map of All Heritage Data")
    df1 = load_and_clean_csv("cultural_heritage.csv")
    df2 = load_and_clean_csv("monuments_data.csv")
    df3 = load_and_clean_csv("museum_data.csv")
    df4 = load_and_clean_csv("art_data.csv")
    dfs = []
    for d in [df1, df2, df3, df4]:
        if has_lat_lon(d):
            d = d.dropna(subset=['latitude', 'longitude'])
            dfs.append(d[['latitude', 'longitude']])
    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        st.map(combined, use_container_width=True)
    else:
        st.warning("No dataframes have both latitude and longitude columns.")

st.markdown("""
    <hr>
    <div style='text-align: center; color: #888;'>
        Made with ❤️ using Streamlit<br>
        Contact: <a href="sivanandini.sk@gmail.com">sivanandini.sk@gmail.com</a>
    </div>
""", unsafe_allow_html=True)
