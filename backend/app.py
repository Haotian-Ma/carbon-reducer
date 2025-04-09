import os
from flask import Flask, jsonify, render_template
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
from flask_cors import CORS
import psycopg2
load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URI,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30
)

def loading_data_from_db(database_name):
    # Database connection parameters
    host = "34.129.179.229"
    database = "project"
    user = "postgres"
    password = "Iti<FVBpR:05tTOU"
    port = "5432"

    # SQL query to fetch data
    query = f"SELECT * FROM {database_name}"

    # Connect to PostgreSQL and fetch data
    try:
        # Establish the connection
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        # Load data into a DataFrame
        df = pd.read_sql_query(query, conn)
        
        # Close the connection
        conn.close()

        print(f"{database_name} downloaded successfully!")
        return df

    except Exception as e:
        print(f"An error occurred: {e}")

heat_data = loading_data_from_db("heat_data")
global_climate = loading_data_from_db("global_climate_data")
forest_trend = loading_data_from_db("forest_trend")
world_temp_data = loading_data_from_db("world_temp_data")


app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://ecosphere1.xyz", "https://sub.ecosphere1.xyz"]
    }
}, supports_credentials=True)

@app.route('/')
def home():
    return jsonify({"status": "OK"})

def load_data_from_db(table_name):
    query = f"SELECT * FROM {table_name}"
    try:
        df = pd.read_sql_query(query, engine)
        print(f"Table '{table_name}' loaded successfully!")
        return df
    except Exception as e:
        print(f"Error loading table '{table_name}': {e}")
        return None

@app.route('/api/chartdata1', methods=['POST',"GET","OPTIONS"])
def chartdata1_api():
    data = [
        {
            "x": world_temp_data["year"].tolist(),
            "y": world_temp_data["upper_bound"].tolist(),
            "type": "scatter",
            "mode": "lines",
            "name": "Upper Bound",
            "line": {"width": 0},
            "showlegend": False
        },
        {
            "x": world_temp_data["year"].tolist(),
            "y": world_temp_data["lower_bound"].tolist(),
            "type": "scatter",
            "mode": "lines",
            "name": "Lower Bound",
            "line": {"width": 0},
            "fill": "tonexty",
            "fillcolor": "rgba(68, 68, 68, 0.3)",
            "showlegend": False
        },
        {
            "x": world_temp_data["year"].tolist(),
            "y": world_temp_data["avg_temp"].tolist(),
            "type": "scatter",
            "mode": "lines",
            "name": "World Average Temperature",
            "line": {"color": "red"}
        }
    ]
    
    layout = {
        "title": {
            "text": "Average Temperature with Confidence Interval"
        },
        "xaxis": {
            "title": {
                "text": "Year"
            }
        },
        "yaxis": {
            "title": {
                "text": "Temperature (°C)"
            }
        },
        "hovermode": "x unified",
        "legend": {
            "title": {
                "text": "Legend"
            }
        }
    }
    
    return jsonify({"data": data, "layout": layout})

@app.route('/api/chartdata2')
def chartdata2_api():
    data = [
        {
            "x": global_climate["year"].tolist(),
            "y": global_climate["avg_temp"].tolist(),
            "type": "scatter",
            "mode": "lines",
            "name": "Avg Temperature (°C)",
            "line": {"color": "red"}
        },
        {
            "x": global_climate["year"].tolist(),
            "y": (global_climate["co2"] / 1e10).tolist(),
            "type": "scatter",
            "mode": "lines",
            "name": "CO₂ Emissions (x10⁻¹⁰)",
            "line": {"color": "blue"}
        },
        {
            "x": global_climate["year"].tolist(),
            "y": (global_climate["methane"] / 1e10).tolist(),
            "type": "scatter",
            "mode": "lines",
            "name": "Methane Emissions (x10⁻¹⁰)",
            "line": {"color": "orange"}
        },
        {
            "x": global_climate["year"].tolist(),
            "y": (global_climate["ghg_emission"] / 1e10).tolist(),
            "type": "scatter",
            "mode": "lines",
            "name": "GHG Emissions (x10⁻¹⁰)",
            "line": {"color": "green"}
        }
    ]
    
    layout = {
        "template": "plotly_white",
        "title": {
            "text": "Temperature and Emissions Over Time"
        },
        "xaxis": {
            "title": {
                "text": "Year"
            }
        },
        "yaxis": {
            "title": {
                "text": "Values (Normalized)"
            }
        },
        "hovermode": "x unified",
        "legend": {
            "title": {
                "text": "Legend"
            }
        }
    }
    
    return jsonify({"data": data, "layout": layout})

