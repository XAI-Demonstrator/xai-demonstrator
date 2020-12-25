<template>
  <div v-if="isActive">
    <mt-button type="primary" size="large" v-on:click="explanationRequested">Kannst du diese Entscheidung begründen?
    </mt-button>
    <BarChart v-if="explanationResult" v-bind:explanation="explanationResult"></BarChart>
    <TextHighlight v-if="explanationResult != null" v-bind:explanation="explanationResult"></TextHighlight>
  </div>
</template>
<script>
import axios from 'axios'

import TextHighlight from "@/components/TextHighlight";
import BarChart from "@/components/BarChart";

export default {
  name: 'ExplainAnalysis',
  components: {BarChart, TextHighlight},
  data() {
    return {
      explanationResult: null
    }
  },
  props: [
    "isActive",
    "reviewText"
  ],
  methods: {
    explanationRequested() {
      this.resetComponent()

      axios
          .post('/explain', {"text": this.reviewText})
          .then(response => {
                this.explanationResult = response.data.explanation.explanation.map(function (pair) {
                  return {
                    word: pair[0],
                    score: pair[1]
                  }
                })
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
</style>
