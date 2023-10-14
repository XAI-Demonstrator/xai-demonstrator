<template>
  <section class="xd-section xd-light">
    <img
      v-if="roundStore.explanationId"
      class="xd-border-secondary"
      :src="explainImage"
    />
    <img v-else class="xd-border-secondary" :src="streetviewImage" />
    <SpinningIndicator class="indicator" :visible="waitingForBackend" />
  </section>
</template>

<script>
import { SpinningIndicator } from "@xai-demonstrator/xaidemo-ui";
import axios from "axios";
import { gameStore } from "@/stores/gameStore.js";
import {
  roundStore,
  setGroundTruth,
  setAiResponse,
} from "@/stores/roundStore.js";

export default {
  name: "StreetView",
  components: {
    SpinningIndicator,
  },
  props: {
    backendUrl: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      streetviewImage: null,
      explainImage: null,
      explanation: "",
      waitingForBackend: false,
    };
  },
  computed: {
    roundStore() {
      return roundStore;
    },
  },
  methods: {
    async getStreetview() {
      this.waitingForBackend = true;

      await axios
        .post(this.backendUrl + "/streetview", {
          ...gameStore,
          ...roundStore,
        })
        .then((res) => {
          this.streetviewImage = res.data.image;
          setGroundTruth(res.data.city);
          this.waitingForBackend = false;
        })
        .catch((error) => {
          console.log(error);
          this.waitingForBackend = false;
        });
    },
    async predict() {
      this.waitingForBackend = true;

      const blob = new Blob([this.streetviewImage]);

      let form = new FormData();
      form.append("file", blob);

      await axios
        .post(this.backendUrl + "/predict", form)
        .then((res) => {
          setAiResponse(res.data.class_label);
          if (roundStore.trueCity === roundStore.aiCity) {
            gameStore.aiScore = gameStore.aiScore + 1;
          }
          roundStore.predictionId = res.data.prediction_id;
          this.waitingForBackend = false;
        })
        .catch((error) => {
          console.error(error);
          this.waitingForBackend = false;
        });
    },
    async explain() {
      this.waitingForBackend = true;

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
          roundStore.explanationId = res.data.explanation_id;
          this.waitingForBackend = false;
        })
        .catch((error) => {
          console.error(error);
          this.waitingForBackend = false;
        });
    },
  },
};
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
