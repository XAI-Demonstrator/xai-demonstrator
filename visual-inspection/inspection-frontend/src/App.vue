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
    <p>Wähle einen Bildausschnitt und frage die KI nach dem Wetter:</p>
    <div id="image-container">
      <Cropper ref="cropper" :src="img" @change="imageChanged"
               :min-width="30" :min-height="20"
               :stencil-component="ExplanationStencil"
               :stencil-props="{
                 'explanationMode': currentExplanation,
                 'explanationImg': explanationImg,
                 'aspectRatio': 1.0,
                 'handlers': {
                    eastNorth: true,
                    north: false,
                    westNorth: true,
                    west: false,
                    westSouth: true,
                    south: false,
                    eastSouth: true,
                    east: false
                 }
               }"/>
    </div>
    <InspectImage ref="inspector"
                  :current-prediction="currentPrediction"
                  v-on:inspectionCompleted="inspectionCompleted"/>
    <ExplainInspection ref="explainer" v-show="currentPrediction"
                       v-on:explanationRequested="explanationRequested"
                       v-on:explanationReceived="explanationReceived"/>
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
  components: {Cropper, InspectImage, ExplainInspection},
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
    explanationReceived(explanationImg) {
      this.explanationImg = explanationImg;
      this.currentExplanation = true;
    }
  },
  data() {
    return {
      ExplanationStencil,
      currentPrediction: false,
      currentExplanation: false,
      explanationImg: null,
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/El_Guamache_Bay%2C_Margarita_island.jpg/300px-El_Guamache_Bay%2C_Margarita_island.jpg'
    }
  },
  created() {
    document.title = "Visual Inspection – XAI Demonstrator";
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
  max-height: 400px;
}

.navigation-header {
  background-color: #77A6F7 !important;
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
