<template>
  <div class="inspector">
    <MultiBounce v-if="!prediction"
                 v-bind:numberOfDots="3"/>
    <p v-if="!prediction && showSlowHint" class="slow-hint">{{ $t('slowHint') }}</p>
    <p v-if="displayProbability"
       v-show="prediction && currentPrediction">{{
        $t('answer_with_probability', {
          percentage: Math.round(probability),
          object: prediction
        })
      }}</p>
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
      this.showSlowHint = false;
      clearTimeout(this.slowHintTimer);
      this.slowHintTimer = setTimeout(() => {
        if (!this.prediction) {
          this.showSlowHint = true;
        }
      }, 3000);

      while (this.cancelTokens.length > 0) {
        this.cancelTokens.pop().cancel()
      }

      const source = axios.CancelToken.source();
      this.cancelTokens.push(source);

      const form = new FormData();
      form.append('file', blob);
      form.append('language', this.$i18n.locale)
      if (this.enableModelConfiguration) {
        form.append('model_id', this.model_id)
      }

      let cancelled = false;
      await axios.post(this.backendUrl + '/predict', form, {
        cancelToken: source.token
      })
          .then(response => {
            this.prediction = response.data.class_label
            this.probability = response.data.probability
            this.$emit('inspection-completed')
          })
          .catch(error => {
            if (axios.isCancel(error)) {
              cancelled = true;
            } else {
              console.log(error)
            }
          })

      if (!cancelled) {
        clearTimeout(this.slowHintTimer);
        this.showSlowHint = false;
      }
    }
  },
  data() {
    return {
      prediction: null,
      probability: null,
      showSlowHint: false,
      slowHintTimer: null,
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      cancelTokens: [],
      /* FEATURE FLAGS */
      enableModelConfiguration: JSON.parse(process.env.VUE_APP_ENABLE_MODEL_CONFIGURATION),
      displayProbability: JSON.parse(process.env.VUE_APP_DISPLAY_PROBABILITY)
    }
  }
}
</script>

<i18n>
{
  "de": {
    "answer_with_probability": "„Das ist zu {percentage}% {object}“",
    "answer_without_probability": "„Das ist {object}“",
    "slowHint": "Einen Moment, die KI startet gerade und ist gleich bereit."
  },
  "en": {
    "answer_with_probability": "\"This is {object} with a probability of {percentage}%\"",
    "answer_without_probability": "\"This is {object}\"",
    "slowHint": "One moment, the AI is starting up and will be ready shortly."
  }
}
</i18n>

<style scoped>
.inspector {
  width: 100%;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  min-height: 30px;
}

.slow-hint {
  width: 100%;
  margin: 6px 0 0;
  text-align: center;
  font-size: 0.85em;
  color: #666;
}
</style>
