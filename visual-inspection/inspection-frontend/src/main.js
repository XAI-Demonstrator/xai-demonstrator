import { createApp } from 'vue'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import {makeServer} from "./server"
import '@xai-demonstrator/xaidemo-ui/lib/xaidemo-ui.css'

if (process.env.NODE_ENV === "development") {
    makeServer()
}

const i18n = createI18n({
    locale: navigator.language.split('-')[0],
    fallbackLocale: 'de',
    messages: {
        "de": {
            "xaidemonstrator": "XAI-Demonstrator"
        },
        "en": {
            "xaidemonstrator": "XAI Demonstrator"
        }
    }
})

const app = createApp(App)
app.use(i18n)
app.mount('#app')
