<template>
  <div>
    <div class="explanation-request">
            <MultiBounce v-if="waitingForExplanation"
                   v-bind:numberOfDots="3"/>
    <div v-for="(item, index) in Cls_Acc_List" :key="index"> 
        <span v-if="item[1] > MinAccuracy">
            <button class="xd-button xd-primary"
                  v-show="!waitingForExplanation && predictionReady"
                  v-bind:disabled="!predictionReady"
                  v-on:click="buttonClicked">
            Warum ist das {{item[0]}} mit GK {{item[1]}}%?
            </button>
         </span>
         <span v-else>
            <button class="xd-button xd-primary"
                  v-show="!waitingForExplanation  && predictionReady"
                  v-bind:disabled="true"
                  v-on:click="buttonClicked">
             „Gk {{item[1]}}%, bitte passen Sie den Ausschnitt an!“
            </button>
          </span>
     </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {MultiBounce} from '@xai-demonstrator/xaidemo-ui'
import {unflatten} from 'flat';

export default {
  name: "ExplainInspection",
  components: {
    MultiBounce
  },
  props: {
    predictionReady: {
      type: Boolean,
      default: false
    },
    Cls_Acc_List: {
      type: Object,
      default: undefined
    }
      
  },
  methods: {
    buttonClicked() {
      this.$emit('explanation-requested')
    },
    async explain(blob) {
      this.waitingForExplanation = true;

      const form = new FormData();
      form.append('file', blob);

      const rawParams = Object.fromEntries(new URLSearchParams(window.location.search.substring(1)))
      const allParams = unflatten(rawParams)

      const method = allParams['method'];
      if (method) {
        form.append('method', method);
      }

      const settings = Object
          .keys(allParams)
          .filter((key) => {
            return key !== 'method'
          })
          .reduce((obj, key) => {
            obj[key] = allParams[key];
            return obj;
          }, {})
      if (settings && Object.keys(settings).length !== 0) {
        form.append('settings', JSON.stringify(settings));
      }

      await axios.post(this.backendUrl + '/explain', form)
          .then(response => {
            this.$emit('explanation-received', response.data.image)
            this.waitingForExplanation = false;
          })
          .catch(error => {
            console.log(error)
            this.waitingForExplanation = false;
          })
    }
  },
  data() {
    return {
      MinAccuracy: 15.0,
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
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  min-height: 180px;
}


</style>
