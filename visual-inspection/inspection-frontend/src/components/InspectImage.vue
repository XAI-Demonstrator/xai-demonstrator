<template>
  <div class="inspector">
    <MultiBounce v-if="!prediction"
                 v-bind:numberOfDots="3"/>
    <p v-show="prediction && currentPrediction">{{ $t('answer', {object: prediction}) }}</p>
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
    model_id: null,
    currentPrediction: {
      type: Boolean,
      value: false
    }
  },
  methods: {
    async predict(blob) {
      this.prediction = null;

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
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      cancelTokens: []
    }
  }
}
</script>

<i18n>
{
  "de": {
    "answer": "„Das ist {object}“"
  },
  "en": {
    "answer": "\"This is {object}\""
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
