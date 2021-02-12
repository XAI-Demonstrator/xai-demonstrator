<template>
  <transition name="indicator">
    <div class="wrapper" v-if="visible">
      <div class="spinner" v-bind:class="backgroundClass">
        <div class="circle circle-smooth" v-bind:class="circleClass"></div>
        <div class="circle circle-fast" v-bind:class="circleClass"></div>
        <div class="circle circle-trace" v-bind:class="circleClass"></div>
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
  transform: translate(-50%, -50%);
  bottom: auto;
  right: auto;
  border-radius: 5px;
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
  border: 8px solid;
  border-radius: 100%;
  position: absolute;

  width: 80%;
  height: 80%;
}

.circle-smooth {
  border-bottom-color: transparent;
  border-right-color: transparent;
  animation: spinner-rotate-smooth 1.2s infinite linear;
}

.circle-fast {
  border-bottom-color: transparent;
  border-left-color: transparent;
  animation: spinner-rotate 1.2s infinite linear;
}

.circle-trace {
  opacity: 0.3;
}

.indicator-enter,
.indicator-leave-active {
  opacity: 0;
}

@keyframes spinner-rotate-smooth {
  0% {
    transform: rotate(0deg);
  }

  50% {
    transform: rotate(180deg);
  }

  100% {
    transform: rotate(360deg);
  }
}

@keyframes spinner-rotate {
  0% {
    transform: rotate(0deg);
  }

  30% {
    transform: rotate(180deg);
  }

  80% {
    transform: rotate(270deg);
  }

  100% {
    transform: rotate(360deg);
  }
}
</style>