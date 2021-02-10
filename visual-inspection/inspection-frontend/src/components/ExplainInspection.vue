<template>
  <section>
    <div class="explanation-request">
      <mt-button class="request-button"
                 v-show="!waitingForExplanation"
                 v-bind:disabled="!predictionReady"
                 v-on:click="buttonClicked">
        Woran erkennst du das?
      </mt-button>
      <mt-spinner v-if="waitingForExplanation" type="triple-bounce"/>
    </div>
  </section>
</template>

<script>
import axios from "axios";

export default {
  name: "ExplainInspection",
  props: {
    predictionReady: {
      type: Boolean,
      default: false
    }
  },
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
.explanation-request {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
}

.request-button {
  background-color: #77A6F7;
  border-radius: 3px;
  font-size: 1em;
  font-weight: normal;
  height: 100%;
  padding: 10px;
  color: white;
  width: 100%;
}
</style>
