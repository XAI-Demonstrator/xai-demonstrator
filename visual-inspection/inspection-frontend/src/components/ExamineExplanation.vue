<template>
  <div style="background-color: #00887A; height: 100%;" v-on:click="requestExplanation">
    {{ explanation }}
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "ExamineInspection",
  methods: {
    requestExplanation() {
      console.log("Explanation Request!")
      axios.post(this.backendUrl + '/explain')
          .then(response => {
            this.explanation = response.data.explanation
          })
    }
  },
  data() {
    return {
      explanation: "",
      backendUrl: process.env.VUE_APP_BACKEND_URL
    }
  }
}
</script>

<style scoped>

</style>