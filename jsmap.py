import streamlit as st
from streamlit_echarts import st_echarts, Map
import pandas as pd
import requests

@st.cache_data
def load_data():
    df = pd.read_csv("js_map_data_en_real.csv")
    df['city'] = df['city'].str.strip()
    df['type'] = df['type'].str.strip()
    years = [col for col in df.columns if col.isdigit()]
    return df, years

@st.cache_data
def load_geo_json():
    url = "https://geo.datav.aliyun.com/areas_v2/bound/320000_full.json"
    return requests.get(url).json()

# --- 封装成一个函数 ---
def render_js_map_dashboard():
    df, years = load_data()
    js_geo = load_geo_json()

    CITY_NAME_MAP = {
        "Nanjing": "南京市", "Wuxi": "无锡市", "Xuzhou": "徐州市",
        "Changzhou": "常州市", "Suzhou": "苏州市", "Nantong": "南通市",
        "Lianyungang": "连云港市", "Huai'an": "淮安市", "Yancheng": "盐城市",
        "Yangzhou": "扬州市", "Zhenjiang": "镇江市", "Taizhou": "泰州市",
        "Suqian": "宿迁市"
    }
    REVERSE_MAP = {v: k for k, v in CITY_NAME_MAP.items()}

    # 1. 准备地图数据
    latest_year = years[-1]
    map_source = df[df['type'] == 'Visitors']
    map_series_data = [{"name": CITY_NAME_MAP.get(row['city'], row['city']), "value": row[latest_year]} 
                       for _, row in map_source.iterrows()]

    map_options = {
        "title": {"text": f"Tourist Distribution ({latest_year})", "left": "center"},
        "tooltip": {"trigger": "item", "formatter": "{b}<br/>Visitors: {c}k"},
        "visualMap": {
            "min": float(map_source[latest_year].min()),
            "max": float(map_source[latest_year].max()),
            "calculable": True,
            "inRange": {"color": ["#e0f3f8", "#2c7fb8", "#084594"]},
            "left": "left"
        },
        "series": [{
            "name": "Jiangsu",
            "type": "map",
            "map": "JS_MAP",
            "label": {"show": True, "fontSize": 10},
            "data": map_series_data
        }]
    }

    # 2. 渲染地图
    selected_raw = st_echarts(
        options=map_options,
        map=Map("JS_MAP", js_geo),
        events={"click": "function(params) { return params.name }"},
        height="550px",
        key="js_map"
    )

    # 3. 点击逻辑处理
    target_city_zh = selected_raw if selected_raw else "南京市"
    if isinstance(target_city_zh, dict):
        target_city_zh = target_city_zh.get('chart_event', "南京市")
    target_city_en = REVERSE_MAP.get(target_city_zh, "Nanjing")

    st.write("---")
    st.subheader(f"📈 Growth Trend: {target_city_en}")

    # 4. 趋势图渲染逻辑
    city_data = df[df['city'] == target_city_en]
    v_data = city_data[city_data['type'] == 'Visitors'][years].iloc[0].tolist()
    r_data = city_data[city_data['type'] == 'Revenue'][years].iloc[0].tolist()

    line_options = {
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
        "legend": {"data": ["Visitors (k)", "Revenue (Billion)"], "bottom": 0},
        "xAxis": {"type": "category", "data": years, "boundaryGap": False},
        "yAxis": [
            {"type": "value", "name": "Visitors", "position": "left"},
            {"type": "value", "name": "Revenue", "position": "right"}
        ],
        "series": [
            {
                "name": "Visitors (k)", "type": "line", "smooth": True, "data": v_data,
                "itemStyle": {"color": "#084594"}, "areaStyle": {"opacity": 0.1}
            },
            {
                "name": "Revenue (Billion)", "type": "line", "smooth": True, "yAxisIndex": 1,
                "data": r_data, "itemStyle": {"color": "#d62728"}
            }
        ]
    }
    st_echarts(options=line_options, height="400px", key="trend_chart")