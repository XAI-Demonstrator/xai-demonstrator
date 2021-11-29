import Vue from 'vue'
import App from './App.vue'
import '@xai-demonstrator/xaidemo-ui/lib/xaidemo-ui.css'

Vue.config.productionTip = false

new Vue({
    render: h => h(App),
}).$mount('#app')
