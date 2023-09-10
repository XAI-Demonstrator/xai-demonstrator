<template>
  <section class="xd-section xd-light">
    <img
        v-if="explanation"
        class="xd-border-secondary"
        v-bind:src="this.explainImage"
    />
    <img
        v-else
        class="xd-border-secondary"
        v-bind:src="this.streetviewImage"
    />
    <SpinningIndicator
        class="indicator"
        v-bind:visible="waitingForBackend"
    />
  </section>
</template>

<script>
import {SpinningIndicator} from "@xai-demonstrator/xaidemo-ui";
import axios from "axios";
import {gameStore} from "@/stores/gameStore";
import {roundStore, setGroundTruth, setAiResponse} from "@/stores/roundStore";

export default {
  name: 'StreetView',
  props: {
    backendUrl: {
      type: String,
      default: ""
    }
  },
  components: {
    SpinningIndicator
  },
  data() {
    return {
      streetviewImage: null,
      explainImage: null,
      explanation: "",
      waitingForBackend: false
    }
  },
  methods: {
    async getStreetview() {
      this.waitingForBackend = true
      this.$emit("streetview-requested")

      await axios
          .post(this.backendUrl + "/streetview", {
            ...gameStore,
            ...roundStore
          })
          .then((res) => {
            this.streetviewImage = res.data.image;
            setGroundTruth(res.data.class_label);
            this.waitingForBackend = false
            this.$emit("streetview-received", true)
          })
          .catch((error) => {
            console.log(error);
            this.waitingForBackend = false
            this.$emit("streetview-received", false)
          });

      await this.predict()
    },
    async predict() {
      this.waitingForBackend = true
      this.$emit("prediction-requested")

      const blob = new Blob([this.streetviewImage]);

      let form = new FormData();
      form.append("file", blob);

      await axios
          .post(this.backendUrl + "/predict", form, {
            headers: {
              Accept: "application/json",
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            setAiResponse(res.data.class_label);
            if (roundStore.trueCity === roundStore.aiCity) {
              gameStore.scoreAI = gameStore.scoreAI + 1;
            }
            this.waitingForBackend = false
            this.$emit("prediction-received", true)
          })
          .catch((error) => {
            console.error(error);
            this.waitingForBackend = false
            this.$emit("prediction-received", false)
          });
    },
    async explain() {
      this.waitingForBackend = true
      this.$emit("explanation-requested")

      const blob = new Blob([this.streetviewImage]);

      let form = new FormData();
      form.append("file", blob);

      await axios
          .post(this.backendUrl + "/explain", form, {
            headers: {
              Accept: "application/json",
              "Content-Type": "multipart/form-data",
            },
          })
          .then((res) => {
            this.explainImage = res.data.image;
            this.explanation = res.data.explanation_id;
            this.waitingForBackend = false
            this.$emit("explanation-received", true)
          })
          .catch((error) => {
            console.error(error);
            this.waitingForBackend = false
            this.$emit("explanation-received", false)
          });
    },
  }
}
</script>
<style>

main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

@media screen and (max-width: 450px) {
}

@media screen and (min-width: 450px) and (max-height: 650px) {

}

@media screen and (min-width: 450px) and (min-height: 650px) {

  main {
    flex-grow: 1;
  }

  main section {
    padding: 0;
  }
}

img {
  width: 100%;
}
</style>