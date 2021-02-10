<template>
  <div id="app">
    <UseCaseHeader
        v-bind:standalone="!Boolean(backendUrl)"
        v-bind:title="title"/>
    <main>
      <section>
        <p>Wähle einen Bildausschnitt und frage die KI nach dem Wetter:</p>
      </section>
      <div id="image-container">
        <Cropper ref="cropper" class="cropper" :src="img" @change="imageChanged"
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
      <ExplainInspection ref="explainer" v-bind:prediction-ready="currentPrediction"
                         v-on:explanationRequested="explanationRequested"
                         v-on:explanationReceived="explanationReceived"/>
    </main>
    <FloatingInfoButton v-bind:info-url="infoUrl"
                        v-bind:info-text="infoText"
                        v-bind:link-label="infoLinkLabel"/>
  </div>
</template>

<script>
import {Cropper} from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css'
import InspectImage from "@/components/InspectImage";
import ExplainInspection from "@/components/ExplainInspection";
import ExplanationStencil from "@/components/ExplanationStencil";
import {FloatingInfoButton, UseCaseHeader} from '@xai-demonstrator/xaidemo-ui';

export default {
  name: 'App',
  components: {
    Cropper,
    InspectImage,
    ExplainInspection,
    UseCaseHeader,
    FloatingInfoButton
  },
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
      title: "Visual Inspection",
      infoUrl: "/",
      infoLinkLabel: "Erfahre viel mehr!",
      infoText: [
        {
          headline: "Visual Inspection",
          paragraphs: [
            "Sehr oft muss man das Wetter vorhersagen.",
            "Eine KI ist darin manchmal sehr gut, manchmal sehr schlecht."
          ]
        }
      ],
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      img: 'https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/El_Guamache_Bay%2C_Margarita_island.jpg/800px-El_Guamache_Bay%2C_Margarita_island.jpg'
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
* {
  box-sizing: border-box;
}

body {
  padding: 0;
  margin: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

main section {
  width: 100%;
  min-height: 40px;
  padding-left: 5px;
  padding-right: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
}

#image-container {
  width: 100%;
  background-color: #000000;
  display: flex;
  align-items: center;
}

.cropper {
  flex: 1;
  display: block;
}

@media screen and (max-width: 450px) {
  #app {
    padding: 60px 0 0;
    overflow: scroll;
    flex-direction: column;
  }
}

@media screen and (min-width: 450px) and (max-height: 650px) {
  #app {
    padding: 60px 0 0;
    max-width: 450px;
    overflow: scroll;
    flex-direction: column;
    flex-wrap: wrap;
  }

  #image-container {
    max-width: 100%;
    height: 50vh;
  }
}

@media screen and (min-width: 450px) and (min-height: 650px) {

  body {
    background-color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100vw;
    height: 100vh;
  }

  #app {
    max-width: 450px;
    border: 1px solid #ddd;
    box-shadow: 2px 2px 5px 2px #eee;
    padding: 8px;
    height: auto;
    min-height: 640px;
    flex-direction: column;
    overflow: auto;
  }

  main {
    flex: 1;
  }
}
</style>
