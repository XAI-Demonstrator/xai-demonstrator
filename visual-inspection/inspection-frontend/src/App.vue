<template>
  <div id="app" class="xd-app">
    <GitHubRibbon url="https://github.com/xai-demonstrator/xai-demonstrator"/>
    <XAIStudioRibbon url="https://www.xai-studio.de"/>
    <UseCaseHeader
        v-bind:standalone="!Boolean(backendUrl)"
        v-bind:title="showConfiguration ? $t('titleConfiguration') : $t('title')"/>

    <main>
      <section>
        <div class="xd-section xd-light">
          <p>{{ showConfiguration ? $t('howToConfigure') : $t('howToInspect') }}</p>
        </div>
      </section>

      <div id="image-container" v-show="!showConfiguration">
        <Cropper ref="cropper" class="cropper"
                 :src="img" @change="imageChanged"
                 :min-width="20" :min-height="20"
                 :stencil-component="explanationStencil"
                 :debounce="false"
                 :resizeImage="{wheel: false, touch: false}"
                 :moveImage="{mouse: false, touch: false}"
                 :size-restrictions-algorithm="sizeRestrictions"
                 :stencil-props="{
                 'explanationMode': currentExplanation,
                 'explanationImg': explanationImg,
                 'aspectRatio': 1.0,
                 'movable': !waitingForExplanation,
                 'resizable': !waitingForExplanation,
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

      <section v-show="!showConfiguration">
        <div class="xd-section xd-light">
          <InspectImage ref="inspector"
                        v-bind:model_id="modelID"
                        v-bind:current-prediction="currentPrediction"
                        v-on:inspection-completed="inspectionCompleted"/>
          <ExplainInspection v-if="showExplainButton" ref="explainer"
                             v-bind:prediction-ready="currentPrediction"
                             v-on:explanation-requested="explanationRequested"
                             v-on:explanation-received="explanationReceived"/>
        </div>
      </section>

      <section v-if="showConfiguration">
        <ConfigureModel ref="configuration"/>
      </section>

      <section>
        <div class="xd-section xd-light">
          <button class="xd-button xd-secondary" @click="toggleConfiguration"
                  v-bind:disabled="!showConfiguration && !currentPrediction">
            {{ showConfiguration ? $t('switchToInspection') : $t('switchToConfiguration') }}
          </button>
        </div>
      </section>
    </main>

    <FloatingInfoButton class="info-button"
                        v-bind:info-url="infoUrl"
                        v-bind:info-text="infoText"
                        v-bind:link-label="$t('infoLinkLabel')"/>
  </div>
</template>

<script>
import {Cropper} from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css'
import InspectImage from "@/components/InspectImage";
import ExplainInspection from "@/components/ExplainInspection";
import ExplanationStencil from "@/components/ExplanationStencil";
import ConfigureModel from "@/components/ConfigureModel";

import {FloatingInfoButton, UseCaseHeader, XAIStudioRibbon, GitHubRibbon} from '@xai-demonstrator/xaidemo-ui';
import {debounce} from "debounce";
import {modelConfig} from '@/modelConfig.js'

/* https://forum.vuejs.org/t/vue-received-a-component-which-was-made-a-reactive-object/119004/2 */
const componentMap = {
  stencil: ExplanationStencil
}
export default {
  name: 'App',
  components: {
    Cropper,
    InspectImage,
    ExplainInspection,
    ConfigureModel,
    UseCaseHeader,
    FloatingInfoButton,
    XAIStudioRibbon,
    GitHubRibbon
  },
  methods: {
    async toggleConfiguration() {
      this.showConfiguration = !this.showConfiguration
      if (!this.showConfiguration && !this.currentPrediction) {
        await this.requestInspection(this.$refs.cropper.getResult().canvas)
      }
    },
    async imageChanged({canvas}) {
      if (!this.waitingForExplanation) {
        this.currentPrediction = false;
        this.currentExplanation = false;
        await this.debouncedRequestInspection(canvas)
      }
    },
    async requestInspection(canvas) {
      canvas.toBlob(await this.$refs.inspector.predict)
    },
    inspectionCompleted() {
      this.currentPrediction = true;
    },
    async explanationRequested() {
      this.currentExplanation = false;
      this.waitingForExplanation = true;
      this.$refs.cropper.getResult().canvas.toBlob(await this.$refs.explainer.explain)
    },
    explanationReceived(explanationImg) {
      this.explanationImg = explanationImg;
      this.currentExplanation = true;
      this.waitingForExplanation = false;
    },
    sizeRestrictions({minWidth, minHeight, maxWidth, maxHeight, imageSize}) {
      return {
        minWidth: Math.max(this.minExplanationImgSize.width, (minWidth / 100) * imageSize.width),
        minHeight: Math.max(this.minExplanationImgSize.height, (minHeight / 100) * imageSize.height),
        maxWidth: maxWidth,
        maxHeight: maxHeight,
      };
    }
  },
  data() {
    return {
      showConfiguration: false,
      currentPrediction: false,
      currentExplanation: false,
      waitingForExplanation: false,
      explanationImg: null,
      minExplanationImgSize: {
        width: 100,
        height: 100
      },
      infoUrl: "https://www.erklaerbare-ki.de/xai-demonstrator/",
      infoText: [{
        headline: this.$t('info1headline'),
        paragraphs: [this.$t('info1paragraph1'), this.$t('info1paragraph2'), this.$t('info1paragraph3')]
      }, {
        headline: this.$t('info2headline'),
        paragraphs: [this.$t('info2paragraph1'), this.$t('info2paragraph2'), this.$t('info2paragraph3')]
      }],
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      modelConfig: modelConfig,
      img: require('./assets/' + process.env.VUE_APP_IMAGE_FILE),
      showExplainButton: JSON.parse(process.env.VUE_APP_SHOW_EXPLAIN_BUTTON)
    }
  },
  computed: {
    explanationStencil() {
      return componentMap['stencil']
    },
    modelID() {
      return modelConfig.getModelId()
    }
  },
  watch: {
    modelID(newValue) {
      console.log(newValue)
      this.currentPrediction = false
      this.currentExplanation = false
    }
  },
  created() {
    document.title = this.$t('title') + " – " + this.$t('xaidemonstrator');
    this.debouncedRequestInspection = debounce(this.requestInspection, 500)
  }
  ,
  mounted() {
    this.$refs.cropper.refresh()
  }
}
</script>

