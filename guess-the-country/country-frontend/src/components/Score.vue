<template>
  <div class="wrapper">
    <section class="left xd-section xd-light">
      <p>Round: {{ round + roundOffset }}/{{ totalNumOfRounds }}</p>
      <p v-if="showScore">Score: {{scoreHuman}} : {{scoreAI}}</p>
    </section>
  </div>
</template>
<script>
import {gameStore} from "@/stores/gameStore";

export default {
  name: "Score",
  props: {
    showScore: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    round() {
      return gameStore.round
    },
    roundOffset() {
      return gameStore.roundOffset
    },
    totalNumOfRounds() {
      return gameStore.totalNumOfRounds
    },
    scoreAI() {
      return gameStore.scoreAI
    },
    scoreHuman() {
      return gameStore.scoreHuman
    }
  }
}
</script>
<style scoped>

.wrapper {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  width: 100%;
  gap: 10px;
  text-align: center;
}

.xd-section:last-child {
  margin-bottom: 12px;
}
</style>
