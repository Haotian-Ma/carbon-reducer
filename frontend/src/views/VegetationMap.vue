<template>
  <div class="veg-map-wrapper">
    <div class="veg-map-container">
      <!-- Error Alert -->
      <div v-if="error" class="error-section">
        <p class="error-message">{{ error }}</p>
      </div>

      <h2 class="map-title">Vegetation Coverage Map</h2>

      <!-- Top Section: Map and Search -->
      <div class="top-section">
        <h3>Find Vegetation Coverage by Location</h3>

        <!-- Search Section -->
        <div class="search-section">
          <div class="address-input-wrapper">
            <input 
              v-model="searchQuery" 
              @input="handleInput" 
              @focus="showSuggestions = true"
              @blur="handleSearchBlur"
              placeholder="Enter postcode or location"
              class="address-input" 
              ref="searchInput"
            />
            <!-- Dropdown address suggestions -->
            <div v-if="showSuggestions && suggestions.length > 0" class="suggestions-dropdown">
              <div 
                v-for="suggestion in suggestions" 
                :key="suggestion.id" 
                @mousedown="handleAddressSelect(suggestion)"
                class="suggestion-item"
              >
                {{ suggestion.place_name }}
              </div>
            </div>
          </div>
          <button @click="searchLocation" class="btn-primary">Search</button>
          <button @click="useMyLocation" class="location-button">
            <span class="location-icon">📍</span> Use My Location
          </button>
        </div>

        <!-- Map Container -->
        <div class="map-wrapper">
          <div class="map-container">
            <div ref="mapContainer" class="map"></div>
            <!-- Loading Indicator -->
            <div v-if="isLoading" class="loading-overlay">
              <div class="loading-spinner"></div>
              <p>Loading vegetation data...</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Section: Vegetation Data Display -->
      <div v-if="locationInfo" class="bottom-section">
        <h3>Vegetation Coverage for {{ locationStr || 'Selected Location' }}</h3>

        <div class="veg-data-section">
          <!-- Vegetation Rate Display -->
          <div class="veg-display">
            <div class="veg-circle" :style="getVegCircleStyle(locationInfo.vegRate)">
              <span class="veg-value">{{ locationInfo.vegRate }}%</span>
              <span class="veg-type">Vegetation</span>
            </div>

            <div class="tree-circle" :style="getTreeCircleStyle(locationInfo.treeRate)">
              <span class="tree-value">{{ locationInfo.treeRate }}%</span>
              <span class="tree-type">Tree Cover</span>
            </div>
          </div>

          <div class="veg-location">
            <p class="location-name">
              <span class="location-icon">📍</span> {{ locationStr || 'Selected Location' }}
            </p>
            <p class="postcode">Postcode: {{ locationInfo.postcode }}</p>
            <p class="coordinates" v-if="coordinates">{{ coordinates.lat.toFixed(4) }}, {{ coordinates.lng.toFixed(4) }}</p>
          </div>

          <!-- Vegetation Scale Bar -->
          <div class="veg-scale-container">
            <span class="veg-label low-label">Low</span>
            <div class="veg-meter-scale">
              <div class="scale-segment"></div>
            </div>
            <span class="veg-label high-label">High</span>
          </div>

          <!-- Vegetation summary -->
          <div class="veg-summary">
            <p>{{ getVegetationRecommendation(locationInfo.vegRate) }}</p>
          </div>
        </div>
      </div>

      <div v-else-if="!isLoading" class="no-data-message">
        <p>Search for a location or click on the map to get vegetation information</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || '<YOUR_MAPBOX_TOKEN>'

// Reactive variables
const mapContainer = ref(null)
const searchInput = ref(null)
const map = ref(null)
const marker = ref(null)
const locationInfo = ref(null)
const isLoading = ref(false)
const error = ref('')
const searchQuery = ref('')
const suggestions = ref([])
const showSuggestions = ref(false)
const locationStr = ref('')
const coordinates = ref(null)

// Get style object for vegetation circle
const getVegCircleStyle = (vegRate) => {
  return {
    backgroundColor: '#238b45',
    color: 'white',
    opacity: Math.max(0.3, vegRate / 100)
  };
};

// Get style object for tree circle
const getTreeCircleStyle = (treeRate) => {
  return {
    backgroundColor: '#2878b8',
    color: 'white',
    opacity: Math.max(0.3, treeRate / 100)
  };
};

