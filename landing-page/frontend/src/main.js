import Vue from 'vue'
import App from './App.vue'
import configPlugin from '@/config'
import '@xai-demonstrator/xaidemo-ui/lib/xaidemo-ui.css'

Vue.config.productionTip = false
Vue.use(configPlugin)

new Vue({
  render: h => h(App),
}).$mount('#app')
