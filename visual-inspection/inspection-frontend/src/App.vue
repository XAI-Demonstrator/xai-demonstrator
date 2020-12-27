<template>
  <div id="app">
    <mt-header fixed title="Visual Inspection" class="navigation-header">
      <a href="/" slot="left">
        <mt-button icon="back"></mt-button>
      </a>
      <a href="./" slot="right">
        <mt-button><span style="font-size: 16px; font-weight:bold;">↻</span></mt-button>
      </a>
    </mt-header>
    <div id="image-container">
      <SelectImage v-if="selectionMode" v-on:imageChanged="imageChanged"/>
      <ExamineInspection v-if="!selectionMode"/>
    </div>
    <InspectImage v-on:buttonClicked="toggleMode"/>
  </div>
</template>

<script>

import SelectImage from "@/components/SelectImage";
import InspectImage from "@/components/InspectImage";
import ExamineInspection from "@/components/ExamineInspection";

export default {
  name: 'App',
  components: {ExamineInspection, SelectImage, InspectImage},
  methods: {
    imageChanged(index) {
      console.log(index)
    },
    toggleMode() {
      this.selectionMode = !this.selectionMode
    }
  },
  data() {
    return {
      selectionMode: true
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 50px;
}

#image-container {
  height: 70vh;
  max-height: 400px;
  margin-bottom: 10px;
}

.navigation-header {
  background-color: #77A6F7 !important;
}

.mint-indicator-wrapper {
  background-color: #00887A !important;
}

.mint-spinner-snake {
  border-top-color: #D3E3FC !important;
  border-bottom-color: #D3E3FC !important;
  border-left-color: #D3E3FC !important;
}

@media screen and (min-width: 500px) {
  body {
    background-color: #FFFFFF;
  }

  #app {
    margin: 40px auto auto;
    max-width: 425px;
    border: 1px solid #D3E3FC;
    padding: 5px;
  }

  .navigation-header {
    margin: auto;
    max-width: 437px;
  }
}
</style>
