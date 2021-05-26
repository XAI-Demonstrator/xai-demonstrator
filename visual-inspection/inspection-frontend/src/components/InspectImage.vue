<template>
  <div class="inspector">
    <MultiBounce v-if="topPredictions.length===0"
                 v-bind:numberOfDots="3"/>     
        <span class="prediction-result" v-if="currentPrediction && topPredictions[0][1] > MinAccuracy"> 
            Bestimmung:
            <br />
            <p>Die KI ist sich zu {{topPredictions[0][1]}}% sicher, dass es sich um {{topPredictions[0][0]}} handelt.</p>
            <div v-for="(item, index) in topPredictions" :key="index"> 
                <a v-show="index === 1">Alternativ könnte das auch </a>
                <a v-show="index > 0">{{item[0]}} ({{item[1]}}%)</a>
                <a v-show="index > 0 && index < topPredictions.length-1"> oder </a>
                <a v-show="index > 0 && index === topPredictions.length-1"> sein.</a>
            </div>
        </span>  
</div>
</template>

<script>
import axios from 'axios'
import {MultiBounce} from '@xai-demonstrator/xaidemo-ui'

export default {
  name: "InspectImage",
  components: {
    MultiBounce
  },
  props: {
    currentPrediction: {
      type: Boolean,
      value: false
    }
  },
  methods: {
    async predict(blob) {
      //this.prediction = [];
      this.topPredictions = [];

      while (this.cancelTokens.length > 0) {
        this.cancelTokens.pop().cancel()
      }

      const source = axios.CancelToken.source();
      this.cancelTokens.push(source);

      const form = new FormData();
      form.append('file', blob);

      await axios.post(this.backendUrl + '/predict', form, {
        cancelToken: source.token
      })
          .then(response => {
              var i;
              for (i = 0; i < response.data.length; i++) {
                 this.topPredictions[i] = [response.data[i].class_label, parseFloat(100*response.data[i].class_percentage).toFixed(0)];
          }

          this.$emit('inspection-completed');
          
          })
          .catch(error => {
            console.log(error)
          })
    }
  },
  data() {
    return {
      //prediction: [],
      topPredictions: [],
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      cancelTokens: [],
      MinAccuracy: 15
    }
  }
}
</script>

<style scoped>
.inspector {
  display: flex;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  min-height: 150px;
}
.prediction-result {
  flex-direction: column;
  font-style: normal;
  font-size: 16px;
  text-align: center;
  color: black;
  border: 2px solid gray;
  padding: 10px;
    }
  .center {
  color: black;
  text-align: center;
  border: 3px solid red;
}

</style>
