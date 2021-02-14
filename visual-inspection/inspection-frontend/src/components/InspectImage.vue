<template>
  <div class="inspector">
    <MultiBounce v-if="!prediction"
                 v-bind:numberOfDots="3" />
    <p v-show="prediction && currentPrediction">„Das ist ein/e {{ prediction }}“</p>
  </div>
</template>

<script>
import axios from 'axios'
import {MultiBounce} from '@xai-demonstrator/xaidemo-ui'

export default {
  name: "InspectImage",
  components: {
    MultiBounce
  },
  props: {
    currentPrediction: {
      type: Boolean,
      value: false
    }
  },
  methods: {
    predict(blob) {
      this.prediction = null;

      const form = new FormData();
      form.append('file', blob);

      axios.post(this.backendUrl + '/predict', form)
          .then(response => {
            this.prediction = response.data.class_label
            this.$emit('inspection-completed')
          })
    }
  },
  data() {
    return {
      prediction: null,
      backendUrl: process.env.VUE_APP_BACKEND_URL
    }
  }
}
</script>

<style scoped>
.inspector {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  min-height: 30px;
}
</style>