<i18n>
{
  "de": {
    "title": "Gegenstände erkennen",
    "titleConfiguration": "KI trainieren",
    "howToInspect": "Wähle einen Bildausschnitt und die KI bestimmt den Gegenstand.",
    "howToConfigure": "Wähle die Daten für das Training der KI aus.",
    "switchToConfiguration": "Trainiere die KI",
    "switchToInspection": "KI trainieren und zurückkehren",
    "info1headline": "Gegenstände erkennen",
    "info1paragraph1": "Du interagierst mit einer KI, die einen Gegenstand in einem Bildausschnitt erkennen kann. Aber eine KI ist nie perfekt!",
    "info1paragraph2": "Durch die Wahl verschiedener Bildausschnitte entdeckst du, für welche Bereiche die KI zuverlässig ist, aber insbesondere auch, wo sie an ihre Grenzen stößt.",
    "info1paragraph3": "Die automatisch erzeugten Erklärungen helfen dir, zu verstehen, wie die KI vorgeht und warum sie manchmal falsche Schlüsse zieht.",
    "info2headline": "Was steckt dahinter?",
    "info2paragraph1": "Die KI ist ein tiefes neuronales Netz, das 1001 verschiedene Objekte erkennen kann.",
    "info2paragraph2": "Die Erklärungen werden mit der XAI-Methode <em><abbr>LIME</abbr></em> (<strong>L</strong>ocal <strong>I</strong>nterpretable <strong>M</strong>odel-Agnostic <strong>E</strong>xplanations) generiert. Die Erklärung entspricht einer graphischen Hervorhebung von Bildbereichen, die für die Entscheidung der KI besonders relevant sind.",
    "info2paragraph3": "<small>Modell: Neuronales Netz auf Basis von <a href='https://www.tensorflow.org/api_docs/python/tf/keras/applications/mobilenet_v2'>MobileNetV2 for Keras</a>, Erklärungen: <a href='https://github.com/marcotcr/lime'>LIME</a><br />Bild: Melinda Pack (Unsplash), <a href='https://creativecommons.org/publicdomain/zero/1.0/deed.en'>CC0</a> 1.0, via <a href='https://commons.wikimedia.org/wiki/File:Camera_keys_notebook_coffee_(Unsplash).jpg'>Wikimedia Commons</a></small>",
    "infoLinkLabel": "Interesse geweckt? Hier gibt’s mehr Infos!"
  },
  "en": {
    "title": "Detect Objects",
    "titleConfiguration": "Train AI",
    "howToInspect": "Select a part of the image and the AI will identify the object.",
    "howToConfigure": "Select data to train the AI.",
    "switchToConfiguration": "Train the AI",
    "switchToInspection": "Train the AI and return",
    "info1headline": "Detect objects",
    "info1paragraph1": "You are interacting with an AI that can detect objects in images. But an AI is never perfect!",
    "info1paragraph2": "By selecting different parts of the image, you can discover for which of these parts the AI is reliable and, perhaps more importantly, for which it is not.",
    "info1paragraph3": "The automatically generated explanations help you understand how the AI detects objects and why it sometimes fails to do so.",
    "info2headline": "What's going on behind the curtain?",
    "info2paragraph1": "The AI is a deep neural network that can detect 1,001 different objects.",
    "info2paragraph2": "The explanations are generated by the XAI method <em><abbr>LIME</abbr></em> (<strong>L</strong>ocal <strong>I</strong>nterpretable <strong>M</strong>odel-Agnostic <strong>E</strong>xplanations). An explanation highlights the areas of the image that were particularly relevant for the AI's decision.",
    "info2paragraph3": "<small>Model: neural network based on <a href='https://www.tensorflow.org/api_docs/python/tf/keras/applications/mobilenet_v2'>MobileNetV2 for Keras</a>, Explanations: <a href='https://github.com/marcotcr/lime'>LIME</a><br />Image: Melinda Pack (Unsplash), <a href='https://creativecommons.org/publicdomain/zero/1.0/deed.en'>CC0</a> 1.0, via <a href='https://commons.wikimedia.org/wiki/File:Camera_keys_notebook_coffee_(Unsplash).jpg'>Wikimedia Commons</a></small>",
    "infoLinkLabel": "Want to learn more? (in German)"
  }
}
</i18n>

<style>
#app {
  display: flex;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
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
    padding: 0;
    margin-bottom: 12px;
  }
  .cropper {
    max-width: 100vw;
  }
  .cropper * {
    border-radius: 0;
  }

  main section {
    margin-bottom: 12px;
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
    margin-bottom: 8px;
  }
  #image-container {
    margin-bottom: 8px;
    width: 100%;
    max-width: 450px;
  }
  .cropper {
    max-width: calc(450px - 16px);
  }
}
</style>