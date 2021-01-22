<template>
  <div class="sentiment">
    <mt-button type="primary" size="large" v-on:click="analysisRequested" v-if="!numOfStars" class="my-button">Wie viele
      Sterne sollte
      meine Bewertung
      erhalten?
    </mt-button>
    <div class="the-sentiment" v-if="numOfStars">
      <p>Ich denke, dein Review entspricht</p>
      <div class="sentiment-stars">
        <img class="my-star" src="@/assets/star_filled.svg" v-for="star in numOfStars" :key="'pos-' + star"/>
        <img class="my-star" src="@/assets/star_blank.svg" v-for="star in (5 - numOfStars)" :key="'neg-' + star"/>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import { Indicator } from 'mint-ui';

export default {
  name: 'AnalyzeReview',
  props: [
    "reviewText"
  ],
  data() {
    return {
      numOfStars: null,
      backendUrl: process.env.VUE_APP_BACKEND_URL
    }
  },
  methods: {
    analysisRequested() {
      Indicator.open()

      this.resetComponent()
      this.$emit('analysisRequested')

      axios.post(this.backendUrl + '/predict', {"text": this.reviewText})
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

.the-sentiment {
  /*border: 1px solid #357EC7;*/
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.sentiment-stars {
  min-width: 151px;
}

.my-star {
  width: 25px;
  margin-left: 5px;
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
