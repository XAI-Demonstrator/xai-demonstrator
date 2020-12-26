<template>
  <div class="sentiment">
    <mt-button type="primary" size="large" v-on:click="analysisRequested" v-if="!numOfStars">Wie viele Sterne sollte
      meine Bewertung
      erhalten?
    </mt-button>
    <div v-if="numOfStars">{{ sentiment }}</div>
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
      sentiment: '',
      numOfStars: null
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
.sentiment {
  height: 3em;
  display: inline-flex;
  align-items: center;
  margin-top: 5px;
}
</style>
