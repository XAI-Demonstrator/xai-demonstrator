import {createApp} from 'vue'
import Notifications from 'notiwind'
import App from './App.vue'
import '@xai-demonstrator/xaidemo-ui/lib/xaidemo-ui.css'

const app = createApp(App)
app.use(Notifications)
app.mount('#app')
