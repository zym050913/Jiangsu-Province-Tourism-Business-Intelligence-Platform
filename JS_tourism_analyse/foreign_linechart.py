import streamlit as st
import pandas as pd
import plotly.graph_objects as go

def render_foreign_trend_fixed():
    """
    Renders the trend of foreign tourism for Jiangsu Province.
    Supports English dataset: JS_foreign_en.csv
    Format: Columns [Year, Revenue (10k USD), Tourists (Person)]
    """
    # 1. 配置
    data_file = "JS_foreign_en.csv"
    
    try:
        # 加载新的 CSV 文件
        df = pd.read_csv(data_file)
        
        # 提取数据列 
        years = df['Year'].astype(str).tolist()
        y_revenue = df['Revenue (10k USD)'].values
        y_tourists = df['Tourists (Person)'].values

        # 2. 构建图表
        fig = go.Figure()

        # --- 轨迹 1: 入境游客 (左轴) --- 
        fig.add_trace(go.Scatter(
            x=years, 
            y=y_tourists, 
            name="Inbound Tourists (Person)",
            mode='lines+markers', 
            line=dict(color='#1f77b4', width=3),
            hovertemplate="Year: %{x}<br>Tourists: %{y:,} Person<extra></extra>"
        ))

        # --- 轨迹 2: 旅游外汇收入 (右轴) --- 
        fig.add_trace(go.Scatter(
            x=years, 
            y=y_revenue, 
            name="Foreign Revenue (10k USD)",
            mode='lines+markers', 
            line=dict(color='#d62728', width=3, dash='dash'),
            yaxis="y2",
            hovertemplate="Year: %{x}<br>Revenue: %{y:,.0f} (10k USD)<extra></extra>"
        ))

        # --- 3. 布局优化 (解决重叠问题) ---
        fig.update_layout(
            template="plotly_white",
            title=dict(
                text="Jiangsu Inbound Tourism Performance Trend",
                x=0.5,
                xanchor='center',
                font=dict(size=22)
            ),
            # 增加顶部边距，为标题和图例留出空间
            margin=dict(l=20, r=20, t=130, b=30), 
            
            xaxis=dict(title=dict(text="Timeline (Year)")),
            
            # 主 Y 轴 (左侧 - 游客数)
            yaxis=dict(
                title=dict(
                    text="Inbound Tourists (Person)",
                    font=dict(color="#1f77b4")
                ),
                tickfont=dict(color="#1f77b4"),
                zeroline=True
            ),
            # 次 Y 轴 (右侧 - 收入)
            yaxis2=dict(
                title=dict(
                    text="Foreign Revenue (10k USD)",
                    font=dict(color="#d62728")
                ),
                tickfont=dict(color="#d62728"),
                anchor="x",
                overlaying="y",
                side="right",
                zeroline=True
            ),
            # 图例置于标题下方，图表上方
            legend=dict(
                orientation="h", 
                yanchor="bottom",
                y=1.12, 
                xanchor="center",
                x=0.5
            ),
            height=550,
            hovermode="x unified"
        )
        
        # 在 Streamlit 中显示
        st.plotly_chart(fig, use_container_width=True, key="foreign_trend_fixed_en")
        
        # 4. 底部指标卡片
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Latest Inbound Tourists", f"{y_tourists[-1]:,} Person")
        with col2:
            st.metric("Latest Foreign Revenue", f"{y_revenue[-1]:,.0f} (10k USD)")
            
    except Exception as e:
        st.error(f"Error loading CSV data: {e}")

if __name__ == "__main__":
    st.set_page_config(page_title="Jiangsu Foreign Tourism Trends", layout="wide")
    render_foreign_trend_fixed()