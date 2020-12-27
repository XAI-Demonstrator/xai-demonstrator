<template>
  <div v-if="isActive">
    <mt-button type="primary" size="large" v-on:click="explanationRequested" v-if="!explanationResult"
               class="my-button">Kannst du diese
      Entscheidung begründen?
    </mt-button>
    <div class="explanation-container" v-if="explanationResult">
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
      explanationResult: null
    }
  },
  props: [
    "isActive",
    "reviewText"
  ],
  methods: {
    explanationRequested() {
      Indicator.open()

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
  border: 1px solid #77A6F7;
  padding: 0px 5px 5px;
}

.explanation-container div {
  margin-top: 5px;
}

.my-button {
  background-color: #77A6F7;
  border-radius: 0;
  font-size: 1em;
  font-weight: normal;
  height: auto;
  padding: 10px;
}
</style>
