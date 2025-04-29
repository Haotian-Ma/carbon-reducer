<template>
  <div class="veg-map-container">
    <h2 class="map-title">Vegetation Coverage Map</h2>
    <div ref="mapContainer" class="map"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
// Mapbox Access Token
mapboxgl.accessToken = import.meta.env.VITE_MAPBOX_TOKEN || '<YOUR_MAPBOX_TOKEN>'

const mapContainer = ref(null)

onMounted(async () => {
  const map = new mapboxgl.Map({
    container: mapContainer.value,
    style: 'mapbox://styles/mapbox/light-v10',
    center: [144.9931, -37.8136],
    zoom: 9
  })

  map.addControl(new mapboxgl.NavigationControl(), 'top-left')

  map.on('load', async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/geojson`)
      const geojson = await res.json()

      map.addSource('suburbs', {
        type: 'geojson',
        data: geojson
      })

      map.addLayer({
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
      })

      // Tooltip
      const popup = new mapboxgl.Popup({ closeButton: false, closeOnClick: false })
      map.on('mousemove', 'veg-choropleth', e => {
        map.getCanvas().style.cursor = 'pointer'
        const props = e.features[0].properties
        popup.setLngLat(e.lngLat)
          .setHTML(`
            <strong>${props.LOC_NAME}</strong><br/>
            Postcode: ${props.Postcode}<br/>
            VegRate: ${parseFloat(props.VegRate).toFixed(1)}%<br/>
            TreeRate: ${parseFloat(props.TreeRate).toFixed(1)}%
          `)
          .addTo(map)
      })
      map.on('mouseleave', 'veg-choropleth', () => {
        map.getCanvas().style.cursor = ''
        popup.remove()
      })
    } catch (err) {
      console.error('load GeoJSON failed', err)
    }
  })
})
</script>

<style scoped>
.veg-map-container {
  padding: 20px;
  text-align: center;
}
.map-title {
  font-size: 1.5rem;
  margin-bottom: 10px;
  color: #333;
  text-align: center;
}
.map {
  display: inline-block;
  width: 80vw;
  height: 600px;
  border-radius: 8px;
  overflow: hidden;
}
</style>
