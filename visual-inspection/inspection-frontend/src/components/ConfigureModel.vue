<template>
    <div class="configurator-menu">
          <div id="smartphone_config" class="configurators">
            <KISettings_Smartphone  ref="configurator"/>
          </div>
          <div id="pencil_config" class="configurators">
            <KISettings_Pencil  ref="configurator"/>
          </div>
          <div id="cup_config" class="configurators">
            <KISettings_Cup  ref="configurator"/>
          </div>
        </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api'

export default defineComponent({
    setup() {
        
    },
})
</script>
