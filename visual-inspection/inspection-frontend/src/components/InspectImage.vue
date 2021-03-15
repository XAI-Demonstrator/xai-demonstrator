<template>
  <div class="inspector">
    <MultiBounce v-if="!prediction"
                 v-bind:numberOfDots="3"/>
    <p v-show="prediction && currentPrediction">„Das ist {{ prediction }}“</p>
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
      this.prediction = null;

      for (let i = this.cancelArray.length - 1; i >= 0; i--) {
        const source = this.cancelArray[i];
        source.cancel();
        this.cancelArray.splice(i, 1);
      }

      const CancelToken = axios.CancelToken;
      const source = CancelToken.source();
      this.cancelArray.push(source);

      const form = new FormData();
      form.append('file', blob);

      await axios.post(this.backendUrl + '/predict', form,{
        cancelToken: source.token
      })
          .then(response => {
            this.prediction = response.data.class_label
            this.$emit('inspection-completed')
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
      cancelArray: []
    }
  }
}
</script>

<style scoped>
.inspector {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  min-height: 30px;
}
</style>
