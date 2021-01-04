<template>
  <div class="barchart">
    <div class="bar" v-for="pair in sortedExplanation.slice(0,maxNumOfBars)" :key="pair.word + Math.random()">
        <div class="progress" v-bind:style="{'--importance': pair.score,
         'background-color': pair.score < 0 ? '#FFCCBC' : '#00887A'}">
        </div>
        <div class="word">{{ pair.word }}</div>
      </div>
  </div>
</template>

<script>
export default {
  name: "BarChart",
  props: {
    explanation: {
      type: Array
    },
    maxNumOfBars: {
      type: Number,
      default: 3
    }
  },
  computed: {
    sortedExplanation() {
      return [...this.explanation].sort(function (a, b) {
        return Math.abs(b.score) - Math.abs(a.score)
      })
    }
  }
}
</script>

<style scoped>
:root {
  --importance: 0;
}

.barchart {
  background-color: #D3E3FC;
  padding: 5px 10px;
}

.bar {
  width: 100%;
  position: relative;
  height: 20px;
}

.progress {
  position: absolute;
  background-color: #77A6F7;
  width: max(calc(var(--importance) * 35%), calc(var(--importance) * -35%));
  height: 12px;
  margin-left: min(calc(35% + var(--importance) * 35%), 35%);;
  margin-top: 4px;
}

.word {
  position: absolute;
  margin-left: 70%;
  margin-right: 0;
}

</style>