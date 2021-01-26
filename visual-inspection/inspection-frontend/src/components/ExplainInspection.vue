<template>
  <div class="explainer">
    <div class="explanation-request">
      <mt-button class="request-button"
                 v-show="!waitingForExplanation"
                 v-on:click="buttonClicked">„Woran erkennst du das?“
      </mt-button>
      <mt-spinner v-if="waitingForExplanation" type="triple-bounce"/>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ExplainInspection",
  methods: {
    buttonClicked() {
      this.$emit('explanationRequested')
    },
    explain(blob) {
      this.waitingForExplanation = true;

      const form = new FormData();
      form.append('file', blob);

      axios.post(this.backendUrl + '/explain', form)
          .then(response => {
            this.$emit('explanationReceived', response.data.image)
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

<style scoped>
.explainer {
  width: 100%;
  margin-top: 5px;
  margin-bottom: 5px;
}

.explanation-request {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px 10px;
}

.request-button {
  background-color: #77A6F7;
  border-radius: 0;
  font-size: 1em;
  font-weight: normal;
  padding-left: 5px;
  padding-right: 5px;
}
</style>
