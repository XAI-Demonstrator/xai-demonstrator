<template>
  <div>
    <button v-on:click="requestAnalysis"
            v-if="!numOfStars"
            class="xd-button xd-secondary"
            v-bind:disabled="waitingForPrediction">
      <label>{{ $t('question') }}</label>
    </button>
    <div class="the-sentiment" v-if="numOfStars">
      <p>{{ $t('answer') }}</p>
      <div class="sentiment-stars">
        <img class="my-star" src="@/assets/star_filled.svg" v-for="star in numOfStars" :key="'pos-' + star" alt="Filled star"/>
        <img class="my-star" src="@/assets/star_blank.svg" v-for="star in (5 - numOfStars)" :key="'neg-' + star" alt="Unfilled star"/>
      </div>
    </div>
    <SpinningIndicator class="indicator" v-bind:visible="waitingForPrediction" />
  </div>
</template>
<script>
import axios from 'axios';
import { SpinningIndicator } from '@xai-demonstrator/xaidemo-ui';

export default {
  name: 'AnalyzeReview',
  components: {
    SpinningIndicator
  },
  props: [
    "reviewText"
  ],
  data() {
    return {
      numOfStars: null,
      waitingForPrediction: false,
      backendUrl: process.env.VUE_APP_BACKEND_URL
    }
  },
  methods: {
    requestAnalysis() {
      this.resetComponent()
      this.waitingForPrediction = true
      this.$emit('analysisRequested')

      axios.post(this.backendUrl + '/predict', {"text": this.reviewText})
          .then(response => {
            this.numOfStars = response.data.prediction.map((x, i) => [x, i]).reduce((r, a) => (a[0] > r[0] ? a : r))[1] + 1
            this.$emit('analysisCompleted', this.numOfStars)
            this.waitingForPrediction = false
          })
    },
    resetComponent() {
      this.numOfStars = null
      this.waitingForPrediction = false
    }
  }
}
</script>

<i18n>
{
    "de": {
         "question": "Wie viele Sterne sollte meine Bewertung erhalten?",
         "answer": "Ich denke, dein Review entspricht"
    },
    "en": {
         "question": "How many stars would you assign to my review?",
         "answer": "I believe that your review resembles"
    }
}
</i18n>

<style scoped>
.the-sentiment {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.sentiment-stars {
  display: flex;
  flex-direction: row;
  justify-content: space-around;
  align-items: center;
  padding: 5px;
}

.my-star {
  width: 24px;
  margin-left: 3px;
  margin-right: 3px;
}

.indicator {
  z-index: 9;
}
</style>
