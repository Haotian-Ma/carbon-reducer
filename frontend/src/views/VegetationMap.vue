<template>
    <div class="map-wrapper">
      <l-map
        v-if="geojson"
        :zoom="zoom"
        :center="center"
        style="height: 600px; width: 100%;"
      >
        <!-- 这里用 CartoDB Positron 底图，也可以改成 OSM、Mapbox 等 -->
        <l-tile-layer
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        />
        <l-geo-json
          :geojson="geojson"
          :options="geoOptions"
        />
      </l-map>
  
      <!-- 等待加载时 -->
      <div v-else class="loading">正在加载地图数据…</div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  // 从 vue-leaflet 里按需引入
 import { LMap, LTileLayer, LMarker } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
  
  const center = ref([-37.8136, 144.9631])  // 墨尔本中心
  const zoom   = ref(9)
  const geojson = ref(null)
  
  // 配置 GeoJSON 样式和 tooltip
  const geoOptions = {
    style: feature => ({
      fillColor: '#2a9d8f',
      color: '#264653',
      weight: 1,
      fillOpacity: 0.6,
    }),
    onEachFeature: (feature, layer) => {
      const props = feature.properties
      layer.bindTooltip(`
        <strong>Suburb:</strong> ${props.LOC_NAME}<br/>
        <strong>VegRate:</strong> ${props.VegRate}%
      `)
    }
  }
  
  onMounted(async () => {
    try {
      const res = await fetch('/api/geojson')
      geojson.value = await res.json()
    } catch (err) {
      console.error('加载 GeoJSON 失败', err)
    }
  })
  </script>
  
  <style>
  .map-wrapper { position: relative; }
  .loading {
    text-align: center;
    padding: 2em;
    font-size: 1.2em;
  }
  </style>
  