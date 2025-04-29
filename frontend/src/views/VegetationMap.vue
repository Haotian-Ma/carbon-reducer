<template>
  <l-map
    ref="mapRef"
    :zoom="9"
    :center="[-37.8136, 144.9631]"
    style="height: 600px; width: 100%"
  >
    <l-tile-layer
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />

    <l-geo-json
      v-if="geoJsonData"
      :geojson="geoJsonData"
      :options-style="styleFeature"
      :options-onEachFeature="onEachFeature"
    />
  </l-map>
</template>

<script>
import { LMap, LTileLayer, LGeoJson } from '@vue-leaflet/vue-leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet-control-geocoder'
import L from 'leaflet'
import axios from 'axios'

export default {
  name: 'VegetationMap',
  components: {
    LMap,
    LTileLayer,
    LGeoJson
  },
  data() {
    return {
      geoJsonData: null,
      map: null
    }
  },
  mounted() {

    axios.get('/geo_sub_data.geojson')
      .then(res => {
        this.geoJsonData = res.data
      })
      .catch(err => console.error('GeoJSON failed', err))

    this.$nextTick(() => {
      this.map = this.$refs.mapRef.mapObject
      L.Control.geocoder({ defaultMarkGeocode: false })
        .on('markgeocode', e => {
          this.map.fitBounds(e.geocode.bbox)
        })
        .addTo(this.map)
    })
  },
  methods: {
    styleFeature(feature) {
      const rate = feature.properties.VegRate
      return {
        fillColor: rate > 50 ? '#006400' : rate > 25 ? '#7CFC00' : '#ADFF2F',
        fillOpacity: 0.7,
        weight: 0.5,
        color: '#000'
      }
    },
    onEachFeature(feature, layer) {
      const p = feature.properties
      layer.bindTooltip(
        `<strong>${p.LOC_NAME}</strong><br/>
         Veg: ${p.VegRate.toFixed(1)}%<br/>
         Tree: ${p.TreeRate.toFixed(1)}%`
      )
    }
  }
}
</script>
