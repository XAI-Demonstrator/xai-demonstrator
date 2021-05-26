<template>
  <div class="highlight-box">
    <span v-for="pair in processedExplanation" :key="pair.word + Math.random()"
          v-bind:style="{'color': calcHSL(pair.score)}">{{ whitespace(pair.word) }}{{ pair.word }}</span>
    <p class ="legend-text">stärker</p>
    <span class = "legend-box xd-green"></span>
    <p class ="legend-text">schwächer</p>
      <span class = "legend-box xd-red"></span>
  </div>
</template>

<script>
export default {
  name: "TextHighlight",
  props: {
    explanation: {
      type: Array,
      default: function () {
        return []
      }
    }, maxScore: {
      type: Number,
      default: 1.0
    }, preScaler: {
      type: Number,
      default: 5.0
    }
  },
  data() {
    return {
      noSpaceInFrontOf: [",", ".", "!", ":", ";", "?"]
    }
  },
  computed: {
    processedExplanation() {
      return this.rescaleScores(this.explanation)
    }
  },
  methods: {
    calcHSL(score) {
      return 'hsl(' + this.calcHue(score) + ',100%,' + this.calcLightness(score) + '%)'
    },
    calcHue(score) {
      if (score <= 0) {
        return 0
      } else {
        return 174
      }
    },
    calcLightness(score) {
      if (score <= 0) {
        return 40
      } else {
        return 27
      }
    },
    whitespace(word) {
      if (this.noSpaceInFrontOf.includes(word)) {
        return ""
      } else {
        return " "
      }
    },
    rescaleScores(explanation) {
      const factor = this.getScalingFactor(explanation)
      return explanation.map(function (pair) {
        return {word: pair.word, score: pair.score * factor}
      })
    },
    getScalingFactor(explanation) {
      return Math.max(1.0, this.maxScore / explanation.reduce(
          (prevMax, pair) =>
              Math.max(prevMax, Math.abs(pair.score)), -Infinity))
    }
  }
}
</script>

<style scoped>
.highlight-box {
  background-color: #fff;
  padding: 8px;
}

.legend-text{
  font-size: small;
  padding: 0;
  margin:0 0.25em;
  display: inline-block;
  float: right;
  text-align: center;
  vertical-align: middle;
  line-height: 1.4em;
}

.legend-box{
  width: 1em;
  height: 1em;
  display: inline-block;
  vertical-align: middle;
  border-radius: 0.1em;
  float: right;
}

</style>