<template>
    <div class="map-wrapper">
      <l-map
        v-if="geojson"
        :zoom="zoom"
        :center="center"
        style="height: 600px; width: 100%;"
      >
        <l-tile-layer
          url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        />
  
        <!-- 这里必须确保 LGeoJson 已注册 -->
        <l-geo-json
          :geojson="geojson"
          :options="geoOptions"
        />
      </l-map>
  
      <div v-else class="loading">正在加载地图数据…</div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import {
    LMap,
    LTileLayer,
    LGeoJson    // ← 新增这一行
  } from '@vue-leaflet/vue-leaflet'
  import 'leaflet/dist/leaflet.css'
  
  const center  = ref([-37.8136, 144.9631])
  const zoom    = ref(9)
  const geojson = ref(null)
  
  // 样式和 tooltip 配置
  const geoOptions = {
    style: () => ({
      fillColor: '#2a9d8f',
      color:     '#264653',
      weight:     1,
      fillOpacity: 0.6,
    }),
    onEachFeature: (feature, layer) => {
      const { LOC_NAME, VegRate } = feature.properties
      layer.bindTooltip(`
        <strong>Suburb:</strong> ${LOC_NAME}<br/>
        <strong>Vegetation Rate:</strong> ${VegRate}%
      `)
    }
  }
  
  // 从环境变量里读后端基础 URL
  const API = import.meta.env.VITE_API_BASE_URL || ''
  
  onMounted(async () => {
    try {
      const res = await fetch(`${API}/api/geojson`)
      if (!res.ok) throw new Error(res.statusText)
      geojson.value = await res.json()
    } catch (err) {
      console.error('加载 GeoJSON 失败:', err)
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
  