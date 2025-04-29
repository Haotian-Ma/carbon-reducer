<template>
    <div class="map-page">
      <section class="section-group">
        <h2 class="section-group-title">Vegetation Coverage Map</h2>
        <div class="map-container">
          <iframe
            :src="mapUrl"
            frameborder="0"
            style="width:100%; height:600px;"
          ></iframe>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
const rawBase = import.meta.env.VITE_API_BASE_URL

const origin = window.location.origin

const API_BASE_URL = rawBase && rawBase !== origin
  ? rawBase
  : ''

const mapUrl = `${API_BASE_URL}/api/map`
  </script>
  
  <style scoped>
  .map-container {
    margin-bottom: 40px;
  }
  </style>
  