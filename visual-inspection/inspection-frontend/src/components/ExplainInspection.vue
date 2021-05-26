<template>
    <div>
        <br />
        <div class="explanation-request">
                <MultiBounce v-if="waitingForExplanation"
                       v-bind:numberOfDots="3"/>
        <span class = "center_block_gray" v-show="!waitingForExplanation && predictionReady" v-if="Cls_Acc_List[0][1] > Cls_Min_Acc">
            Erklärung:
            <br />
            <div v-for="(item, index) in Cls_Acc_List" :key="index"> 
                 <span v-if="index===0"> 
                    <button class="xd-button xd-primary"
                          ref="'B'+index"
                          v-show="!waitingForExplanation && predictionReady"
                          v-bind:disabled="!predictionReady"
                          v-on:click="buttonClicked(index, positive_only, $event)">
                    Warum ist das {{item[0]}}?
                    </button>
                  </span>
                 <span v-else> 
                    <button class="xd-button xd-primary"
                          ref="'B'+index"
                          v-show="!waitingForExplanation && predictionReady"
                          v-bind:disabled="!predictionReady"
                          v-on:click="buttonClicked(index, positive_only, $event)">
                    Warum könnte das auch {{item[0]}} sein?
                    </button>
                  </span>
            </div>
        </span>
         <span v-else>
            <p class = "center_block_red" v-show="!waitingForExplanation && predictionReady">Die KI erkennt keinen Gegenstand mit ausreichender Genauigkeit. Bitte passen Sie den Bidlausschnitt an.</p>
        </span> 
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
    isButtonClicked: {
      type: Boolean,
      default: false
    }, 
    Cls_Acc_List: {
      type: Object,
      default: undefined
    },
    Cls_Min_Acc :{
      type: Number,
      default: 0
    }
      
  },
  methods: {
    buttonClicked(index_of_label_to_explain, positive_only_parameter, event) {
    this.$emit('explanation-requested', index_of_label_to_explain, positive_only_parameter);
    let elems = document.getElementsByTagName('button');
    for(let i = 0; i < elems.length; i++)
      {
         elems[i].disabled = false;
      }
    event.target.disabled = true;

    },
    async explain(index_of_label_to_explain,positive_only_parameter, blob) {
      //document.write(index_of_label_to_explain + 10);
      this.waitingForExplanation = true;

      const form = new FormData();
      form.append('file', blob);
      form.append('index_of_label_to_explain', index_of_label_to_explain);
      form.append('positive_only_parameter', positive_only_parameter);
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
      explanation: null,
      waitingForExplanation: false,
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      positive_only: 0
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
  min-height: 190px;
}
.center_block_red {
  color: black;
  text-align: center;
  border: 3px solid red;
  padding: 15px;
}
.center_block_gray {
  color: black;
  text-align: center;
  border: 2px solid gray;
  padding: 10px;
}
.xd-button{
      border: 2px solid #fff;
    }

</style>
