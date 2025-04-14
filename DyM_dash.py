import streamlit as st
import pandas as pd
import plotly.express as px

# ✅ First Streamlit Command
st.set_page_config(page_title="Bird Monitoring Dashboard", layout="wide")

st.title("🦜 Bird Species Observation Analysis Dashboard")
st.markdown("### Upload both Forest and Grassland datasets to analyze bird diversity.")

# ✅ File Uploads
forest_file = st.file_uploader("📂 Upload Forest Dataset (Excel)", type=["xlsx"])
grassland_file = st.file_uploader("📂 Upload Grassland Dataset (Excel)", type=["xlsx"])

@st.cache_data
def load_data(forest_file, grassland_file):
    if not forest_file or not grassland_file:
        return None  # Return nothing if files are not uploaded

    # Load Forest Data
    df_forest = pd.concat(pd.read_excel(forest_file, sheet_name=None), ignore_index=True)
    df_forest['Location_Type'] = 'Forest'

    # Load Grassland Data
    df_grassland = pd.concat(pd.read_excel(grassland_file, sheet_name=None), ignore_index=True)
    df_grassland['Location_Type'] = 'Grassland'

    # Merge both datasets
    combined_df = pd.concat([df_forest, df_grassland], ignore_index=True)
    return combined_df

df = load_data(forest_file, grassland_file)

if df is not None:
    # ✅ Sidebar Filters
    st.sidebar.header("🔍 Filter Data")
    habitat_filter = st.sidebar.multiselect("Select Location Type", df['Location_Type'].unique(),
                                            default=df['Location_Type'].unique())
    admin_unit_filter = st.sidebar.multiselect("Select Admin Unit", df['Admin_Unit_Code'].dropna().unique(),
                                               default=df['Admin_Unit_Code'].dropna().unique())
    observer_filter = st.sidebar.multiselect("Select Observer", df['Observer'].dropna().unique(),
                                             default=df['Observer'].dropna().unique())

    # ✅ Apply Filters
    df_filtered = df[
        (df['Location_Type'].isin(habitat_filter)) &
        (df['Admin_Unit_Code'].isin(admin_unit_filter)) &
        (df['Observer'].isin(observer_filter))
    ]

    # ✅ Convert Date and Extract Month
    df_filtered.loc[:, 'Date'] = pd.to_datetime(df_filtered['Date'], errors='coerce')
    df_filtered.loc[:, 'Month'] = df_filtered['Date'].dt.month

    # ----------- Section 1: Seasonal Trends -----------
    st.header("1️⃣ Seasonal Trends")
    temporal = df_filtered.groupby(['Month', 'Location_Type']).size().reset_index(name='Sightings')
    fig1 = px.line(temporal, x='Month', y='Sightings', color='Location_Type', markers=True,
                   title="Bird Sightings Trend Across Months")
    st.plotly_chart(fig1, use_container_width=True)

    # ----------- Section 2: Spatial Analysis -----------
    st.header("2️⃣ Spatial Distribution")
    spatial = df_filtered.groupby(['Admin_Unit_Code', 'Location_Type']).size().reset_index(name='Sightings')
    fig2 = px.bar(spatial, x='Admin_Unit_Code', y='Sightings', color='Location_Type',
                  title="Bird Sightings by Administrative Unit")
    st.plotly_chart(fig2, use_container_width=True)

    # ----------- Section 3: Species Insights -----------
    st.header("3️⃣ Species Insights")
    species_count = df_filtered.groupby('Scientific_Name').size().reset_index(name='Count').sort_values(by='Count', ascending=False).head(10)
    fig3 = px.bar(species_count, x='Scientific_Name', y='Count', color='Count', title="Top 10 Most Observed Bird Species")
    st.plotly_chart(fig3, use_container_width=True)

    sex_ratio = df_filtered.groupby('Sex').size().reset_index(name='Count')
    fig4 = px.pie(sex_ratio, values='Count', names='Sex', title="Sex Ratio of Observed Birds")
    st.plotly_chart(fig4, use_container_width=True)

    # ----------- Section 4: Environmental Conditions -----------
    st.header("4️⃣ Environmental Conditions")
    fig5 = px.scatter(df_filtered, x='Temperature', y='Humidity', color='Location_Type', title="Temperature vs Humidity")
    st.plotly_chart(fig5, use_container_width=True)

    disturbance = df_filtered.groupby('Disturbance').size().reset_index(name='Count')
    fig6 = px.bar(disturbance, x='Disturbance', y='Count', title="Impact of Disturbances on Bird Sightings")
    st.plotly_chart(fig6, use_container_width=True)

    # ----------- Section 5: Distance & Flyover Behavior -----------
    st.header("5️⃣ Distance & Behavior")
    distance = df_filtered.groupby('Distance').size().reset_index(name='Count')
    fig7 = px.bar(distance, x='Distance', y='Count', title="Bird Observation Distance Distribution")
    st.plotly_chart(fig7, use_container_width=True)

    flyover = df_filtered.groupby('Flyover_Observed').size().reset_index(name='Count')
    fig8 = px.pie(flyover, values='Count', names='Flyover_Observed', title="Flyover Behavior Observations")
    st.plotly_chart(fig8, use_container_width=True)

    # ----------- Section 6: Observer Trends -----------
    st.header("6️⃣ Observer Patterns")
    observer_trend = df_filtered.groupby('Observer').size().reset_index(name='Sightings').sort_values(by='Sightings', ascending=False)
    fig9 = px.bar(observer_trend.head(10), x='Observer', y='Sightings', title="Top Observers with Most Bird Sightings")
    st.plotly_chart(fig9, use_container_width=True)

    # ----------- Section 7: Conservation Insights -----------
    st.header("7️⃣ Conservation Insights")
    watchlist = df_filtered[df_filtered['PIF_Watchlist_Status'] == True]
    watchlist_counts = watchlist.groupby('Scientific_Name').size().reset_index(name='Count')
    fig10 = px.bar(watchlist_counts, x='Scientific_Name', y='Count', title="Birds on Conservation Watchlist")
    st.plotly_chart(fig10, use_container_width=True)

    # ✅ Sidebar Summary
    st.sidebar.markdown("---")
    st.sidebar.metric("Total Records", len(df_filtered))
    st.sidebar.metric("Unique Bird Species", df_filtered['Scientific_Name'].nunique())

else:
    st.warning("⚠ Please upload both the Forest and Grassland datasets to proceed.")