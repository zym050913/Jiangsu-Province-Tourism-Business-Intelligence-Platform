import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

def render_scenic_map_en():
    """
    Jiangsu Scenic Spots Map (English Version)
    Fixed: Icon missing issue replaced with CircleMarkers.
    """
    # 1. 配置文件路径
    data_file = 'JS_scenic_en.csv'
    
    try:
        # 加载英文版数据
        df = pd.read_csv(data_file)
        
        # 处理坐标列 (确保列名与英文CSV匹配)
        col_lng = 'lng'
        col_lat = 'lat'
        
        df[col_lng] = pd.to_numeric(df[col_lng], errors='coerce')
        df[col_lat] = pd.to_numeric(df[col_lat], errors='coerce')
        df = df.dropna(subset=[col_lng, col_lat])

        # 2. 初始化地图 (使用标准 OpenStreetMap)
        m = folium.Map(
            location=[32.5, 119.5], 
            zoom_start=7,
            tiles='OpenStreetMap'
        )

        # 3. 使用聚合标记防止页面卡顿
        marker_cluster = MarkerCluster(name="Scenic Spots").add_to(m)

        # 4. 遍历数据并生成标记
        for _, row in df.iterrows():
            name = str(row.get('Name', 'Unknown'))
            addr = str(row.get('Address', 'N/A'))
            score = str(row.get('Rating', 'N/A'))
            open_time = str(row.get('Open_Time', 'N/A'))
            advice = str(row.get('Suggested_Duration', 'N/A'))
            intro = str(row.get('Introduction', ''))
            
            # 限制简介长度，防止弹窗过长
            short_intro = (intro[:100] + '...') if len(intro) > 100 else intro

            # 构建全英文 HTML 弹窗
            popup_html = f"""
            <div style="width:220px; font-family: 'Arial'; line-height:1.4;">
                <h4 style="color:#d62728; margin-bottom:8px; border-bottom:1px solid #ddd;">{name}</h4>
                <p style="font-size:12px;"><b>⭐ Rating:</b> {score}</p>
                <p style="font-size:12px;"><b>📍 Location:</b> {addr}</p>
                <p style="font-size:12px;"><b>⏰ Hours:</b> {open_time}</p>
                <p style="font-size:12px;"><b>💡 Advice:</b> {advice}</p>
                <hr style="margin:8px 0;">
                <p style="font-size:11px; color:#555; font-style:italic;">{short_intro}</p>
            </div>
            """
            
            # 使用 CircleMarker (圆形标记) 彻底解决图标图片缺失问题
            folium.CircleMarker(
                location=[row[col_lat], row[col_lng]],
                radius=8,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=name,
                color="white",
                fill=True,
                fill_color="#d62728", # 红色填充
                fill_opacity=0.7,
                weight=2
            ).add_to(marker_cluster)

        # 5. 在 Streamlit 中展示
        st_folium(m, width="100%", height=600)

    except Exception as e:
        st.error(f"Error loading map data: {e}")

if __name__ == "__main__":
    st.set_page_config(page_title="Jiangsu Attractions", layout="wide")
    st.title("🏯 Jiangsu Scenic Spots Navigator")
    st.markdown("Interactive map based on your English datasets.")
    render_scenic_map_en()