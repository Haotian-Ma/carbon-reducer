<template>
    <o-map style="height: 600px; width: 100%;">
      <!-- 视图：中心点 & 缩放 -->
      <o-view :center="center" :zoom="zoom" />
  
      <!-- 瓦片图层：OpenStreetMap -->
      <o-layer-tile>
        <o-source-osm />
      </o-layer-tile>
  
      <!-- 如果有 GeoJSON 数据，可用矢量图层渲染 -->
      <o-layer-vector>
        <o-source-vector :features="features" />
      </o-layer-vector>
    </o-map>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { fromLonLat } from 'ol/proj'
  import GeoJSON from 'ol/format/GeoJSON'
  import { Vector as VectorSource } from 'ol/source'
  import { Feature } from 'ol'
  import { Style, Fill, Stroke } from 'ol/style'
  
  const center = ref(fromLonLat([144.9631, -37.8136]))  // 墨尔本经纬度转投影
  const zoom   = ref(9)
  const features = ref([])
  
  onMounted(async () => {
    // 从后端拉 GeoJSON
    const res = await fetch('/api/geojson')
    const gj = await res.json()
    
    // 使用 OpenLayers 的 GeoJSON 格式化器
    const format = new GeoJSON()
    features.value = format.readFeatures(gj, {
      featureProjection: 'EPSG:3857'
    }).map(f => {
      // 可选：给每个要素设置样式
      f.setStyle(new Style({
        fill: new Fill({ color: 'rgba(42,157,143,0.6)' }),
        stroke: new Stroke({ color: '#264653', width: 1 })
      }))
      return f
    })
  })
  </script>
  