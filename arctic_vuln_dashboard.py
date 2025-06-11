
import streamlit as st
import pandas as pd
import plotly.express as px

# Inject custom CSS for Arctic background image
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/e/e8/Arctic_Ocean_-_icebergs_and_sunset.jpg');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Frozen vulnerability scores data
data = {
    "Country": [
        "Canada", "United States", "Russia", "Norway", "Denmark",
        "Finland", "Sweden", "Iceland", "United Kingdom", "Germany",
        "France", "China"
    ],
    "Base Score": [58.0, 50.0, 45.0, 32.0, 45.0, 51.0, 54.0, 44.0, 43.0, 52.0, 48.0, 62.0],
    "Risk-Adjusted Score": [73.66, 63.5, 32.85, 40.64, 57.15, 64.77, 68.58, 55.88, 54.61, 66.04, 60.96, 0],
    "Net Readiness": [59.0, 73.0, 81.0, 74.0, 62.0, 60.0, 57.0, 52.0, 63.0, 58.0, 60.0, 66.0]
}

df = pd.DataFrame(data)

st.title("Arctic Vulnerability Dashboard (VULN-2025-Q2)")

score_type = st.selectbox("Select Score Type:", ["Base Score", "Risk-Adjusted Score", "Net Readiness"])

# Bar chart with blue-themed color
st.subheader(f"{score_type} by Country")
fig_bar = px.bar(df, x="Country", y=score_type, color=score_type,
                 color_continuous_scale="Blues", title=f"{score_type}")
st.plotly_chart(fig_bar)

# Map visualization (excluding China due to ISO3 limitation)
st.subheader("Map: Risk-Adjusted Score")
map_data = df[df["Country"] != "China"].dropna(subset=["Risk-Adjusted Score"]).copy()
map_data["ISO3"] = ["CAN", "USA", "RUS", "NOR", "DNK", "FIN", "SWE", "ISL", "GBR", "DEU", "FRA"]
fig_map = px.choropleth(
    map_data,
    locations="ISO3",
    color="Risk-Adjusted Score",
    hover_name="Country",
    color_continuous_scale=px.colors.sequential.Blues,
    range_color=(30, 75),
    title="Arctic Risk-Adjusted Vulnerability Scores"
)
fig_map.update_geos(showcoastlines=True, showland=True, fitbounds="locations")
st.plotly_chart(fig_map)

# Display score table
st.subheader("Full Vulnerability Score Table")
st.dataframe(df.set_index("Country"))

st.markdown("---")
st.caption("Data source: VULN-2025-Q2 (Frozen Canonical Scores)")
