<template>
  <transition name="indicator">
    <div class="wrapper" v-if="visible">
      <div class="spinner" v-bind:class="backgroundClass">
        <div class="circle circle-trace" v-bind:class="circleClass"></div>
        <div class="circle circle-fast" v-bind:class="circleClass"></div>
        <div class="circle circle-slow" v-bind:class="circleClass"></div>
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
  box-shadow: 2px 4px 8px rgba(120, 120, 120, 0.5);
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
  opacity: 0.6;
  width: 48px;
  height: 48px;
}

.circle-slow {
  border-bottom-color: transparent;
  border-right-color: transparent;
  animation: spinner-rotate-smooth 1.4s infinite linear;
}

.circle-fast {
  border-bottom-color: transparent;
  border-right-color: transparent;
  animation: spinner-rotate-smooth 0.7s infinite linear;
}

.circle-trace {
  opacity: 0.15;
}

.indicator-enter-active,
.indicator-leave-active {
  transition: opacity .4s ease;
}

.indicator-enter-from,
.indicator-leave-to {
  opacity: 0;
}

.indicator-enter-to,
.indicator-leave-from {
  opacity: 1;
}

@keyframes spinner-rotate-smooth {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}
</style>