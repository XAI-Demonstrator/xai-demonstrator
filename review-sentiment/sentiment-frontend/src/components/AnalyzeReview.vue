<template>
  <div class="sentiment">
    <mt-button type="primary" size="large" v-on:click="analysisRequested" v-if="!numOfStars" class="my-button">Wie viele
      Sterne sollte
      meine Bewertung
      erhalten?
    </mt-button>
    <div class="sentiment-stars" v-if="numOfStars"><img class="my-star" src="@/assets/star.svg" v-for="star in numOfStars" :key="star" /></div>
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
            this.$emit('analysisCompleted', this.numOfStars)
            Indicator.close()
          })
    },
    resetComponent() {
      this.numOfStars = null
    }
  }
}
</script>
<style scoped>
.sentiment {
  height: 3em;
  width: 100%;
  margin-top: 5px;
  margin-bottom: 5px;
}

.sentiment-stars {
  /*border: 1px solid #357EC7;*/
  display: inline-flex;
  align-items: center;
  height: 100%;
}

.my-star {
  height: 25px;
  margin-right: 5px;
}

.my-button {
  background-color: #77A6F7;
  border-radius: 0;
  font-size: 1em;
  font-weight: normal;
  height: auto;
  padding: 10px;
}
</style>
