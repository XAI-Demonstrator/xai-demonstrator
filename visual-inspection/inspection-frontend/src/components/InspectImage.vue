<template>
  <section>
    <mt-spinner v-show="!prediction" type="triple-bounce"></mt-spinner>
    <span v-show="prediction && currentPrediction">„Das ist ein/e {{ prediction }}“</span>
  </section>
</template>

<script>
import axios from 'axios'

export default {
  name: "InspectImage",
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
            this.$emit('inspectionCompleted')
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

</style>
