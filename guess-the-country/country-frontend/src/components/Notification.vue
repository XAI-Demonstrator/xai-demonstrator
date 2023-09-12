<template>
  <div class="notification">
    <section class="xd-section xd-light">
      <section>
        <p v-show="showQuestion">Where has this Google Streetview picture been taken?</p>
        <p v-show="showHumanAnswer">Your guess is: {{ roundStore.humanCity }}.</p>
        <p v-show="showThinking">Let me think for a second...</p>
        <p v-show="showAiAnswer">I think this picture was taken in {{ roundStore.aiCity }}.</p>
        <p v-show="roundStore.explanationId">In particular, the colored areas below have helped me form my guess:</p>
        <p v-show="showFinal">That was fun!</p>
      </section>
    </section>
  </div>
</template>
<script>
import {roundStore} from "@/stores/roundStore.js";

export default {
  name: "Notification",
  props: {
    gameState: {
      type: String,
      default: "start"
    }
  },
  computed: {
    roundStore() {
      return roundStore
    },
    showHumanAnswer() {
      return this.gameState === "ask"
    },
    showThinking() {
      return this.gameState === "explain" && !roundStore.aiCity
    },
    showAiAnswer() {
      return this.gameState === "explain" && roundStore.aiCity
    },
    showQuestion() {
      return this.gameState === "guess"
    },
    showFinal() {
      return this.gameState === "finished"
    }
  }
}

</script>
<style scoped>
.notification {
  width: 100%;
}

.xd-section:last-child {
  text-align: center;
  margin-bottom: 12px;
}

.short-text {
  line-height: 2;
}
</style>
