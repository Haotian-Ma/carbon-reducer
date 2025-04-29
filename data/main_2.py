import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip

geo_json_file = 'geo_sub_data.geojson'
gdf = gpd.read_file(geo_json_file)

# ------ Using Folium for create a map ---------
# For any datetime columns (which can cause issues with GeoJSON)
for col in gdf.select_dtypes(include=['datetime64']).columns:
    gdf[col] = gdf[col].astype(str)

# Create a map centered on Melbourne
m = folium.Map(location=[-37.8136, 144.9631], zoom_start=9, tiles='CartoDB positron')

# Add a choropleth map layer
folium.Choropleth(
    geo_data=gdf,
    name='Vegetation Coverage',
    data=gdf,
    columns=['LOC_NAME', 'VegRate'],
    key_on='feature.properties.LOC_NAME',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Vegetation Coverage (%)'
).add_to(m)

# Add GeoJson with tooltips for interactive hover
style_function = lambda x: {
    'fillColor': '#ffffff',
    'color': '#000000',
    'fillOpacity': 0.0,
    'weight': 0.5
}

tooltip = GeoJsonTooltip(
    fields=['LOC_NAME', 'Postcode', 'VegRate', 'TreeRate'],  
    aliases=['Suburb:', 'Postcode:', 'Vegetation Coverage (%):', 'Tree Coverage Rate (%):'],  
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 2px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """
)

geojson = folium.GeoJson(
    gdf,
    style_function=style_function,
    tooltip=tooltip
)

geojson.add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

m.save('map.html')