<template>
  <div id="app">
    <mt-header fixed title="Visual Inspection" class="navigation-header">
      <a href="/" slot="left" v-if="backendUrl">
        <mt-button icon="back"></mt-button>
      </a>
      <a href="./" slot="right">
        <mt-button><span style="font-size: 16px; font-weight:bold;">↻</span></mt-button>
      </a>
    </mt-header>
    <div id="image-container">
      <SelectImage v-if="!explainMode" v-on:imageChanged="imageChanged"/>
      <ExamineExplanation ref="examiner" v-if="explainMode"/>
    </div>
    <InspectImage ref="inspector" v-on:predictionReceived="predictionReceived" />
    <ExplainInspection v-if="!selectionMode && !explainMode"
                       v-on:explanationRequested="explanationRequested"/>
  </div>
</template>

<script>

import SelectImage from "@/components/SelectImage";
import InspectImage from "@/components/InspectImage";
import ExamineExplanation from "@/components/ExamineExplanation";
import ExplainInspection from "@/components/ExplainInspection";

export default {
  name: 'App',
  components: {ExamineExplanation, SelectImage, InspectImage, ExplainInspection},
  methods: {
    imageChanged(index) {
      this.$refs.inspector.predict(index)
      this.selectionMode = true
    },
    explanationRequested() {
      console.log("Requested Click")
      this.selectionMode = false
      this.explainMode = true
      this.$refs.examiner.requestExplanation()
    },
    predictionReceived() {
      console.log("Received Prediction")
      this.selectionMode = false
    }
  },
  data() {
    return {
      selectionMode: true,
      explainMode: false,
      backendUrl: process.env.VUE_APP_BACKEND_URL
    }
  },
  created() {
    document.title = "Visual Inspection – XAI Demonstrator"
  },
  mounted() {
    this.$refs.inspector.predict(0)
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 50px;
}

#image-container {
  height: 70vh;
  max-height: 400px;
  margin-bottom: 10px;
}

.navigation-header {
  background-color: #77A6F7 !important;
}

.mint-indicator-wrapper {
  background-color: #00887A !important;
}

.mint-spinner-snake {
  border-top-color: #D3E3FC !important;
  border-bottom-color: #D3E3FC !important;
  border-left-color: #D3E3FC !important;
}

@media screen and (min-width: 450px) {
  body {
    background-color: #FFFFFF;
  }

  #app {
    margin: 40px auto auto;
    max-width: 425px;
    border: 1px solid #D3E3FC;
    padding: 5px;
  }

  .navigation-header {
    margin: auto;
    max-width: 437px;
  }
}
</style>
