<template>
  <div class="inspector">
    <MultiBounce v-if="!prediction"
                 v-bind:numberOfDots="3"/>
     <p v-if="show_probability_percentage"
        v-show="prediction && currentPrediction">{{ $t('answer_with_probability', {percentage: probability, object: prediction}) }}</p>
     <p v-else 
        v-show="prediction && currentPrediction">{{ $t('answer_without_probability', {object: prediction}) }}</p>
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
    model_id: {
      type: String
    },
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
      form.append('model_id', this.model_id)

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
      show_probability_percentage: JSON.parse(process.env.VUE_APP_SHOW_PROBABILITY_PERCENTAGE)
    }
  }
}
</script>

<i18n>
{
  "de": {
     "answer_with_probability": "„Das ist zu {percentage} % {object}“",
     "answer_without_probability": "„Das ist {object}“"
  },
  "en": { 
    "answer_with_probability": "\"This is with a probability of {percentage} % {object}\"",
    "answer_without_probability": "\"This is {object}\""
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
