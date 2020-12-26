<template>
  <div>
    <mt-button type="primary" size="large" v-on:click="analysisRequested">Wie viele Sterne sollte meine Bewertung
      erhalten?
    </mt-button>
    <p>{{ sentiment }}</p>
  </div>
</template>
<script>
import axios from 'axios'
import {Indicator} from "mint-ui";

export default {
  name: 'AnalyzeReview',
  props: [
    "reviewText"
  ],
  data() {
    return {
      sentiment: ''
    }
  },
  methods: {
    analysisRequested() {
      Indicator.open()

      this.resetComponent()
      this.$emit('analysisRequested')

      axios.post('/predict', {"text": this.reviewText})
          .then(response => {
            this.numOfStars = response.data.prediction.map((x, i) => [x, i]).reduce((r, a) => (a[0] > r[0] ? a : r))[1] + 1
            this.sentiment = "⭐".repeat(this.numOfStars)
            this.$emit('analysisCompleted', this.numOfStars)
            Indicator.close()
          })
    },
    resetComponent() {
      this.sentiment = ''
      this.numOfStars = null
    }
  }
}
</script>
<style scoped>
</style>
