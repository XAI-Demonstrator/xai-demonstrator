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
      <cropper ref="cropper" :src="img" @change="imageChanged"
               :min-width="50" :min-height="30"
               :stencil-component="$options.components.ExplanationStencil"
               :stencil-props="{
                 'explanationMode': currentExplanation,
                 'explanationImg': explanation,
                 'aspectRatio': 1.0}"/>
    </div>
    <InspectImage ref="inspector"
                  v-on:inspectionCompleted="inspectionCompleted"/>
    <ExplainInspection ref="explainer" v-show="currentPrediction"
                       v-on:explanationRequested="explanationRequested"
                       v-on:explanationReceived="explanationReceived"/>
    <ExplanationStencil/>
  </div>
</template>

<script>
import {Cropper} from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css'
import InspectImage from "@/components/InspectImage";
import ExplainInspection from "@/components/ExplainInspection";
import ExplanationStencil from "@/components/ExplanationStencil";

export default {
  name: 'App',
  components: {Cropper, InspectImage, ExplainInspection, ExplanationStencil},
  methods: {
    imageChanged({canvas}) {
      this.currentPrediction = false;
      this.currentExplanation = false;
      canvas.toBlob(this.$refs.inspector.predict)
    },
    inspectionCompleted() {
      this.currentPrediction = true;
    },
    explanationRequested() {
      this.currentExplanation = false;
      this.$refs.cropper.getResult().canvas.toBlob(this.$refs.explainer.explain)
    },
    explanationReceived(explanation) {
      this.explanation = explanation;
      this.currentExplanation = true;
    }
  },
  data() {
    return {
      currentPrediction: false,
      currentExplanation: false,
      explanation: null,
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Cute-dog-licking-lips.jpg/300px-Cute-dog-licking-lips.jpg'
    }
  },
  created() {
    document.title = "Visual Inspection – XAI Demonstrator"
  },
  mounted() {
    this.$refs.cropper.refresh()
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
