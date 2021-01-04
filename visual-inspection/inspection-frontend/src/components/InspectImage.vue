<template>
  <div>
    <p v-if="prediction">Ich erkenne einen {{ prediction }}</p>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "InspectImage",
  methods: {
    predict(index) {

      this.prediction = ""

      axios.post(this.backendUrl + '/predict', {"index": index})
          .then(response => {
            this.prediction = response.data.prediction
            this.$emit('predictionReceived')
          })
    }
  },
  data() {
    return {
      prediction: "",
      backendUrl: process.env.VUE_APP_BACKEND_URL
    }
  }
}
</script>

<style scoped>

</style>