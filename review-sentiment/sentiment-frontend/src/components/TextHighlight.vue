<template>
  <div class="highlight-box">
    <div>
      <span v-for="pair in processedExplanation" :key="pair.word + Math.random()"
            v-bind:style="{'color': calcHSL(pair.score)}">{{ whitespace(pair.word) }}{{ pair.word }}</span>
    </div>
    <div class="legend">
      <div class="legend-entry"><div class="legend-marker xd-green"></div><span class="legend-text">stärker</span></div>
      <div class="legend-entry"><div class="legend-marker xd-red"></div><span class="legend-text">schwächer</span></div>
    </div>
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
        return Math.min(this.preScaler * Math.abs(score) * 40, 40)
      } else {
        return Math.min(this.preScaler * Math.abs(score) * 27, 27)
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
  display: flex;
  flex-direction: column;
}

.legend {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
}

.legend-entry {
  display: flex;
  flex-direction: row;
  align-items: baseline;
  padding-left: 8px;
}

.legend-marker {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-text {
  font-size: small;
  padding-left: 4px;
}
</style>