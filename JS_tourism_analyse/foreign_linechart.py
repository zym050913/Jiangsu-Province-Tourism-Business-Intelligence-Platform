import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_domestic_trend_fixed():
    """
    Renders the trend of domestic tourism (Tourists & Revenue) for Jiangsu Province.
    Supports English dataset: JS_domestic_en.csv
    Fixed: Legend and Title overlap issue.
    """
    # 1. Configuration
    data_file = "JS_domestic_en.csv"
    
    try:
        # Load the English-translated CSV
        df = pd.read_csv(data_file)
        
        # Identify year columns (e.g., "2000", "2010"...)
        years = [col for col in df.columns if col.isdigit()]
        
        # In JS_domestic_en.csv, the first column is 'Indicator'
        target_col = 'Indicator' 
        
        # 2. Data Extraction
        # Look for English keywords translated in the previous step
        tourist_row = df[df[target_col].str.contains('Tourists', na=False)]
        revenue_row = df[df[target_col].str.contains('Revenue', na=False)]

        if not tourist_row.empty and not revenue_row.empty:
            y_tourists = tourist_row[years].iloc[0].values.astype(float)
            y_revenue = revenue_row[years].iloc[0].values.astype(float)

            # 3. Build the Figure
            fig = go.Figure()

            # --- Trace 1: Tourists (Primary Y-Axis) ---
            fig.add_trace(go.Scatter(
                x=years, 
                y=y_tourists, 
                name="Domestic Tourists (10k)",
                mode='lines+markers', 
                line=dict(color='#1f77b4', width=3),
                hovertemplate="Year: %{x}<br>Tourists: %{y:,.2f} (10k)<extra></extra>"
            ))

            # --- Trace 2: Revenue (Secondary Y-Axis) ---
            fig.add_trace(go.Scatter(
                x=years, 
                y=y_revenue, 
                name="Tourism Revenue (Billion CNY)",
                mode='lines+markers', 
                line=dict(color='#d62728', width=3, dash='dash'),
                yaxis="y2",
                hovertemplate="Year: %{x}<br>Revenue: %{y:,.2f} Billion CNY<extra></extra>"
            ))

            # --- 4. Layout Optimization (Fixing Overlap) ---
            fig.update_layout(
                template="plotly_white",
                title=dict(
                    text="Jiangsu Domestic Tourism Performance Trend",
                    x=0.5,
                    xanchor='center',
                    font=dict(size=22)
                ),
                # INCREASE TOP MARGIN (t) to make room for Title + Legend
                margin=dict(l=20, r=20, t=130, b=30), 
                
                xaxis=dict(title=dict(text="Timeline (Year)")),
                
                # Primary Y-Axis (Left)
                yaxis=dict(
                    title=dict(
                        text="Number of Tourists (10,000 Person-times)",
                        font=dict(color="#1f77b4")
                    ),
                    tickfont=dict(color="#1f77b4"),
                    zeroline=True
                ),
                # Secondary Y-Axis (Right)
                yaxis2=dict(
                    title=dict(
                        text="Total Revenue (Billion CNY)",
                        font=dict(color="#d62728")
                    ),
                    tickfont=dict(color="#d62728"),
                    anchor="x",
                    overlaying="y",
                    side="right",
                    zeroline=True
                ),
                # POSITION LEGEND ABOVE THE PLOT AREA
                legend=dict(
                    orientation="h", 
                    yanchor="bottom",
                    y=1.12, # Adjusted to sit between Title and Chart
                    xanchor="center",
                    x=0.5
                ),
                height=550,
                hovermode="x unified"
            )
            
            # Display chart in Streamlit
            st.plotly_chart(fig, use_container_width=True, key="domestic_trend_fixed_en")
            
            # Additional Metric Summary Cards
            st.markdown("---")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Latest Tourist Count", f"{y_tourists[-1]:,.0f} (10k)")
            with col2:
                st.metric("Latest Total Revenue", f"{y_revenue[-1]:,.1f} Billion CNY")

        else:
            st.warning("Data not found. Please ensure 'Tourists' and 'Revenue' strings exist in the Indicator column.")
            
    except Exception as e:
        st.error(f"Error loading map data: {e}")

if __name__ == "__main__":
    st.set_page_config(page_title="Jiangsu Tourism Trends", layout="wide")
    render_domestic_trend_fixed()