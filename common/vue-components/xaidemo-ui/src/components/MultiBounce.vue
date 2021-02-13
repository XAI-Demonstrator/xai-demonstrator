<template>
  <div class="multi-bounce">
    <div v-for="dot in parseInt(numberOfDots)" v-bind:key="dot"
         class="bouncing-dot"
         v-bind:class="dotClass"
         v-bind:style="{'animation-delay': (dot-1) * period + 's',
                        'animation-duration': duration}"></div>
  </div>
</template>

<script>
export default {
  name: "MultiBounce",
  data: function () {
    return {
      period: 0.4
    }
  },
  computed: {
    duration() {
      return this.numberOfDots * this.period + 's'
    }
  },
  props: {
    numberOfDots: {
      type: Number,
      default: 3
    },
    dotClass: {
      type: String,
      default: 'xd-primary'
    }
  }
}
</script>

<style scoped>
.multi-bounce {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  min-height: 1em;
  padding: 4px 0;
}

.bouncing-dot {
  border-radius: 100%;
  height: 10px;
  width: 10px;
  margin-left: 3px;
  margin-right: 3px;
  animation-name: bounce;
  animation-fill-mode: both;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in;
  box-shadow: 2px 2px 4px rgba(180, 180, 180, 0.5);
}

@keyframes bounce {
  0%, 100% {
    transform: scale(0.0);
  }
  50% {
    transform: scale(1.0);
  }
}
</style>