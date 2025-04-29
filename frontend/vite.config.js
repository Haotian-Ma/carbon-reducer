import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  base: '/',
  plugins: [vue()],
  optimizeDeps: {
    // force Vite to pre‐bundle these two
    include: [
      'mapbox-gl',
      '@mapbox/mapbox-gl-geocoder'
    ],
  }
})
