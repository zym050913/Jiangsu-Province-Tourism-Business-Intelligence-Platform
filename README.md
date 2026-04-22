# Jiangsu-Province-Tourism-Business-Intelligence-Platform
## 1. Problem & User
The project addresses the lack of integrated, interactive platforms that combine macroeconomic tourism trends with granular scenic spot data. It serves policy analysts researching Jiangsu’s tourism development and travelers seeking data-driven insights to plan their destinations.
## 2.Data
Macroeconomic Data: Tourism-related indicators (2000–2025) sourced from the Jiangsu Provincial Bureau of Statistics Yearbooks. 
Scenic Spot Data: "China City Attraction Details" from Kaggle, originally web-scraped from qunar.com. 
Key Fields: Annual Tourist Volume, Revenue, City-level Growth Metrics, and Attraction Metadata (Location, Ratings, and Visitor Comments).
## 3. Methods
The technical workflow involves four key stages: Data Cleaning of 500+ records via Pandas, Geocoding for geographic coordinate generation, and Visualization using Plotly and Folium to create interactive maps and business intelligence charts. The final product is deployed as a responsive Web Interface using Streamlit, providing an intuitive platform for exploring tourism analytics in Jiangsu Province.
## 4. Key Findings
Top Source: Taiwan, China is the leading origin of overseas visitors to Jiangsu.
Geospatial Data: Analyzed 505 geolocated attractions sourced from Qunar.com.
COVID Impact: Identified significant economic troughs in 2020 and 2022.
Platform Utility: Successfully transformed raw web data into interactive BI insights.
## 5. How to run
Firstly, download all the files in the same folder.
Secondly, install dependencies: pip install streamlit pandas plotly streamlit-echarts streamlit-folium folium.
Lastly, run the app: streamlit run main_app.py.
## 6. Product link / Demo
## 7. Limitations & next steps
Currently, the platform focuses exclusively on Jiangsu Province and relies on static datasets. The next step is to expand the system to a national scale, covering all provinces in China, and to integrate real-time API data alongside predictive AI models to forecast upcoming travel peaks.
