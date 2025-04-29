<template>
    <o-map style="height: 600px; width: 100%;">
      <o-view :center="center" :zoom="zoom" />
  
      <o-layer-tile>
        <o-source-osm />
      </o-layer-tile>
  
      <o-layer-vector>
        <o-source-vector :features="features" />
      </o-layer-vector>
    </o-map>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { fromLonLat } from 'ol/proj'
  import GeoJSON from 'ol/format/GeoJSON'
  
  const center = ref(fromLonLat([144.9631, -37.8136]))
  const zoom   = ref(9)
  const features = ref([])
  
  onMounted(async () => {
    try {
      const res = await fetch('/api/geojson')
      const gj  = await res.json()
      const format = new GeoJSON()
      features.value = format.readFeatures(gj, {
        featureProjection: 'EPSG:3857'
      })
    } catch (err) {
      console.error('加载 GeoJSON 失败', err)
    }
  })
  </script>
  