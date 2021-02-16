<template>
  <div id="app" class="xd-app">
    <UseCaseHeader
        v-bind:standalone="!Boolean(backendUrl)"
        v-bind:title="title"/>
    <main>
      <section>
        <div class="xd-section xd-light">
          <p>Wähle einen Bildausschnitt und frage die KI nach dem Wetter:</p>
        </div>
      </section>
      <div id="image-container">
        <Cropper ref="cropper" class="cropper" :src="img" @change="imageChanged"
                 :min-width="30" :min-height="20"
                 :stencil-component="ExplanationStencil"
                 :stencil-props="{
                 'explanationMode': currentExplanation,
                 'explanationImg': explanationImg,
                 'aspectRatio': 1.0,
                 'movable': !waitingForExplanation,
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

      <section>
        <div class="xd-section xd-light">
          <InspectImage ref="inspector"
                        v-bind:current-prediction="currentPrediction"
                        v-on:inspection-completed="inspectionCompleted"/>
          <ExplainInspection ref="explainer"
                             v-bind:prediction-ready="currentPrediction"
                             v-on:explanation-requested="explanationRequested"
                             v-on:explanation-received="explanationReceived"/>
        </div>
      </section>

    </main>
    <FloatingInfoButton class="info-button"
                        v-bind:info-url="infoUrl"
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
      this.waitingForExplanation = true;
      this.$refs.cropper.getResult().canvas.toBlob(this.$refs.explainer.explain)
    },
    explanationReceived(explanationImg) {
      this.explanationImg = explanationImg;
      this.currentExplanation = true;
      this.waitingForExplanation = false;
    }
  },
  data() {
    return {
      ExplanationStencil,
      currentPrediction: false,
      currentExplanation: false,
      waitingForExplanation: false,
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
#app {
  display: flex;
}

main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

main section {
  width: 100%;
  margin: 0;
  padding: 0 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

#image-container {
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cropper * {
  border-radius: 3px;
}

@media screen and (max-width: 450px) {
  #app {
    flex-direction: column;
    padding-left: 0;
    padding-right: 0;
  }

  #image-container {
    width: 100%;
    max-width: 100vw;
    padding: 12px 0;
  }

  .cropper {
    max-width: 100vw;
  }

  .cropper * {
    border-radius: 0;
  }
}

@media screen and (min-width: 450px) and (max-height: 650px) {

  #app {
    flex-direction: column;
    padding-left: 0;
    padding-right: 0;
    overflow: auto;
    height: 100vh;
    width: 100vw;
  }

  main {
    flex: 1;
    max-height: calc(100vh - 54px);

    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  main section {
    width: 40%;
    order: 2;
    margin-bottom: 12px;
  }

  main section:last-of-type {
    margin-bottom: 0;
  }

  #image-container {
    max-height: calc(100vh - 54px);
    width: 60%;

    align-self: flex-start;
    order: 1;

    justify-content: center;
    align-items: flex-start;
  }

  .cropper {
    max-height: calc(100vh - 54px);
  }

}

@media screen and (min-width: 450px) and (min-height: 650px) {

  #app {
    flex-direction: column;
  }

  main {
    flex-grow: 1;
  }

  main section {
    padding: 0;
  }

  #image-container {
    margin-top: 8px;
    margin-bottom: 8px;
    width: 100%;
    max-width: 450px;
  }

  .cropper {
    max-width: calc(450px - 16px);
  }

}
</style>
