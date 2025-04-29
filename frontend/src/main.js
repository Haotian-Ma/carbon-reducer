import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
// import PrimeVue from 'primevue/config'
// import Aura from '@primevue/themes/aura'
import 'vue3-openlayers/dist/vue3-openlayers.css'
import 'ol/ol.css'
import { createOpenLayers } from 'vue3-openlayers'

const app = createApp(App)  
app.use(router)
app.use(createOpenLayers())  
app.mount('#app')