@app.route('/api/chartdata3')
def chartdata3_api():
    # chart3：CO2 Emissions by Sector in Australia (2021)
    url = "https://ourworldindata.org/grapher/co-emissions-by-sector.csv?v=1&csvType=full&useColumnShortNames=true"
    carbon_emission_by_sector = pd.read_csv(url, storage_options={'User-Agent': 'Our World In Data data fetch/1.0'})
    
    aus_co2_by_sector = carbon_emission_by_sector[carbon_emission_by_sector['Entity'] == 'Australia']
    aus_co2 = aus_co2_by_sector[aus_co2_by_sector['Year'] == 2021]
    aus_co2['Total'] = aus_co2.iloc[:, 3:].sum(axis=1)
    sector_percentages = aus_co2.iloc[:, 3:-1].div(aus_co2['Total'], axis=0) * 100
    sector_data = sector_percentages

    labels = [
        'Buildings',
        'Industry',
        'Land Use Change & Forestry',
        'Other Fuel Combustion',
        'Transport',
        'Manufacturing & Construction',
        'Fugitive Emissions',
        'Electricity & Heat',
        'Aviation & Shipping'
    ]
    values = sector_data.iloc[0].tolist()

    data = [
        {
            "labels": labels,
            "values": values,
            "hole": 0.3,
            "type": "pie"
        }
    ]
    
    layout = {
        "title": {"text": "CO₂ Emissions by Sector in Australia (2021)"}
    }
    
    return jsonify({"data": data, "layout": layout})

@app.route('/api/chartdata4')
def chartdata4_api():
    data = [
        {
            "type": "choropleth",
            "locations": forest_trend["country code"].tolist(),
            "z": forest_trend["percentage_change"].tolist(),
            "text": forest_trend["country name"].tolist(),
            "colorscale": "Jet",
            "zmin": -60,           
            "zmax": 60,            

            "colorbar": {
                "title": {"text": "Percentage Change"}
            }
        }
    ]
    
    layout = {
        "title": {"text": "Percentage Change in Forest Area (2000-2022)"},
        "geo": {
            "showframe": False,
            "showcoastlines": False,
            "projection": {"type": "equirectangular"}
        }
    }
    
    return jsonify({"data": data, "layout": layout})

@app.route('/api/chartdata5')
def chartdata5_api():

    data_series = forest_trend['percentage_change_norm'].dropna()
    
    kde = gaussian_kde(data_series)
    x_min = data_series.min()
    x_max = data_series.max()
    x_range = np.linspace(x_min - (x_max - x_min) * 0.1, x_max + (x_max - x_min) * 0.1, 500)
    y = kde(x_range)

    hist_trace = {
        "type": "histogram",
        "x": data_series.tolist(),
        "nbinsx": 30,
        "marker": {"color": "lightblue"},
        "histnorm": "probability density",
        "name": "Frequency (Histogram)"
    }
    
    kde_trace = {
        "type": "scatter",
        "x": x_range.tolist(),
        "y": y.tolist(),
        "mode": "lines",
        "name": "KDE",
        "line": {"color": "blue"}
    }
    
    data = [hist_trace, kde_trace]
    
    layout = {
        "title": {"text": "Distribution of Forest Trend (2000-2020)", "font": {"size": 16}},
        "xaxis": {"title": {"text": "Trend", "font": {"size": 14}}},
        "yaxis": {"title": {"text": "Frequency", "font": {"size": 14}}},
        "bargap": 0.05,
        "template": "plotly_white"
    }
    
    return jsonify({"data": data, "layout": layout})

@app.route('/api/chartdata6')
def chartdata6_api():

    heat_data['date'] = pd.to_datetime(heat_data['date'])
    heat_data['year'] = heat_data['date'].dt.year


    hot_days = heat_data[heat_data['is_hot']]

    hot_days_per_year = hot_days.groupby(['city', 'year']).size().reset_index(name='hot_day_count')

    pivot = hot_days_per_year[
        (hot_days_per_year['year'] >= 2014) & (hot_days_per_year['year'] <= 2024)
    ].pivot(index='city', columns='year', values='hot_day_count')

    z_list = [[None if pd.isna(x) else x for x in row] for row in pivot.values.tolist()]
    text_list = [[None if pd.isna(x) else x for x in row] for row in pivot.values.tolist()]

    trace = {
        "type": "heatmap",
        "z": z_list,
        "x": pivot.columns.tolist(),
        "y": pivot.index.tolist(),
        "colorscale": "YlOrRd",
        "reversescale": True,
        "colorbar": {"title": {"text": "Hot Days"}},
        "zmin": 0,  
        "text": text_list,     
        "texttemplate": "%{text:.0f}" 
    }
    
    layout = {
        "title": {"text": "Number of Hot Days per Year by City"},
        "xaxis": {"title": {"text": "Year"}},
        "yaxis": {"title": {"text": "City","standoff": 50},"automargin": True},
        "template": "plotly_white"
    }
    
    return jsonify({"data": [trace], "layout": layout})

@app.after_request
def after_request(response):
    print("Response Headers:", response.headers)
    return response
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
