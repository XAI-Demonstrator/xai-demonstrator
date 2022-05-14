<template>
  <div class="config-container">
    <ConfigureClass v-for="(options, classKey) in availableModels" v-bind:key="classKey"
                    v-bind:amounts="options.amounts"
                    v-bind:labels="options.labels"
                    v-bind:image="options.image"
                    v-bind:className="options.name"
                    v-bind:classKey="classKey"
                    v-bind:ref="classKey"/>
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
.config-container {
  display: flex;
}

@media screen and (max-width: 450px) {
  .config-container {
    flex-direction: column;
    width: 100%;
  }

  .config-container div:last-child {
    margin-bottom: 0;
  }
}

@media screen and (min-width: 450px) and (max-height: 650px) {
  .config-container {
    flex-direction: row;
  }
}

@media screen and (min-width: 450px) and (min-height: 650px) {
  .config-container {
    flex-direction: column;
    width: 100%;
  }

  .config-container div:last-child {
    margin-bottom: 0;
  }
}
</style>