"""
TB Global Analysis - Interactive Streamlit Dashboard
Explore tuberculosis incidence data from OWID and WHO sources
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Set page configuration
st.set_page_config(
    page_title="TB Global Analysis Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set style
sns.set_theme(style="whitegrid")
plt.style.use('seaborn-v0_8-darkgrid')

# ============================================================================
# LOAD DATA
# ============================================================================
@st.cache_data
def load_data():
    """Load cleaned datasets"""
    try:
        owid = pd.read_csv('data/processed/tb_owid_cleaned.csv')
        who = pd.read_csv('data/processed/tb_who_cleaned.csv')
        merged = pd.read_csv('data/processed/tb_merged.csv')
        return owid, who, merged
    except FileNotFoundError:
        st.error("❌ Data files not found. Please run `python src/pipeline.py` first.")
        st.stop()

owid_data, who_data, merged_data = load_data()

# ============================================================================
# SIDEBAR - FILTERS
# ============================================================================
st.sidebar.markdown("# 🔍 Filters")
st.sidebar.markdown("---")

# Select data source
data_source = st.sidebar.radio(
    "📊 Data Source",
    ["OWID (Global Trends)", "WHO (2023 Snapshot)", "Combined Analysis"]
)

# Year range filter (for OWID)
if data_source in ["OWID (Global Trends)", "Combined Analysis"]:
    year_range = st.sidebar.slider(
        "📅 Year Range (OWID)",
        min_value=int(owid_data['year'].min()),
        max_value=int(owid_data['year'].max()),
        value=(int(owid_data['year'].min()), int(owid_data['year'].max())),
        step=1
    )
else:
    year_range = None

# Country filter
all_countries = sorted(
    set(owid_data['country'].unique()) | set(who_data['country'].unique())
)
selected_countries = st.sidebar.multiselect(
    "🌏 Select Countries (leave empty for all)",
    all_countries,
    default=[]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**📈 Dashboard Info**\n\n"
    f"• OWID Records: {len(owid_data):,}\n"
    f"• WHO Records: {len(who_data):,}\n"
    f"• Merged Records: {len(merged_data):,}\n"
    f"• Countries: {len(all_countries)}\n"
    f"• Year Range: {int(owid_data['year'].min())}-{int(owid_data['year'].max())}"
)

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.markdown("# 🌍 TB Global Analysis Dashboard")
st.markdown("Explore tuberculosis incidence data from Our World in Data and WHO")
st.markdown("---")

# ============================================================================
# OWID ANALYSIS
# ============================================================================
if data_source == "OWID (Global Trends)":
    st.header("📊 OWID Global Trends Analysis")
    
    # Filter data
    filtered_owid = owid_data[
        (owid_data['year'] >= year_range[0]) & 
        (owid_data['year'] <= year_range[1])
    ]
    
    if selected_countries:
        filtered_owid = filtered_owid[filtered_owid['country'].isin(selected_countries)]
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📍 Countries", filtered_owid['country'].nunique())
    with col2:
        st.metric("📅 Years", filtered_owid['year'].nunique())
    with col3:
        st.metric("📊 Records", len(filtered_owid))
    with col4:
        avg_incidence = filtered_owid['tb_incidence'].mean()
        st.metric("📈 Avg TB Incidence", f"{avg_incidence:.1f}")
    
    st.markdown("---")
    
    # Global trend
    st.subheader("🔴 Global TB Incidence Trend Over Time")
    global_trend = filtered_owid.groupby('year')['tb_incidence'].mean().reset_index()
    
    fig_trend = px.line(
        global_trend,
        x='year',
        y='tb_incidence',
        title="Average TB Incidence Rate (Cases per 100,000)",
        labels={'year': 'Year', 'tb_incidence': 'TB Incidence Rate'},
        markers=True,
        line_shape='spline'
    )
    fig_trend.update_layout(hovermode='x unified', height=400)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Top countries for selected year
    st.subheader("🏆 Top 10 Countries by TB Incidence (Latest Year)")
    latest_year = filtered_owid['year'].max()
    top_countries = (
        filtered_owid[filtered_owid['year'] == latest_year]
        .nlargest(10, 'tb_incidence')
        .sort_values('tb_incidence')
    )
    
    if len(top_countries) > 0:
        fig_top = px.barh(
            top_countries,
            x='tb_incidence',
            y='country',
            orientation='h',
            title=f"Top 10 Countries - {latest_year}",
            labels={'tb_incidence': 'TB Incidence Rate', 'country': 'Country'},
            color='tb_incidence',
            color_continuous_scale='Reds'
        )
        fig_top.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_top, use_container_width=True)
    
    # Country comparison
    if selected_countries:
        st.subheader("📊 Selected Countries Comparison")
        comparison = filtered_owid.groupby('country')['tb_incidence'].mean().reset_index()
        comparison = comparison.sort_values('tb_incidence', ascending=True)
        
        fig_comp = px.barh(
            comparison,
            x='tb_incidence',
            y='country',
            orientation='h',
            title="Average TB Incidence by Country",
            labels={'tb_incidence': 'Average TB Incidence', 'country': 'Country'},
            color='tb_incidence',
            color_continuous_scale='Blues'
        )
        fig_comp.update_layout(height=max(300, len(selected_countries) * 30))
        st.plotly_chart(fig_comp, use_container_width=True)
    
    # Data export
    st.subheader("💾 Download Filtered Data")
    csv = filtered_owid.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"tb_owid_filtered_{year_range[0]}-{year_range[1]}.csv",
        mime="text/csv"
    )

# ============================================================================
# WHO ANALYSIS
# ============================================================================
elif data_source == "WHO (2023 Snapshot)":
    st.header("🏥 WHO 2023 Snapshot Analysis")
    
    filtered_who = who_data.copy()
    if selected_countries:
        filtered_who = filtered_who[filtered_who['country'].isin(selected_countries)]
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🌍 Countries", filtered_who['country'].nunique())
    with col2:
        st.metric("📊 Records", len(filtered_who))
    with col3:
        avg_incidence = filtered_who['tb_incidence'].mean()
        st.metric("📈 Avg TB Incidence", f"{avg_incidence:.1f}")
    
    st.markdown("---")
    
    # Top countries
    st.subheader("🏆 Top 15 Countries by TB Incidence (WHO 2023)")
    top_who = who_data.nlargest(15, 'tb_incidence').sort_values('tb_incidence')
    
    fig_who_top = px.barh(
        top_who,
        x='tb_incidence',
        y='country',
        orientation='h',
        title="WHO Top 15 Countries - 2023",
        labels={'tb_incidence': 'TB Incidence Rate', 'country': 'Country'},
        color='tb_incidence',
        color_continuous_scale='Oranges'
    )
    fig_who_top.update_layout(height=500)
    st.plotly_chart(fig_who_top, use_container_width=True)
    
    # Selected countries comparison
    if selected_countries:
        st.subheader("📊 Selected Countries (WHO 2023)")
        selected_who = filtered_who.sort_values('tb_incidence', ascending=True)
        
        fig_sel_who = px.barh(
            selected_who,
            x='tb_incidence',
            y='country',
            orientation='h',
            title="TB Incidence - Selected Countries",
            labels={'tb_incidence': 'TB Incidence Rate', 'country': 'Country'},
            color='tb_incidence',
            color_continuous_scale='Purples'
        )
        fig_sel_who.update_layout(height=max(300, len(selected_countries) * 30))
        st.plotly_chart(fig_sel_who, use_container_width=True)
    
    # Data export
    st.subheader("💾 Download Filtered Data")
    csv = filtered_who.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="tb_who_2023_filtered.csv",
        mime="text/csv"
    )

# ============================================================================
# COMBINED ANALYSIS
# ============================================================================
else:  # Combined Analysis
    st.header("🔀 Combined OWID & WHO Analysis")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🌍 Merged Countries", merged_data['country'].nunique())
    with col2:
        st.metric("📊 Merged Records", len(merged_data))
    with col3:
        avg_owid = merged_data['tb_incidence_owid'].mean()
        st.metric("📈 OWID Avg", f"{avg_owid:.1f}")
    with col4:
        avg_who = merged_data['tb_incidence_who'].mean()
        st.metric("📈 WHO Avg", f"{avg_who:.1f}")
    
    st.markdown("---")
    
    # OWID vs WHO comparison
    st.subheader("📊 OWID vs WHO Comparison (Top Countries)")
    
    # Prepare comparison data
    if 'tb_incidence_owid' in merged_data.columns and 'tb_incidence_who' in merged_data.columns:
        comparison_data = merged_data[['country', 'tb_incidence_owid', 'tb_incidence_who']].copy()
        comparison_data['avg_both'] = (
            comparison_data['tb_incidence_owid'] + comparison_data['tb_incidence_who']
        ) / 2
        comparison_data = comparison_data.nlargest(10, 'avg_both')
        
        fig_comp = px.bar(
            comparison_data,
            x='country',
            y=['tb_incidence_owid', 'tb_incidence_who'],
            barmode='group',
            title="OWID vs WHO TB Incidence Rates",
            labels={
                'country': 'Country',
                'value': 'TB Incidence Rate',
                'variable': 'Source'
            },
            color_discrete_map={
                'tb_incidence_owid': '#1f77b4',
                'tb_incidence_who': '#ff7f0e'
            }
        )
        fig_comp.update_layout(height=400)
        st.plotly_chart(fig_comp, use_container_width=True)
    
    # Data distribution
    st.subheader("📈 Data Distribution")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist_owid = px.histogram(
            merged_data,
            x='tb_incidence_owid',
            nbins=30,
            title="OWID TB Incidence Distribution",
            labels={'tb_incidence_owid': 'TB Incidence Rate'},
            color_discrete_sequence=['#1f77b4']
        )
        fig_hist_owid.update_layout(height=350)
        st.plotly_chart(fig_hist_owid, use_container_width=True)
    
    with col2:
        fig_hist_who = px.histogram(
            merged_data,
            x='tb_incidence_who',
            nbins=30,
            title="WHO TB Incidence Distribution",
            labels={'tb_incidence_who': 'TB Incidence Rate'},
            color_discrete_sequence=['#ff7f0e']
        )
        fig_hist_who.update_layout(height=350)
        st.plotly_chart(fig_hist_who, use_container_width=True)
    
    # Scatter plot
    st.subheader("🔵 OWID vs WHO Correlation")
    fig_scatter = px.scatter(
        merged_data,
        x='tb_incidence_owid',
        y='tb_incidence_who',
        hover_data=['country'],
        title="OWID vs WHO TB Incidence Rates",
        labels={
            'tb_incidence_owid': 'OWID TB Incidence',
            'tb_incidence_who': 'WHO TB Incidence'
        },
        color='tb_incidence_owid',
        color_continuous_scale='Viridis'
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Data export
    st.subheader("💾 Download Merged Data")
    csv = merged_data.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="tb_merged_analysis.csv",
        mime="text/csv"
    )

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown(
    "**📚 Data Sources:**\n"
    "- OWID: Our World in Data - TB Incidence (1990-2023)\n"
    "- WHO: World Health Organization - TB Incidence (2023)\n\n"
    "**🔧 Built with:** Python • Streamlit • Pandas • Plotly\n\n"
    "[View on GitHub](https://github.com) • [Report Issue](https://github.com)"
)
