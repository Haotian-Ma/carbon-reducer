import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
// import PrimeVue from 'primevue/config'
// import Aura from '@primevue/themes/aura'
import 'mapbox-gl/dist/mapbox-gl.css'
import '@mapbox/mapbox-gl-geocoder/dist/mapbox-gl-geocoder.css'

const app = createApp(App)  
app.use(router)
app.mount('#app')