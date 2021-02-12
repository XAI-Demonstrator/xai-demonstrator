<template>
  <div>
    <button v-on:click="requestAnalysis" v-if="!numOfStars" class="xd-button xd-primary">
      <label>Wie viele Sterne sollte meine Bewertung erhalten?</label>
    </button>
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
import {Indicator} from 'mint-ui';

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
    requestAnalysis() {
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
* {
  box-sizing: border-box;
}

.the-sentiment {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.sentiment-stars {
  background-color: white;
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  padding: 3px;
}

.my-star {
  width: 24px;
  margin-left: 3px;
  margin-right: 3px;
}
</style>
