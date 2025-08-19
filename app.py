import streamlit as st
import pandas as pd
import plotly.express as px

# ---- Sample dataset ----
data = {
    "Provider": ["Maxar", "Maxar", "Planet", "Planet", "Airbus", "Airbus", "Capella", "ICEYE", "Umbra", "Maxar", "Planet", "Airbus"],
    "Price_per_km2": [18.5, 22.0, 6.2, 5.6, 12.8, 10.9, 14.2, 9.5, 11.4, 20.3, 7.1, 13.6],
    "Resolution_m": [0.3, 0.3, 3, 5, 1, 1.5, 0.5, 1, 0.3, 0.5, 3, 0.8],
    "Revisit_days": [0.8, 0.5, 0.7, 0.5, 1.2, 1.0, 0.3, 0.4, 0.6, 0.6, 0.6, 0.9],
    "Swath_km": [13, 13, 24, 24, 19, 19, 5, 15, 6, 13, 24, 19],
    "Type": ["Optical","Optical","Optical","Optical","Optical","Optical","SAR","SAR","SAR","Optical","Optical","Optical"]
}
df = pd.DataFrame(data)

st.set_page_config(page_title="Satellite Pricing Intelligence", layout="wide")
st.title("🛰️ Satellite Pricing Intelligence Dashboard")

# ---- Sidebar filters ----
provider_filter = st.sidebar.multiselect("Filter by Provider", options=df["Provider"].unique(), default=df["Provider"].unique())
df_filtered = df[df["Provider"].isin(provider_filter)]

x_axis = st.sidebar.selectbox("X Axis", options=["Resolution_m", "Revisit_days", "Swath_km"])
y_axis = st.sidebar.selectbox("Y Axis (Price)", options=["Price_per_km2"])
size_axis = st.sidebar.selectbox("Bubble Size", options=["Revisit_days", "Swath_km"])
color_axis = st.sidebar.selectbox("Color By", options=["Provider", "Type"])

# ---- Scatter plot ----
st.subheader("Pricing vs Factors")
fig = px.scatter(
    df_filtered,
    x=x_axis, y=y_axis,
    color=color_axis,
    size=size_axis,
    hover_name="Provider",
    trendline="ols",
    labels={x_axis: x_axis, y_axis: "Price ($/km²)"}
)
st.plotly_chart(fig, use_container_width=True)

# ---- Correlation heatmap ----
st.subheader("Correlation Heatmap")
corr = df_filtered[["Price_per_km2","Resolution_m","Revisit_days","Swath_km"]].corr()
fig2 = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", title="Pearson Correlation")
st.plotly_chart(fig2, use_container_width=True)

# ---- Data table ----
st.subheader("Data Preview")
st.dataframe(df_filtered, use_container_width=True)

# ---- Download filtered ----
csv = df_filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download filtered CSV", csv, "filtered_satellite_data.csv", "text/csv")
