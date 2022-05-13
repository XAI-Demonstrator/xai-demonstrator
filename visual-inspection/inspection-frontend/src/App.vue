<template>
  <div id="app" class="xd-app">
    <GitHubRibbon url="https://github.com/xai-demonstrator/xai-demonstrator"/>
    <XAIStudioRibbon url="https://www.xai-studio.de"/>
    <UseCaseHeader
        v-if="!showConfiguration"
        v-bind:standalone="!Boolean(backendUrl)"
        v-bind:title="$t('titleInspection')"/>
    <UseCaseHeader
        v-else
        v-bind:standalone="!Boolean(backendUrl)"
        v-bind:title="$t('titleConfiguration')"/>

    <main>
      <section>
        <div class="xd-section xd-light">
          <p v-if="!showConfiguration">{{ $t('howToInspect') }}</p>
          <p v-else>{{ $t('howToConfigurate') }}</p>
        </div>
      </section>
      <div v-show = "!showConfiguration" id="image-container">
        <Cropper ref="cropper" class="cropper" :src="img" @change="imageChanged"
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

      <section>
        <div class="xd-section xd-light">
          <InspectImage v-if="!showConfiguration" ref="inspector"
                        v-bind:model_id="modelID"
                        v-bind:current-prediction="currentPrediction"
                        v-on:inspection-completed="inspectionCompleted"/>
          <ExplainInspection ref="explainer"
                             v-bind:prediction-ready="currentPrediction"
                             v-on:explanation-requested="explanationRequested"
                             v-on:explanation-received="explanationReceived"/>
          <ConfigureModel ref="configurator"/>
        </div>
      </section>

      <section v-show="showConfiguration">
        <div class="configurator-menu">
          <div id="smartphone_config" class="configurators">
            <KISettings v-bind:amounts= "['0', '15', '200']"
                        v-bind:header="'Kategorie A'"
                        v-bind:labels="['Handy', 'Tasse']"
                        v-bind:pic_filename="'25_Handys.jpg'"
                        v-bind:store_key="'smartphone'"
                        ref="smartphone"/>
            
          </div>
          <div id="pencil_config" class="configurators">
            <KISettings v-bind:amounts="['15', '200']"
                        v-bind:header="'Kategorie B'"
                        v-bind:labels="['Stift', 'Tasse']"
                        v-bind:pic_filename="'25_Stifte.jpg'"
                        v-bind:store_key="'pencil'"
                        ref="pencil"/>
          
          </div>
          <div id="cup_config" class="configurators">
            <KISettings  v-bind:amounts= "['15', '200']"
                         v-bind:header="'Kategorie C'"
                         v-bind:labels="['Tasse']"
                         v-bind:pic_filename="'25_Tassen.jpg'"
                         v-bind:store_key="'cup'"
                         ref="cup"/>
         
          </div>
        </div>
      </section>

    <GoToConfiguration v-show= "!showConfiguration" ref="explainer"
                            v-on:click="changeP()" />

    <GoToInspection v-show="showConfiguration" ref="explainer"
                             v-on:click="changeP()"/>

    <p>Smartphone: {{this.store.smartphone.amount}} {{this.store.smartphone.label}}</p>
    <p>Pencil: {{this.store.pencil.amount}} {{this.store.pencil.label}}</p>
    <p>Cup: {{this.store.cup.amount}} {{this.store.cup.label}}</p>
    <p>{{modelID}}</p>
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
import KISettings from "./components/KISettings";
import GoToConfiguration from "./components/GoToConfiguration";
import GoToInspection from "./components/GoToInspection";
import {FloatingInfoButton, UseCaseHeader, XAIStudioRibbon, GitHubRibbon} from '@xai-demonstrator/xaidemo-ui';
import {debounce} from "debounce";
import { store } from './store.js'

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
    UseCaseHeader,
    FloatingInfoButton,
    GoToConfiguration,
    GoToInspection,
    KISettings,
    XAIStudioRibbon,
    GitHubRibbon
  },
  methods: {
     async changeP() {
      this.showConfiguration = !this.showConfiguration
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
      model_id: "TestId",
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
      img: require('./assets/table.jpg'),
      store
    }
  },
  computed: {
    explanationStencil() {
      return componentMap['stencil']
    },
    modelID() {
      var id = 'model_'
      id += this.store.smartphone.amount
      if (this.store.smartphone.label==='Tasse') {
        id += 'T'
      }
      id += '_' + this.store.pencil.amount
      if (this.store.pencil.label==='Tasse') {
        id += 'T'
      }
      id += '_' + this.store.cup.amount
      return id
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
    "titleInspection": "Gegenstände erkennen",
    "titleConfiguration": "KI trainieren",
    "howToInspect": "Wähle einen Bildausschnitt und die KI bestimmt den Gegenstand.",
    "howToConfigurate": "Wähle die Daten für das Training der KI aus.",
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
    "titleInspection": "Detect Objects",
    "titleConfiguration": "Train AI",
    "howToInspect": "Select a part of the image and the AI will identify the object.",
    "howToConfigurate": "Select data to train the AI.",
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

.configurator-menu {
  display: flex;
}

.configurators {
  margin: 5px;
  border-radius: 25px;
  width: 140px;
  height: 400px;
  text-align: left;
}

.category_headline {
  text-align: center;
}

.config_picture {
  width: 135px;
  float: left;
  margin-top: 6px;
  margin-bottom: 6px;
}

#smartphone_config {
  background-color: #E2E6EC;
  box-shadow: #E2E6EC 2px 2px;
}

#pencil_config {
  background-color: #F1DEDB;
  box-shadow: #F1DEDB 2px 2px;
}

#cup_config {
  background-color: #EFFBF8;
  box-shadow: #EFFBF8 2px 2px;
}

/*The following Code is for getting Radio-Buttons with a square design
  instead of the old-school Radio-Buttons. It is based on the following StackOverflow-Thread;
  https://stackoverflow.com/questions/24516958/styling-radio-buttons-into-a-square*/
input {
  display: none;
}

label {
  display: inline-block;
  padding: 5px 10px;
  cursor: pointer;
}

label span {
  position: relative;
  line-height: 22px;
}

label span:before,
label span:after {
  content: '';
}


label span:before {
  border: 1px solid #222021;
  width: 20px;
  height: 20px;
  margin-right: 10px;
  display: inline-block;
  vertical-align: top;
}

label span:after {
  background: #222021;
  width: 14px;
  height: 14px;
  position: absolute;
  top: 2px;
  left: 4px;
  transition: 300ms;
  opacity: 0;
}

label input:checked+span:after {
  opacity: 1;
}
/*
body {
  background: #fbfbfb;
  font-family: Arial;
  font-weight: bold;
  color: rgba(0, 0, 0, 0.7);
}
*/
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