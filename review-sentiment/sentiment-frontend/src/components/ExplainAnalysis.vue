<template>
  <div>
    <button v-on:click="requestExplanation" v-if="!explanationResult" class="xd-button xd-primary">
      <label>Wie kommst du zu dieser Einschätzung?</label>
    </button>
    <div class="explanation-container" v-if="explanationResult">
      <p>Die Wörter deines Reviews tragen wie folgt zur Bewertung bei:</p>
      <BarChart v-if="explanationResult" v-bind:explanation="explanationResult"></BarChart>
      <TextHighlight v-if="explanationResult != null" v-bind:explanation="explanationResult"></TextHighlight>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
import {Indicator} from "mint-ui";

import TextHighlight from "@/components/TextHighlight";
import BarChart from "@/components/BarChart";

export default {
  name: 'ExplainAnalysis',
  components: {BarChart, TextHighlight},
  data() {
    return {
      explanationResult: null,
      backendUrl: process.env.VUE_APP_BACKEND_URL
    }
  },
  props: [
    "reviewText"
  ],
  methods: {
    requestExplanation() {
      Indicator.open()
      this.resetComponent()

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
                Indicator.close()
              }
          )
    },
    resetComponent() {
      this.explanationResult = null
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
</style>
