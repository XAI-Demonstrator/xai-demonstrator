<template>
  <div class="inspector">
    <MultiBounce v-if="!prediction"
                 v-bind:numberOfDots="3"/>
     <p v-if="show_probability_percentage"
        v-show="prediction && currentPrediction">{{ $t('answer1', {percentage: probability}, {object: prediction}) }}</p>
     <p v-else 
        v-show="prediction && currentPrediction">{{ $t('answer2', {object: prediction}) }}</p>
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
    async predict(blob) {
      this.prediction = null;
      this.probability = null;

      while (this.cancelTokens.length > 0) {
        this.cancelTokens.pop().cancel()
      }

      const source = axios.CancelToken.source();
      this.cancelTokens.push(source);

      const form = new FormData();
      form.append('file', blob);
      form.append('language', this.$i18n.locale)

      await axios.post(this.backendUrl + '/predict', form, {
        cancelToken: source.token
      })
          .then(response => {
            this.prediction = response.data.class_label
            this.probability = response.data.probability
            this.$emit('inspection-completed')
          })
          .catch(error => {
            console.log(error)
          })
    }
  },
  data() {
    return {
      prediction: null,
      probability: null,
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      cancelTokens: [],
      show_probability_percentage: process.env.VUE_APP_SHOW_PROBABILITY_PERCENTAGE
    }
  }
}
</script>

<i18n>
{
  "de": {
     "answer1": "„Das ist zu {percentage} % {object}“",
     "answer2": "„Das ist {object}“"
  },
  "en": { 
    "answer1": "\"This is with a probability of {percentage} % {object}\"",
    "answer2": "\"This is {object}\""
    }
}
</i18n>

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
