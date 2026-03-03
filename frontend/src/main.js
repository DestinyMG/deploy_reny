// src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router' // Importamos la configuración de rutas
import './style.css'

const app = createApp(App)

// Usamos el router
app.use(router)

// Montamos la aplicación
app.mount('#app')