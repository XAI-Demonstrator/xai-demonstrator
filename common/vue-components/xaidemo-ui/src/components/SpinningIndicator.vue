<template>
  <transition name="indicator">
    <div class="wrapper" v-if="visible">
      <div class="spinner" v-bind:class="backgroundClass">
        <div class="circle" v-bind:class="circleClass"></div>
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  name: "SpinningIndicator",
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    backgroundClass: {
      type: String,
      default: 'xd-secondary'
    },
    circleClass: {
      type: String,
      default: 'xd-border-light'
    }
  }
}
</script>

<style scoped>
.wrapper {
  position: fixed;
  top: 50%;
  left: 50%;
  bottom: auto;
  right: auto;
  border-radius: 5px;
  transform: translate(-50%, -50%);
  transition: opacity 0.3s ease-in;
  box-shadow: 4px 4px 4px #eee;
}

.spinner {
  width: 70px;
  height: 70px;
  border-radius: 5px;
  display: flex;
  justify-content: space-around;
  align-items: center;
}

.circle {
  width: 80%;
  height: 80%;
  border-radius: 50%;
  border: 8px solid;
  animation: spinner-rotate 1.0s infinite linear;
  border-bottom-color: transparent;
}

.indicator-enter,
.indicator-leave-active {
  opacity: 0;
}

@keyframes spinner-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>