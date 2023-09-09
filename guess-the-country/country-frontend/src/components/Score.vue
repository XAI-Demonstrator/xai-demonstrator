<template>
  <div class="wrapper">
    <section class="left xd-section xd-light">
      <p>Round: {{ round }}/{{ totalNumOfRounds }}</p>
    </section>
  </div>
</template>
<script>
import {gameStore} from "@/gameStore";

export default {
  name: "Score",
  computed: {
    round() {
      return gameStore.round
    },
    totalNumOfRounds() {
      return gameStore.totalNumOfRounds
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
