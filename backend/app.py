import os
import json
from flask import Flask, send_from_directory, jsonify, render_template, request
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import plotly.graph_objects as go
from sqlalchemy import create_engine, text, MetaData, Table, select
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv
from flask_cors import CORS
import geopandas as gpd
import folium
import geopandas as gpd, folium
import psycopg2
from ultralytics import YOLO
import torch
from io import BytesIO
from PIL import Image
from utils import preprocess_image

# File upload validation
ALLOWED_EXT = {"png", "jpg", "jpeg"}
def allowed_file(fn):
    return "." in fn and fn.rsplit(".",1)[1].lower() in ALLOWED_EXT

# 1) Load the YOLOv8 model
#    'best.pt' is the trained detection+classification checkpoint
det_model = YOLO("best.pt")  # ultralytics will parse the 'model' layer from the checkpoint

# Confidence threshold and input size for YOLOv8
DETECT_CONF = 0.5
IMG_SIZE    = 640

# Path to GeoJSON data
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'geo_sub_data.geojson')

# Load environment variables from .env file
load_dotenv()

# Retrieve database credentials from environment variables
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

# Construct the database URI for SQLAlchemy using psycopg2 driver
DATABASE_URI = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create a SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URI,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30
)

# Function to load data from a specified database table using psycopg2 directly
def loading_data_from_db(database_name):
    """
    Load data from the specified table using SQLAlchemy's reflection.
    This method avoids SQL injection risks by using SQLAlchemy's safe methods.
    
    Parameters:
        database_name (str): Name of the table to load data from.
    
    Returns:
        pd.DataFrame: DataFrame containing the table's data.
    """
    # Define a whitelist of allowed table names to prevent unauthorized access.
    allowed_tables = ["heat_data", "global_climate_data", "forest_trend", "world_temp_data"]
    if database_name not in allowed_tables:
        raise ValueError("Invalid table name provided.")
    
    try:
        # Use SQLAlchemy's MetaData to reflect the table structure
        metadata = MetaData()
        # Reflect the table from the existing database
        table = Table(database_name, metadata, autoload_with=engine)
        
        # Build a SELECT query to fetch all records from the table
        query = select(table)
        
        # Execute the query and load the results into a Pandas DataFrame
        with engine.connect() as conn:
            df = pd.read_sql_query(query, conn)
        
        print(f"{database_name} downloaded successfully!")
        return df

    except Exception as e:
        print(f"An error occurred: {e}")

# Load data from various tables
heat_data = loading_data_from_db("heat_data")
global_climate = loading_data_from_db("global_climate_data")
forest_trend = loading_data_from_db("forest_trend")
world_temp_data = loading_data_from_db("world_temp_data")


app = Flask(__name__, template_folder="templates")

@app.route("/api/predict", methods=["POST"])
def predict():
    # 1. Validate the uploaded file
    if "file" not in request.files:
        return jsonify(error="No file"), 400
    f = request.files["file"]
    if f.filename == "" or not allowed_file(f.filename):
        return jsonify(error="Invalid file"), 400

    # 2. Read image from request
    data = f.read()
    img = Image.open(BytesIO(data)).convert("RGB")
    img_np = np.array(img)  # 转成 H×W×3 的 NumPy

    # 3. Perform YOLO inference for detection and classification
    results = det_model.predict(
        source=img_np,
        imgsz=IMG_SIZE,
        conf=DETECT_CONF,
        max_det=10,
        verbose=False
    )

    # 4. Check if exactly one object is detected
    boxes = results[0].boxes
    n = len(boxes)
    if n != 1:
        return jsonify(error=f"Detected {n} objects; please upload exactly one."), 400

    # 5. Extract detection output
    box = boxes[0]
    cls_id = int(box.cls)          # Class index
    cls_name = det_model.names[cls_id]  # Class name
    conf = float(box.conf)         # Confidence score
    x1,y1,x2,y2 = box.xyxy[0].tolist()


    return jsonify({
        "class":      cls_name,
        "confidence": round(conf, 4),
        "bbox":       [x1, y1, x2, y2]
    })

# Define a simple home route to verify the service is running.
@app.route('/')
def home():
    return jsonify({"status": "OK"})

#Reads the GeoJSON file containing suburb boundaries and vegetation data
@app.route('/api/geojson')
def get_geojson():
    # Load the GeoJSON file
    with open('data/geo_sub_data.geojson', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

# API route: /api/chartdata1
# Returns JSON data for the chart with Global Temperature and Emissions.
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

# API route: /api/chartdata2
# Returns JSON data for the chart with temperature and emissions.
@app.route('/api/chartdata2', methods=['POST',"GET","OPTIONS"])
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

# API route: /api/chartdata3
# Returns JSON data for a pie chart showing CO2 emissions by sector in Australia (2021).
@app.route('/api/chartdata3', methods=['POST',"GET","OPTIONS"])
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

# API route: /api/chartdata4
# Returns JSON data for a choropleth map visualizing percentage change in forest area.
@app.route('/api/chartdata4', methods=['POST',"GET","OPTIONS"])
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

# API route: /api/chartdata5
# Returns JSON data for a combined histogram and kernel density estimation (KDE) chart.
@app.route('/api/chartdata5', methods=['POST',"GET","OPTIONS"])
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

# API route: /api/chartdata6
# Returns JSON data for a heatmap showing the number of hot days per year by city.
@app.route('/api/chartdata6', methods=['POST',"GET","OPTIONS"])
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

# An after_request hook to add CORS headers to every response for debugging purposes.
@app.after_request
def add_cors_headers(response):
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Print the URL map for debugging purposes (shows all registered routes)
print(app.url_map)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
