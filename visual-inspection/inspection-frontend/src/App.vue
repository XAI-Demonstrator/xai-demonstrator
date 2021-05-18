<template>
  <div id="app" class="xd-app">
    <UseCaseHeader
        v-bind:standalone="!Boolean(backendUrl)"
        v-bind:title="useCaseTitle"/>
    <main>
      <section class="app_heading">
        <div v-if="!expButtonClicked">
          <p>Wähle einen Bildausschnitt und die KI bestimmt den Gegenstand.</p>
        </div>
        <div v-else>
            <p>Ausgegraute Bereiche sind für die Entscheidung der KI weniger relevant gewesen.</p>
            <p>Wähle einen neuen Bildausschnitt und die KI bestimmt weitere Gegenstände.</p>
        </div>
      </section>
      <div id="image-container">
        <Cropper ref="cropper" class="cropper" :src="img" @change="imageChanged"
                 :min-width="20" :min-height="20"
                 :stencil-component="ExplanationStencil"
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
          <InspectImage ref="inspector"
                        v-bind:current-prediction="currentPrediction"
                        v-on:inspection-completed="inspectionCompleted"/>
          <ExplainInspection ref="explainer"
                             v-bind:prediction-ready="currentPrediction"
                             v-bind:Cls_Acc_List = "cls_accuracy_List"
                             v-bind:isButtonClicked = "expButtonClicked"
                             v-bind:Cls_Min_Acc = "cls_MinAccuracy"
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
import {debounce} from "debounce";

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
    async imageChanged({canvas}) {
      if (!this.waitingForExplanation) {
        this.currentPrediction = false;
        this.currentExplanation = false;
        this.expButtonClicked = false;
        await this.debouncedRequestInspection(canvas)
      }
    },
    async requestInspection(canvas) {
      canvas.toBlob(await this.$refs.inspector.predict)
 
    },
    inspectionCompleted() {
      this.currentPrediction = true;
      this.cls_accuracy_List =this.$refs.inspector.topPredictions;
      this.cls_MinAccuracy = this.$refs.inspector.MinAccuracy;
    },
    async explanationRequested(index_of_label_to_explain, positive_only_parameter) {
         
      this.currentExplanation = false;
      this.waitingForExplanation = true;
       
      this.$refs.cropper.getResult().canvas.toBlob(await this.$refs.explainer.explain.bind(null, index_of_label_to_explain, positive_only_parameter))
    },
    explanationReceived(explanationImg) {
      this.explanationImg = explanationImg;
      this.currentExplanation = true;
      this.waitingForExplanation = false;
      this.expButtonClicked = true;
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
      ExplanationStencil,
      currentPrediction: false,
      currentExplanation: false,
      waitingForExplanation: false,
      explanationImg: null,
      minExplanationImgSize: {
        width: 100,
        height: 100
      },
      useCaseTitle: "Gegenstände erkennen",
      infoUrl: "https://xai-demonstrator.github.io/#use-case-ii",
      infoLinkLabel: "Interesse geweckt? Hier gibt’s mehr Infos!",
      infoText: [
        {
          headline: "Gegenstände erkennen",
          paragraphs: [
            "Du interagierst mit einer KI, die einen Gegenstand in einem Bildausschnitt erkennen kann. Aber eine KI ist nie perfekt!",
            "Durch die Wahl verschiedener Bildausschnitte entdeckst du, für welche Bereiche die KI zuverlässig ist, aber insbesondere auch, wo sie an ihre Grenzen stößt.",
            "Die automatisch erzeugten Erklärungen helfen dir, zu verstehen, wie die KI vorgeht und warum sie manchmal falsche Schlüsse zieht."

          ]
        }, {
          headline: "Was steckt dahinter?",
          paragraphs: [
            "Die KI ist ein tiefes neuronales Netz, das 1000 verschiedene Objekte erkennen kann.",
            "Die Erklärungen werden mit der XAI-Methode <em><abbr>LIME</abbr></em> (<strong>L</strong>ocal <strong>I</strong>nterpretable <strong>M</strong>odel-Agnostic <strong>E</strong>xplanations) generiert. Die Erklärung entspricht einer graphischen Hervorhebung von Bildbereichen, die für die Entscheidung der KI besonders relevant sind.",
            "<small>Modell: <a href='https://www.tensorflow.org/api_docs/python/tf/keras/applications/mobilenet_v2'>MobileNetV2 for Keras</a>, Erklärungen: <a href='https://github.com/marcotcr/lime'>LIME</a><br />Bild: Melinda Pack (Unsplash), <a href='https://creativecommons.org/publicdomain/zero/1.0/deed.en'>CC0</a> 1.0, via <a href='https://commons.wikimedia.org/wiki/File:Camera_keys_notebook_coffee_(Unsplash).jpg'>Wikimedia Commons</a></small>"
          ]
        }],
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      img: require('./assets/table.jpg')
    }
  },
  created() {
    document.title = this.useCaseTitle + " – XAI Demonstrator";
    this.debouncedRequestInspection = debounce(this.requestInspection, 500)
  }
  ,
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
.app_heading { 
  display: flex;
  align-items: center;
  width: 100%;
  min-height: 90px;
  text-align: justify;
  text-justify: inter-word;
}

  .cropper {
    max-width: calc(450px - 16px);
  }

}
</style>
