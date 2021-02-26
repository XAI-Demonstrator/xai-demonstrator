<template>
  <div>
    <button v-on:click="requestExplanation"
            v-if="!explanationResult"
            class="xd-button xd-secondary"
            v-bind:disabled="waitingForExplanation">
      <label>Wie kommst du zu dieser Einschätzung?</label>
    </button>
    <div class="explanation-container" v-if="explanationResult">
      <p>Die Wörter deines Reviews tragen wie folgt zur Bewertung bei:</p>
      <BarChart v-if="explanationResult" v-bind:explanation="explanationResult"></BarChart>
      <TextHighlight v-if="explanationResult != null" v-bind:explanation="explanationResult"></TextHighlight>
    </div>
    <SpinningIndicator class="indicator" v-bind:visible="waitingForExplanation"/>
  </div>
</template>
<script>
import axios from 'axios'
import { SpinningIndicator } from '@xai-demonstrator/xaidemo-ui';

import TextHighlight from "@/components/TextHighlight";
import BarChart from "@/components/BarChart";

export default {
  name: 'ExplainAnalysis',
  components: {
    BarChart,
    TextHighlight,
    SpinningIndicator
  },
  data() {
    return {
      explanationResult: null,
      waitingForExplanation: false,
      backendUrl: process.env.VUE_APP_BACKEND_URL
    }
  },
  props: [
    "reviewText"
  ],
  methods: {
    requestExplanation() {
      this.resetComponent()
      this.waitingForExplanation = true

      let data = {"text": this.reviewText}

      let params = new URLSearchParams(window.location.search.substring(1));
      let method = params.get('method');
      if (method) {
        data.method = method;
      }

      axios
          .post(this.backendUrl + '/explain', data)
          .then(response => {
                this.explanationResult = response.data.explanation.map(function (pair) {
                  return {
                    word: pair[0],
                    score: pair[1]
                  }
                })
                this.waitingForExplanation = false
              }
          )
    },
    resetComponent() {
      this.explanationResult = null
      this.waitingForExplanation = false
    }
  }
}
</script>
<style scoped>
.explanation-container {
  display: flex;
  flex-direction: column;
}

.explanation-container div {
  margin-bottom: 8px;
  border-radius: 3px;
}

.explanation-container div:last-child {
  margin-bottom: 0;
}

.indicator {
  z-index: 9;
}
</style>
