import { createApp } from 'vue'
import App from './App.vue'
import { makeServer } from "./server"
import '@xai-demonstrator/xaidemo-ui/lib/xaidemo-ui.css'

if (process.env.NODE_ENV === "development") {
  makeServer()
}

const app = createApp(App)
app.mount('#app')
