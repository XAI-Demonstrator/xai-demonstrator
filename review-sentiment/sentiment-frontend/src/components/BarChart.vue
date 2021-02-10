<template>
  <div class="barchart">
    <div class="line" v-for="pair in processedExplanation.slice(0,maxNumOfBars)" :key="pair.word + Math.random()">
      <div class="bar">
        <div class="progress" v-bind:style="{'--importance': pair.score}"
             v-bind:class="{'positive': pair.score > 0}">
        </div>
      </div>
      <div class="word">{{ pair.word }}</div>
    </div>
    <div class="legend">
      <div class="legend-element">
        &#9668; negativ
      </div>
      <div class="legend-element legend-right">
        positiv &#9658;
      </div>
      <div class="legend-element">&nbsp;</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "BarChart",
  props: {
    explanation: {
      type: Array,
      default: function () {
        return []
      }
    },
    maxNumOfBars: {
      type: Number,
      default: 5
    },
    minLengthOfLongestBar: {
      type: Number,
      default: 0.8
    }
  },
  computed: {
    processedExplanation() {
      return this.sortByScore(this.rescaleScores(this.explanation))
    }
  }, methods: {
    sortByScore(explanation) {
      return [...explanation].sort(function (a, b) {
        return Math.abs(b.score) - Math.abs(a.score)
      })
    },
    rescaleScores(explanation) {
      const factor = this.getScalingFactor(explanation)
      return explanation.map(function (pair) {
        return {word: pair.word, score: pair.score * factor}
      })
    },
    getScalingFactor(explanation) {
      return Math.max(1.0, this.minLengthOfLongestBar / explanation.reduce(
          (prevMax, pair) =>
              Math.max(prevMax, Math.abs(pair.score)), -Infinity))
    }
  }
}
</script>

<style scoped>
:root {
  --importance: 0;
}

.barchart {
  display: flex;
  flex-direction: column;
  background-color: #fff;
}

.line {
  width: 100%;
  height: 20px;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.bar {
  height: 100%;
  flex: 2;
  display: flex;
  align-items: center;
}

.word {
  flex: 1;
}

.progress {
  background-color: #CC0000;
  width: max(calc(var(--importance) * 50%), calc(var(--importance) * -50%));
  height: 12px;
  margin-left: min(calc(50% + var(--importance) * 50%), 50%);
  border-radius: 2px;
}

.positive {
  background-color: #00887A;
}

.legend {
  width: 100%;
  height: 20px;
  display: flex;
  justify-content: space-evenly;
  flex-direction: row;
  align-items: center;
}

.legend-element {
  font-size: small;
  flex: 1;
  padding-left: 10px;
  padding-right: 10px;
}

.legend-right {
  text-align: right;
}
</style>