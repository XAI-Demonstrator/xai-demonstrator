<template>
  <div class="loadingBar">
    <MultiBounce  v-if="time < 100"
                 v-bind:numberOfDots="3"/>
    </div>
</template>

<script>
import {MultiBounce} from '@xai-demonstrator/xaidemo-ui'
export default {
  components: {
    MultiBounce
  },
  name: "loadingBar",
  data: () => {
    return {
      time: 0
    }
  },
  created() {
    var intval = setInterval(() => {
      if(this.time < 100)
        this.time += .95;
      else
        clearInterval(intval);
    }, 10);
  }
}
</script>