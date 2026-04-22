import streamlit as st
import pandas as pd
import plotly.express as px
from jsmap import render_js_map_dashboard

# --- 1. 页面基本配置 ---
st.set_page_config(
    page_title="Jiangsu Tourism BI Platform",
    page_icon="🏯",
    layout="wide"
)

# --- 2. 导入各模块函数 ---
# 确保以下文件名与你的 .py 文件名完全一致
try:
    from domestic_linechart import render_domestic_trend_en
    from foreign_linechart import render_domestic_trend_fixed as render_foreign_trend
    from foreign_piechart import load_and_init_data as load_pie_data
    from scenic_map import render_scenic_map_en
    # 注意：jsmap.py 内部直接写了逻辑，我们可以在主应用中直接引用其逻辑
    import jsmap 
except ImportError as e:
    st.error(f"Module Import Error: {e}. Please ensure all .py files are in the same folder.")

# --- 3. 界面标题与侧边栏 ---
st.title("🏯 Jiangsu Province Tourism Business Intelligence Platform")
st.markdown("### Multi-dimensional Perspective and Data Analysis (2026 Edition)")

st.sidebar.image("https://img.icons8.com/clouds/100/000000/map.png", width=80)
st.sidebar.header("Platform Navigation")
st.sidebar.info("""
This English-localized dashboard provides:
1. Macro Tourism Trends
2. Overseas Market Analysis
3. Geographic Intelligence
""")

# --- 4. 定义选项卡 (Tabs) ---
# 将你的 5 个模块合理分配到 4 个 Tab 中
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Growth Trends", 
    "🌏 Overseas Market", 
    "📍 City Intelligence",
    "🗺️ Scenic Navigator"
])

# --- 5. 模块填充逻辑 ---

# --- Tab 1: 国内与国外趋势 (基于 linechart 模块) ---
with tab1:
    st.header("Tourism Performance Trends")
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Domestic Market")
        render_domestic_trend_en()
    with col_b:
        st.subheader("Foreign-Related Market")
        render_foreign_trend()

# --- Tab 2: 海外游客结构 (基于 piechart 模块) ---
with tab2:
    st.header("Overseas Visitors Composition")
    df_pie, color_map = load_pie_data()
    
    if df_pie is not None:
        years_pie = sorted(df_pie['Year'].unique(), reverse=True)
        selected_year = st.selectbox("Select Year", years_pie, key="global_year_select")
        
        plot_data = df_pie[df_pie['Year'] == selected_year]
        plot_data = plot_data[plot_data['Visitors'] > 0].sort_values('Visitors', ascending=False)
        
        c1, c2 = st.columns([2, 1])
        with c1:
            fig = px.pie(
                plot_data, values='Visitors', names='Country',
                color='Country', color_discrete_map=color_map,
                hole=0.4, title=f"Source Market Distribution ({selected_year})"
            )
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.write("**Data Details**")
            st.dataframe(plot_data[['Country', 'Visitors']], use_container_width=True, hide_index=True)

# --- Tab 3: 城市交互地图 (基于 jsmap.py) ---
with tab3:
    st.header("City-level Tourism Intelligence")
    st.info("Interactive Feature: Click any city on the map to refresh the trend chart.")
    
    # 这样调用就不会报 NameError 了
    render_js_map_dashboard()
# --- Tab 4: 景点导航 (基于 scenic_map.py) ---
with tab4:
    st.header("Interactive Scenic Spots Navigator")
    st.write("Geographic distribution of major attractions across Jiangsu.")
    render_scenic_map_en()

# --- 6. 页脚 ---
st.markdown("---")
st.caption("Data Source: Jiangsu Provincial Bureau of Statistics | Developed for BI Analysis Project | 2026")