<template>
  <div class="inspector">
    <div class="inspection-result">
      <p>
        <mt-spinner v-if="!prediction" type="triple-bounce"></mt-spinner>
        <span v-show="prediction && currentPrediction">„Das ist ein/e {{ prediction }}“</span>
      </p>

    </div>
  </div>
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
.inspector {
  width: 100%;
  margin-top: 5px;
  margin-bottom: 5px;
}

.inspection-result {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding-left: 5px;
  padding-right: 5px;
}
</style>
