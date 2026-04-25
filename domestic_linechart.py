import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_domestic_trend_en():
    """
    Renders the trend of domestic tourism (Tourists & Revenue) for Jiangsu Province.
    Supports English dataset: JS_domestic_en.csv
    """
    # 1. Config Data Path
    data_file = "JS_domestic_en.csv"
    
    try:
        # Load the English-translated CSV
        df = pd.read_csv(data_file)
        
        # Identify year columns (e.g., "2000", "2010"...)
        years = [col for col in df.columns if col.isdigit()]
        
        # In JS_domestic_en.csv, the first column is named 'Indicator'
        target_col = 'Indicator' 
        
        # 2. Extract Data Rows using English Keywords
        # Matching labels: "Domestic Tourists (10k)" and "Domestic Tourism Revenue (Billion CNY)"
        tourist_row = df[df[target_col].str.contains('Tourists', na=False)]
        revenue_row = df[df[target_col].str.contains('Revenue', na=False)]

        if not tourist_row.empty and not revenue_row.empty:
            y_tourists = tourist_row[years].iloc[0].values.astype(float)
            y_revenue = revenue_row[years].iloc[0].values.astype(float)

            # 3. Create Interactive Chart (Dual Y-Axis)
            fig = go.Figure()

            # --- Trace 1: Tourists (Primary Y-Axis - Blue) ---
            fig.add_trace(go.Scatter(
                x=years, 
                y=y_tourists, 
                name="Domestic Tourists (10k)",
                mode='lines+markers', 
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=8),
                hovertemplate="Year: %{x}<br>Tourists: %{y:,.2f} (10k)<extra></extra>"
            ))

            # --- Trace 2: Revenue (Secondary Y-Axis - Red) ---
            fig.add_trace(go.Scatter(
                x=years, 
                y=y_revenue, 
                name="Tourism Revenue (Billion CNY)",
                mode='lines+markers', 
                line=dict(color='#d62728', width=3, dash='dash'),
                marker=dict(size=8, symbol='diamond'),
                yaxis="y2",
                hovertemplate="Year: %{x}<br>Revenue: %{y:,.2f} Billion CNY<extra></extra>"
            ))

            # --- Layout Configuration ---
            fig.update_layout(
                template="plotly_white",
                title=dict(
                    text="Jiangsu Domestic Tourism Performance Trend",
                    x=0.5,
                    xanchor='center',
                    font=dict(size=20)
                ),
                xaxis=dict(
                    title=dict(text="Timeline (Year)"),
                    gridcolor='rgba(235, 235, 235, 1)'
                ),
                # Primary Y-Axis (Tourists)
                yaxis=dict(
                    title=dict(
                        text="Number of Tourists (10k Person-times)",
                        font=dict(color="#1f77b4", size=14)
                    ),
                    tickfont=dict(color="#1f77b4"),
                    showgrid=True,
                    zeroline=True
                ),
                # Secondary Y-Axis (Revenue)
                yaxis2=dict(
                    title=dict(
                        text="Total Revenue (Billion CNY)",
                        font=dict(color="#d62728", size=14)
                    ),
                    tickfont=dict(color="#d62728"),
                    anchor="x",
                    overlaying="y",
                    side="right",
                    showgrid=False,
                    zeroline=True
                ),
                legend=dict(
                    orientation="h", 
                    yanchor="bottom",
                    y=1.05, 
                    xanchor="center",
                    x=0.5
                ),
                height=550,
                margin=dict(l=20, r=20, t=100, b=20),
                hovermode="x unified"
            )
            
            # Display chart in Streamlit
            st.plotly_chart(fig, use_container_width=True, key="domestic_trend_en_chart")
            
            # Additional Metric Summary
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Latest Tourist Count", f"{y_tourists[-1]:,.0f} (10k)")
            with col2:
                st.metric("Latest Total Revenue", f"{y_revenue[-1]:,.1f} Billion")

        else:
            st.error("Error: Could not locate 'Tourists' or 'Revenue' rows in the dataset.")
            
    except FileNotFoundError:
        st.error(f"Critical Error: File '{data_file}' not found. Please ensure the translation script has been executed.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Page setup for individual testing
    st.set_page_config(page_title="Jiangsu Tourism Dashboard", layout="wide")
    render_domestic_trend_en()