import streamlit as st

# 1. 导入各个模块的渲染函数
# 请确保这些 .py 文件与 main_app.py 在同一目录下
from domestic_linechart import render_domestic_trend_en
from foreign_linechart import render_foreign_trend_fixed
from foreign_piechart import load_and_init_data as load_pie_data
from jsmap import render_js_map_dashboard
from scenic_map import render_scenic_map_en

# 2. 页面全局配置 (必须在所有 streamlit 命令之前)
st.set_page_config(
    page_title="Jiangsu Tourism Big Data Dashboard",
    page_icon="🏯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义标题样式
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        color: #1f77b4;
        text-align: center;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .section-header {
        font-size: 24px;
        color: #333;
        border-left: 5px solid #1f77b4;
        padding-left: 10px;
        margin-top: 30px;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.sidebar.title("🏮 Navigation")
    st.sidebar.markdown("Select a module to view details")
    
    # 3. 定义侧边栏菜单
    menu = [
        "Comprehensive Trends (Domestic & Foreign)",  # 将两者整合的新菜单项
        "Market Structure: Overseas",
        "City Distribution: Regional Map",
        "Scenic Spot Navigator"
    ]
    choice = st.sidebar.radio("Go to", menu)

    st.sidebar.info("Data source: Jiangsu Tourism Statistics")

    # 4. 路由逻辑
    
    # --- 模块 A: 整合国内与入境趋势 ---
    if choice == "Comprehensive Trends (Domestic & Foreign)":
        st.markdown('<p class="main-title">Jiangsu Tourism Performance Overview</p>', unsafe_allow_html=True)
        
        # 使用 Tabs 标签页或者直接上下排列
        tab1, tab2 = st.tabs(["📍 Domestic Tourism", "🌎 Foreign Tourism"])
        
        with tab1:
            st.markdown('<div class="section-header">Domestic Market Trends</div>', unsafe_allow_html=True)
            render_domestic_trend_en()
            
        with tab2:
            st.markdown('<div class="section-header">Inbound/Foreign Market Performance</div>', unsafe_allow_html=True)
            render_foreign_trend_fixed()

    # --- 模块 B: 海外市场结构 (饼图) ---
    elif choice == "Market Structure: Overseas":
        st.markdown('<p class="main-title">Overseas Visitors Market Structure</p>', unsafe_allow_html=True)
        from plotly import express as px
        df, color_map = load_pie_data()
        if df is not None:
            years = sorted(df['Year'].unique(), reverse=True)
            selected_year = st.sidebar.selectbox("Select Analysis Year", years)
            
            plot_data = df[df['Year'] == selected_year]
            plot_data = plot_data[plot_data['Visitors'] > 0].sort_values('Visitors', ascending=False)
            
            col1, col2 = st.columns([2, 1])
            with col1:
                fig = px.pie(plot_data, values='Visitors', names='Country', color='Country',
                             color_discrete_map=color_map, hole=0.4)
                fig.update_layout(margin=dict(t=50, b=0, l=0, r=0))
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                st.subheader(f"Details ({selected_year})")
                st.dataframe(plot_data[['Country', 'Visitors']], hide_index=True, use_container_width=True)
        else:
            st.error("Error: Could not load data for Pie Chart.")

    # --- 模块 C: 城市分布地图 ---
    elif choice == "City Distribution: Regional Map":
        st.markdown('<p class="main-title">Regional Growth & City Ranking</p>', unsafe_allow_html=True)
        render_js_map_dashboard()

    # --- 模块 D: 景区导航地图 ---
    elif choice == "Scenic Spot Navigator":
        st.markdown('<p class="main-title">Interactive Scenic Spots Map</p>', unsafe_allow_html=True)
        render_scenic_map_en()

if __name__ == "__main__":
    main()