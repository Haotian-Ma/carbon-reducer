<template>
  <l-map
    ref="mapRef"
    :zoom="9"
    :center="[-37.8136, 144.9631]"
    style="height: 600px; width: 100%;"
    @ready="onMapReady"
  >
    <l-tile-layer
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    />

    <l-geo-json
      v-if="geoJsonData"
      :geojson="geoJsonData"
      :options-style="styleFeature"
      :options-on-each-feature="onEachFeature"
    />
  </l-map>
</template>

<script>
import { LMap, LTileLayer, LGeoJson } from '@vue-leaflet/vue-leaflet'
import L from 'leaflet'
import axios from 'axios'
import 'leaflet-control-geocoder'
import 'leaflet-control-geocoder/dist/Control.Geocoder.css'

export default {
  name: 'VegetationMap',
  components: { LMap, LTileLayer, LGeoJson },
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
  },
  methods: {
    onMapReady(mapInstance) {
      this.map = mapInstance
      const nominatim = L.Control.Geocoder.nominatim()
      L.Control.geocoder({
        geocoder: nominatim,
        defaultMarkGeocode: false
      })
      .on('markgeocode', e => {
        this.map.fitBounds(e.geocode.bbox)
      })
      .addTo(this.map)
    },
    styleFeature(feature) {
      const rate = feature.properties.VegRate
      return {
        fillColor: rate > 50 ? '#006400'
                  : rate > 25 ? '#7CFC00'
                  : '#ADFF2F',
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

<style>
.leaflet-control-geocoder-form {
  background: white;
  padding: 4px;
  border-radius: 4px;
}
</style>
