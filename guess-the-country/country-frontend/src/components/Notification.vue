<template>
  <div class="notification">
    <section class="xd-section xd-light">
      <!-- Question -->
      <section v-show="showQuestion">
        <p v-if="sequenceMode==='classic'">Your guess: Where has this Google Streetview picture been taken?</p>
        <p v-else>Where has this Google Streetview picture been taken?</p>
      </section>
      <!-- User guess -->
      <section v-show="showUserGuess">
        <p class="short-text">Your guess is: {{ roundStore.humanCity }}</p>
      </section>
      <!-- control group (without explanation), AI guess -->
      <section v-show="showAIGuess&&playerInControlGroup">
        <p class="short-text">My guess is: {{ roundStore.aiCity }}</p>
      </section>
      <!-- treatment group (with explanation), AI guess -->
      <section v-show="showAIGuess&&!playerInControlGroup">
        <p>My guess is: {{ roundStore.aiCity }}
          <br>In particular, the colored areas below have helped me form my guess. </p>
        <p v-if="sequenceMode==='recommender'">What is your guess?</p>
      </section>
    </section>
  </div>
</template>
<script>
import axios from "axios";
import {roundStore} from "@/stores/roundStore";

export default {
  name: "Notification",
  props: {
    playerInControlGroup: {
      type: Boolean
    },
    sequenceMode: {
      type: String
    },
  },
  computed: {
    roundStore() {
      return roundStore
    },
    showQuestion() {
      if (this.sequenceMode === 'classic' || this.sequenceMode === 'basic') {
        return !roundStore.humanCity
      } else if (this.sequenceMode === 'recommender') {
        return !roundStore.aiCity
      } else {
        return false
      }
    },
    showUserGuess() {
      if (this.sequenceMode === 'classic') {
        return roundStore.humanCity && !roundStore.aiCity
      } else if (this.sequenceMode === 'recommender' || this.sequenceMode === 'basic') {
        return roundStore.humanCity
      } else {
        return false
      }
    },
    showAIGuess() {
      if (this.sequenceMode === 'classic') {
        return roundStore.aiCity
      } else if (this.sequenceMode === 'recommender') {
        return roundStore.aiCity && !roundStore.humanCity
      } else
        return false
    },
  },

  data() {
    return {
      msg: "Hello",
      backendUrl: ""
    }
  },
  methods: {
    async getMessage() {
      await axios
          .get(this.backendUrl + "/msg")
          .then((res) => {
            this.msg = res.data.data;
          })
          .catch((error) => {
            console.error(error);
          });
    },
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
