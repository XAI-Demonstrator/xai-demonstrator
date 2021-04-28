<template>
  <div class="inspector">
    <MultiBounce v-if="prediction.length===0"
                 v-bind:numberOfDots="3"/>  
       <div v-if="prediction.length > 1">
            <p v-show="prediction && currentPrediction">„Das ist {{ prediction[0] }} Genauigkeit“</p>
            <p v-show="prediction && currentPrediction">„Das ist {{ prediction[1] }} Genauigkeit“</p>
            <p v-show="prediction && currentPrediction">„Das ist {{ prediction[2] }} Genauigkeit“</p>
      </div>
      <div v-else>
            <p v-show="prediction && currentPrediction">„Das ist {{ prediction[0] }} Genauigkeit“</p>
      </div>        
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
      this.prediction = [];
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
          if (response.data.length > 1)
          {
         this.prediction[0] = response.data[0].class_label.concat(' mit ', parseFloat(100*response.data[0].class_percentage).toFixed(2)+"%")
         this.prediction[1] = response.data[1].class_label.concat(' mit ', parseFloat(100*response.data[1].class_percentage).toFixed(2)+"%")
         this.prediction[2] = response.data[2].class_label.concat(' mit ', parseFloat(100*response.data[2].class_percentage).toFixed(2)+"%")
         this.topPredictions[0] = [response.data[0].class_label, parseFloat(100*response.data[0].class_percentage).toFixed(2)];
         this.topPredictions[1] = [response.data[1].class_label, parseFloat(100*response.data[1].class_percentage).toFixed(2)];
         this.topPredictions[2] = [response.data[2].class_label, parseFloat(100*response.data[2].class_percentage).toFixed(2)];

          }
          else
          {
         this.prediction[0] = response.data[0].class_label.concat(' mit ', parseFloat(100*response.data[0].class_percentage).toFixed(2)+"%")
         this.topPredictions[0] = [response.data[0].class_label, parseFloat(100*response.data[0].class_percentage).toFixed(2)];
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
      prediction: null,
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      cancelTokens: []
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
  min-height: 90px;
}
</style>
