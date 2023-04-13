<template>
  <div>
    <div class="explanation-request">
      <button class="xd-button xd-secondary"
              v-show="!waitingForExplanation"
              v-bind:disabled="!predictionReady"
              v-on:click="buttonClicked">
        {{ $t('question') }}
      </button>
      <MultiBounce v-if="waitingForExplanation"
                   v-bind:numberOfDots="3"/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {MultiBounce} from '@xai-demonstrator/xaidemo-ui'
import {unflatten} from 'flat';

export default {
  name: "ExplainInspection",
  components: {
    MultiBounce
  },
  props: {
    predictionReady: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    buttonClicked() {
      this.$emit('explanation-requested')
    },
    async explain(blob) {
      this.waitingForExplanation = true;

      const form = new FormData();
      form.append('file', blob);

      const rawParams = Object.fromEntries(new URLSearchParams(window.location.search.substring(1)))
      const allParams = unflatten(rawParams)

      const method = allParams['method'];
      if (method) {
        form.append('method', method);
      }
      else{
        form.append('method', 'visualime');
      }

      const settings = Object
          .keys(allParams)
          .filter((key) => {
            return key !== 'method'
          })
          .filter((key) => {
            return key !== 'embedded'
          })
          .reduce((obj, key) => {
            obj[key] = allParams[key];
            return obj;
          }, {})
      if (settings && Object.keys(settings).length !== 0) {
        form.append('settings', JSON.stringify(settings));
      }

      await axios.post(this.backendUrl + '/explain', form)
          .then(response => {
            this.$emit('explanation-received', response.data.image)
            this.waitingForExplanation = false;
          })
          .catch(error => {
            console.log(error)
            this.waitingForExplanation = false;
          })
    }
  },
  data() {
    return {
      explanation: null,
      waitingForExplanation: false,
      backendUrl: process.env.VUE_APP_BACKEND_URL
    }
  }
}
</script>

<i18n>
{
  "de": {
    "question": "Woran erkennst du das?"
  },
  "en": {
    "question": "How do you know?"
  }
}
</i18n>

<style scoped>
.explanation-request {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  min-height: 60px;
}

</style>
