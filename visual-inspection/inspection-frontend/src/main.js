import Vue from 'vue'
import App from './App.vue'
import MintUI from 'mint-ui'
import 'mint-ui/lib/style.css'
import { makeServer } from "./server"

Vue.config.productionTip = false
Vue.use(MintUI)

if (process.env.NODE_ENV === "development") {
  makeServer()
}

new Vue({
    render: h => h(App),
}).$mount('#app')