// Get vegetation recommendation
const getVegetationRecommendation = (vegRate) => {
  if (vegRate < 20) {
    return "This area has very low vegetation coverage. Urban greening initiatives could significantly improve environmental quality and livability.";
  } else if (vegRate < 40) {
    return "This area has low vegetation coverage. Adding more plants and trees would help reduce urban heat and improve air quality.";
  } else if (vegRate < 60) {
    return "This area has moderate vegetation coverage, providing some environmental benefits. Further greening could enhance these benefits.";
  } else if (vegRate < 80) {
    return "This area has good vegetation coverage, offering substantial environmental benefits to residents.";
  } else {
    return "This area has excellent vegetation coverage, providing optimal environmental benefits including temperature regulation, air purification, and wildlife habitat.";
  }
};

// Fetch address suggestions from Mapbox
const handleInput = async () => {
  error.value = '';
  if (!searchQuery.value) {
    suggestions.value = [];
    return;
  }
  try {
    const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(
      searchQuery.value
    )}.json?access_token=${mapboxgl.accessToken}&country=au&limit=5`;
    const response = await fetch(url);
    if (!response.ok) throw new Error('Failed to fetch address suggestions');

    const data = await response.json();
    suggestions.value = data.features;
  } catch (err) {
    error.value = 'Failed to fetch address suggestions.';
  }
};

// Handle search blur
const handleSearchBlur = () => {
  setTimeout(() => {
    showSuggestions.value = false;
  }, 200);
};

// Handle address selection
const handleAddressSelect = (suggestion) => {
  searchQuery.value = suggestion.place_name;
  suggestions.value = [];
  showSuggestions.value = false;
  locationStr.value = suggestion.place_name;

  if (marker.value) {
    marker.value.setLngLat(suggestion.center);
    map.value.flyTo({ center: suggestion.center });
  }

  coordinates.value = {
    lat: suggestion.center[1],
    lng: suggestion.center[0]
  };

  findVegetationData([suggestion.center[0], suggestion.center[1]]);
};

// Manual search
const searchLocation = async () => {
  error.value = '';
  if (!searchQuery.value) {
    error.value = 'Please enter a location.';
    return;
  }

  try {
    if (suggestions.value.length > 0 && suggestions.value[0].center) {
      const center = suggestions.value[0].center;
      if (marker.value) {
        marker.value.setLngLat(center);
        map.value.flyTo({ center: center });
      }
      locationStr.value = searchQuery.value;
      coordinates.value = {
        lat: center[1],
        lng: center[0]
      };
      findVegetationData(center);
    } else {
      const coords = await geocodeAddress(searchQuery.value);
      if (!coords) throw new Error('No valid coordinates found.');
      if (marker.value) {
        marker.value.setLngLat([coords.lng, coords.lat]);
        map.value.flyTo({ center: [coords.lng, coords.lat] });
      }
      locationStr.value = searchQuery.value;
      coordinates.value = coords;
      findVegetationData([coords.lng, coords.lat]);
    }
  } catch (err) {
    error.value = 'Failed to find coordinates for this location.';
  }
};

// Geocode an address
const geocodeAddress = async (address) => {
  const url = `https://api.mapbox.com/geocoding/v5/mapbox.places/${encodeURIComponent(
    address
  )}.json?access_token=${mapboxgl.accessToken}&country=au&limit=1`;
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('Geocoding failed');
    const data = await response.json();
    if (!data.features?.length) return null;

    const feature = data.features[0];
    return { lat: feature.center[1], lng: feature.center[0] };
  } catch (err) {
    console.error('Mapbox geocoding error:', err);
    return null;
  }
};

// Use current location
const useMyLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const { longitude, latitude } = position.coords;
        map.value.flyTo({
          center: [longitude, latitude],
          zoom: 14,
          essential: true
        });

        if (marker.value) {
          marker.value.setLngLat([longitude, latitude]);
        } else {
          marker.value = new mapboxgl.Marker({ color: '#0078FF' })
            .setLngLat([longitude, latitude])
            .addTo(map.value);
        }

        coordinates.value = {
          lat: latitude,
          lng: longitude
        };

        locationStr.value = 'My Location';
        findVegetationData([longitude, latitude]);
      },
      (error) => {
        console.error('Failed to get location:', error);
        error.value = 'Failed to get your location: ' + error.message;
      },
      { enableHighAccuracy: true }
    );
  } else {
    error.value = 'Your browser does not support geolocation';
  }
};

// Find vegetation data
const findVegetationData = (coordinates) => {
  if (!map.value) return;

  isLoading.value = true;
  error.value = '';

  setTimeout(() => {
    try {
      const features = map.value.queryRenderedFeatures(
        map.value.project(coordinates),
        { layers: ['veg-choropleth'] }
      );

      if (features.length > 0) {
        const props = features[0].properties;
        locationInfo.value = {
          name: props.LOC_NAME,
          postcode: props.Postcode,
          vegRate: parseFloat(props.VegRate).toFixed(1),
          treeRate: parseFloat(props.TreeRate).toFixed(1)
        };
      } else {
        locationInfo.value = null;
        error.value = 'No vegetation data available for this location.';
      }
    } catch (err) {
      console.error('Error finding vegetation data:', err);
      error.value = 'Failed to retrieve vegetation data.';
    } finally {
      isLoading.value = false;
    }
  }, 500);
};

onMounted(async () => {
  setTimeout(() => {
    try {
      map.value = new mapboxgl.Map({
        container: mapContainer.value,
        style: 'mapbox://styles/mapbox/light-v10',
        center: [144.9931, -37.8136],
        zoom: 9
      });

      map.value.addControl(new mapboxgl.NavigationControl(), 'top-left');
      map.value.addControl(new mapboxgl.FullscreenControl(), 'top-right');
      map.value.addControl(new mapboxgl.ScaleControl(), 'bottom-left');

      marker.value = new mapboxgl.Marker()
        .setLngLat([144.9931, -37.8136])
        .addTo(map.value);

      map.value.on('load', async () => {
        try {
          const res = await fetch(`${API_BASE_URL}/api/geojson`);
          const geojson = await res.json();

          map.value.addSource('suburbs', {
            type: 'geojson',
            data: geojson
          });

          map.value.addLayer({
            id: 'veg-choropleth',
            type: 'fill',
            source: 'suburbs',
            paint: {
              'fill-color': [
                'interpolate', ['linear'], ['get', 'VegRate'],
                0, '#f7fcf5',
                25, '#c7e9c0',
                50, '#74c476',
                75, '#238b45',
                100, '#00441b'
              ],
              'fill-opacity': 0.7,
              'fill-outline-color': '#888'
            }
          });

          map.value.addLayer({
            id: 'suburb-boundaries',
            type: 'line',
            source: 'suburbs',
            paint: {
              'line-color': '#555',
              'line-width': 1
            }
          });

          const popup = new mapboxgl.Popup({
            closeButton: false,
            closeOnClick: false,
            maxWidth: '300px'
          });

          map.value.on('mousemove', 'veg-choropleth', e => {
            map.value.getCanvas().style.cursor = 'pointer';
            const props = e.features[0].properties;
            popup.setLngLat(e.lngLat)
              .setHTML(`
                <strong>${props.LOC_NAME}</strong><br/>
                Postcode: ${props.Postcode}<br/>
                Vegetation Rate: ${parseFloat(props.VegRate).toFixed(1)}%<br/>
                Tree Coverage: ${parseFloat(props.TreeRate).toFixed(1)}%
              `)
              .addTo(map.value);
          });

          map.value.on('mouseleave', 'veg-choropleth', () => {
            map.value.getCanvas().style.cursor = '';
            popup.remove();
          });

          map.value.on('click', 'veg-choropleth', e => {
            const props = e.features[0].properties;
            locationInfo.value = {
              name: props.LOC_NAME,
              postcode: props.Postcode,
              vegRate: parseFloat(props.VegRate).toFixed(1),
              treeRate: parseFloat(props.TreeRate).toFixed(1)
            };
            locationStr.value = props.LOC_NAME;
            coordinates.value = {
              lat: e.lngLat.lat,
              lng: e.lngLat.lng
            };
            marker.value.setLngLat(e.lngLat);
          });

        } catch (err) {
          console.error('Load GeoJSON failed', err);
          error.value = 'Failed to load map data. Please try again later.';
        }
      });
    } catch (err) {
      console.error("Map initialization error:", err);
      error.value = "Failed to initialize map. Please refresh the page.";
    }
  }, 500);
});
</script>

<style scoped>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.veg-map-wrapper {
  width: 100%;
  overflow-x: hidden;
  display: flex;
  justify-content: center;
  background-color: #f9f9f9;
}

.veg-map-container {
  width: 100%;
  padding: 20px;
  font-family: 'Poppins', Arial, sans-serif;
  color: #333;
}

.map-title {
  font-size: 2rem;
  margin-bottom: 20px;
  position: relative;
  padding-bottom: 12px;
  text-align: center;
  color: #2c3e50;
}

.map-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 3px;
  background: linear-gradient(to right, #2c9d44, #1a5829);
}

h3 {
  font-size: 1.5rem;
  margin-bottom: 1.2rem;
  position: relative;
  padding-bottom: 10px;
  color: #2c3e50;
}

h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(to right, #2c9d44, #1a5829);
}

.search-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.address-input-wrapper {
  position: relative;
  flex: 1;
  min-width: 250px;
}

.address-input {
  width: 100%;
  padding: 12px 15px;
  font-size: 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
  transition: all 0.3s ease;
}

.address-input:focus {
  border-color: #2c9d44;
  box-shadow: 0 0 0 2px rgba(44, 157, 68, 0.2);
}

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: white;
  border: 1px solid #ddd;
  border-top: none;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-height: 200px;
  overflow-y: auto;
}

.suggestion-item {
  padding: 10px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
  text-align: left;
}

.suggestion-item:hover {
  background-color: #f0f8f0;
}

.btn-primary {
  background: linear-gradient(135deg, #2c9d44, #1a5829);
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  border-radius: 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  min-width: 120px;
}

.btn-primary:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.location-button {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  background-color: #2196F3;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  min-width: 180px;
}

.location-button:hover {
  background-color: #0b7dda;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.location-icon {
  margin-right: 8px;
}

.map-wrapper {

  width: 1200px;
  display: flex;
  justify-content: center;

}

.map-container {
  position: relative;
  width: 1200px;
  height: 600px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.map {
  width: 100%;
  height: 100%;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(44, 157, 68, 0.1);
  border-radius: 50%;
  border-top-color: #2c9d44;
  animation: spin 1s linear infinite;
  margin-bottom: 10px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.bottom-section {
  margin-top: 30px;
}

.veg-data-section {
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.veg-display {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.veg-circle,
.tree-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.veg-value,
.tree-value {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1;
}

.veg-type,
.tree-type {
  font-size: 0.9rem;
  font-weight: 500;
  margin-top: 5px;
}

.veg-location {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin: 20px 0;
  text-align: center;
}

.location-name {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

.postcode {
  color: #555;
  margin: 5px 0;
}

.coordinates {
  color: #666;
  font-size: 0.9rem;
}

.veg-scale-container {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 20px 0;
  gap: 10px;
}

.veg-label {
  font-weight: 500;
  font-size: 0.9rem;
  color: #333;
}

.low-label {
  color: #666;
}

.high-label {
  color: #238b45;
}

.veg-meter-scale {
  display: flex;
  width: 70%;
  height: 15px;
  border-radius: 10px;
  overflow: hidden;
}

.scale-segment {
  flex: 1;
  height: 100%;
  background: linear-gradient(to right, rgba(35, 139, 69, 0.3), rgba(35, 139, 69, 1));
}

.veg-summary {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 10px;
  margin-top: 20px;
  text-align: center;
}

.veg-summary p {
  margin: 0;
  line-height: 1.5;
}

.no-data-message {
  padding: 40px 20px;
  text-align: center;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  color: #666;
}

.error-section {
  background-color: #ffebee;
  border-left: 4px solid #f44336;
  padding: 15px 20px;
  margin-bottom: 20px;
  border-radius: 4px;
}

.error-message {
  color: #d32f2f;
  margin: 0;
}

@media (max-width: 768px) {
  .veg-display {
    flex-direction: column;
    gap: 20px;
  }

  .search-section {
    flex-direction: column;
  }

  .address-input-wrapper {
    width: 100%;
  }

  .btn-primary, .location-button {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .map-container {
    height: 400px;
  }

  .veg-map-container {
    padding: 15px;
  }
}

@media screen and (-ms-high-contrast: active), (-ms-high-contrast: none) {
  .map-container {
    width: 98%;
  }
}

@supports (-moz-appearance:none) {
  .map {
    margin-left: 1px;
  }
}
</style>