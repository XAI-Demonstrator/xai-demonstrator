<template>
  <div class="wrapper">
    <section class="left xd-section xd-light">
      <p>Round:  {{ gameStore.round + gameStore.roundOffset }}/{{ gameStore.totalNumOfRounds }}</p>
      <p v-if="showScore">Score: {{gameStore.scoreHuman}} : {{gameStore.scoreAI}}</p>
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
    gameStore() {
      return gameStore
    },
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
