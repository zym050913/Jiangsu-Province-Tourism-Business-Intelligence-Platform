# Jiangsu Province Tourism Business Intelligence Platform
## 1. Problem & User
- This project addresses the lack of an integrated interactive platform that combines macro-level tourism statistics with scenic spot data in Jiangsu Province.
- It is designed for policy analysts studying tourism development in Jiangsu and for travelers seeking data-driven destination insights.
## 2.Data

### Dataset 1: China Tourist Attractions Dataset
Source: Kaggle
Accessed on: 18 April 2026

Main fields used:
- attraction_name
- city
- province
- rating
- ticket_price
- opening_hours
- location
- visitor_count

### Dataset 2: Jiangsu Statistical Yearbook
Source: Jiangsu Provincial Bureau of Statistics
Accessed on: 18 April 2026

Main fields used:
- year
- city
- domestic_tourist_arrivals
- inbound_tourist_arrivals
- tourism_revenue

## 3. Methods
The technical workflow includes four main stages:

- Data cleaning and formatting of attraction-level and city-level tourism data using pandas
- Data integration across multiple sources for comparative analysis
- Geocoding to generate geographic coordinates
- Visualisation using Plotly and Folium to create interactive maps and business intelligence charts

## 4. Key Findings
- Taiwan, China is the leading source of inbound visitors to Jiangsu in the selected data period.
- Tourism activity in Jiangsu experienced clear declines in 2020 and 2022, suggesting a strong COVID-related impact.
- Tourist arrivals and tourism revenue are positively related in most Jiangsu cities.
- Cities with richer tourism resources tend to show stronger overall tourism performance, although the relationship is not perfectly consistent.

## 5. How to run
1. Clone or download this repository.
2. Install the required packages:

```bash
pip install -r requirements.txt
```
3. Make sure all project files are kept in the same folder structure and that the required data files are available.
4. If the datasets are not included in this repository, download them from the sources listed in the Data section and place them in the correct folder.
5. Run the Streamlit app locally:
```bash
streamlit run main_app.py
```
6. Open the local URL shown in the terminal 

## 6. Demo video link

## 7. Limitations & next steps
Currently, the platform focuses exclusively on Jiangsu Province and relies on static datasets. The next step is to expand the system to a national scale, covering all provinces in China, and to integrate real-time API data alongside predictive AI models to forecast upcoming travel peaks.
