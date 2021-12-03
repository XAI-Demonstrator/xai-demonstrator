import { createApp } from 'vue'
import App from './App.vue'
import configPlugin from '@/config'
import '@xai-demonstrator/xaidemo-ui/lib/xaidemo-ui.css'

const app = createApp(App)
app.use(configPlugin)
app.mount('#app')
