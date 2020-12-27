<template>
  <div class="highlight-box">
    <span v-for="pair in explanation" :key="pair.word + Math.random()"
          v-bind:style="{'color': calcHSL(pair.score), 'font-weight': calcWeight(pair.score)}">{{ whitespace(pair.word) }}{{ pair.word }}</span>
  </div>
</template>

<script>
export default {
  name: "TextHighlight",
  props: [
    "explanation"
  ],
  data() {
    return {
      noSpaceInFrontOf: [",", ".", "!", ":", ";", "?"]
    }
  },
  methods: {
    calcHSL(score) {
      return 'hsl(' + this.calcHue(score) + ',' + this.calcSat(score) + '%,' + this.calcLightness(score) + '%)'
    },
    calcHue(score) {
      if (score <= 0) {
        return "14"
      } else {
        return "174"
      }
    },
    calcSat(score) {
      return Math.abs(score) * 100
    },
    calcLightness(score) {
      if (score <= 0) {
        return "87"
      } else {
        return "27"
      }
    },
    calcWeight(score) {
      return 100 + Math.min(1600 * Math.abs(score), 800)
    },
    whitespace(word) {
      if (this.noSpaceInFrontOf.includes(word)) {
        return ""
      } else {
        return " "
      }

    }
  }
}
</script>

<style scoped>
.highlight-box {
  background-color: #77A6F7;
  padding: 5px 10px;
}
</style>