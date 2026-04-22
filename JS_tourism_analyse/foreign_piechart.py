import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="Jiangsu Inbound Tourism Analysis", layout="wide")

@st.cache_data
def load_and_init_data():
    try:
        # Load the English dataset created in Step 1
        df = pd.read_csv("cleaned_tourism_en.csv")
        df['Year'] = df['Year'].astype(str)
        
        # Fixed Color Mapping to keep consistency across years
        all_countries = sorted(df['Country'].unique())
        palette = px.colors.qualitative.Prism + px.colors.qualitative.Safe
        color_map = {country: palette[i % len(palette)] for i, country in enumerate(all_countries)}
        
        return df, color_map
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

df, color_map = load_and_init_data()

if df is not None:
    st.title("🌏 Jiangsu Overseas Visitors Structure Analysis")
    st.markdown("---")

    # --- Sidebar Controls ---
    st.sidebar.header("Control Panel")
    years = sorted(df['Year'].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Select Analysis Year", years)

    # Filter data
    plot_data = df[df['Year'] == selected_year]
    # Filter out zeros or tiny values for a cleaner pie chart
    plot_data = plot_data[plot_data['Visitors'] > 0].sort_values('Visitors', ascending=False)

    # --- Layout ---
    col1, col2 = st.columns([2, 1])

    with col1:
        # Create Donut Chart
        fig = px.pie(
            plot_data,
            values='Visitors',
            names='Country',
            color='Country',
            color_discrete_map=color_map,
            hole=0.4, # Donut style
            title=f"Market Composition of Overseas Visitors in {selected_year}"
        )
        
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='#FFFFFF', width=2))
        )
        
        # --- FIXED: Adjusted Margins and Legend to prevent overlap ---
        fig.update_layout(
            # Increased top margin to prevent title/legend overlap
            margin=dict(t=100, b=50, l=0, r=0),
            legend=dict(
                orientation="v", 
                yanchor="middle", 
                y=0.5, 
                xanchor="left", 
                x=1.05 # Move legend to the right side
            ),
            title=dict(
                x=0.5,
                xanchor='center',
                font=dict(size=20)
            )
        )
        
        st.plotly_chart(fig, use_container_width=True, key="overseas_pie_en")

    with col2:
        st.subheader("Data Details")
        # Displaying a clean table of the selected year
        display_df = plot_data[['Country', 'Visitors']].copy()
        display_df['Percentage'] = (display_df['Visitors'] / display_df['Visitors'].sum() * 100).round(2).astype(str) + '%'
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Additional Metric Summary
    total_visitors = plot_data['Visitors'].sum()
    top_market = plot_data.iloc[0]['Country']
    st.info(f"**Quick Insight:** In {selected_year}, the total number of overseas visitors reached **{total_visitors:,.0f}**, with **{top_market}** being the largest source market.")

else:
    st.warning("Please make sure 'cleaned_tourism_en.csv' exists in the directory.")