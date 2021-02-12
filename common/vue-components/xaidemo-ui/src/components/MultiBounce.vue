<template>
  <div class="multi-bounce">
    <div v-for="dot in parseInt(dots)" v-bind:key="dot"
         class="bouncing-dot"
         v-bind:class="dotClass"
         v-bind:style="{'animation-delay': dot * period + 's',
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
      return this.dots * this.period + 's'
    }
  },
  props: {
    dots: {
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
  min-height: 16px;
}

.bouncing-dot {
  border-radius: 100%;
  height: 12px;
  width: 12px;
  margin-left: 3px;
  margin-right: 3px;
  animation-name: bounce;
  animation-fill-mode: both;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in;
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