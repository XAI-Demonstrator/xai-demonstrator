<template>
  <div id="configure-model" class="xd-section xd-light">
    <div v-for="(options, classKey) in availableModels" v-bind:key="classKey">
      <ConfigureClass
          v-bind:amounts="options.amounts"
          v-bind:labels="options.labels"
          v-bind:image="options.image"
          v-bind:className="options.name"
          v-bind:classKey="classKey"
          v-bind:ref="classKey"/>
    </div>
  </div>
</template>

<script>
import ConfigureClass from '@/components/ConfigureClass'
import {availableModels} from '@/modelConfig.js'

export default {
  name: "ConfigureModel",
  components: {
    ConfigureClass
  },
  data() {
    return {
      availableModels
    }
  }
}
</script>

<style scoped>

</style>