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
  margin-top: 60px;
}

#image-container {
  height: 200px;
  margin-bottom: 10px;
}

@media screen and (min-width: 500px) {
  #app {
    margin: 60px auto auto;
    max-width: 500px;
    border: 1px solid #2c3e50;
    padding: 5px;
  }

  .navigation-header {
    margin: auto;
    max-width: 512px;
  }
}
</style>
