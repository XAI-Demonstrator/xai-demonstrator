<template>
  <div id="app" class="xd-app">
    <GitHubRibbon url="https://github.com/xai-demonstrator/xai-demonstrator" />
    <XAIStudioRibbon url="https://www.xai-studio.de" />
    <UseCaseHeader
      v-bind:standalone="Boolean(true)"
      v-bind:title="useCaseTitle"
    />
    <main>
      <Notification
        :prediction_city="prediction_city"
        :msg="msg"
        :label_city="label_city"
        :user_city_answer="user_city_answer"
        :explanation="explanation"
      />

      <section class="xd-section xd-light">
        <img v-if="explanation" class="xd-border-secondary;" v-bind:src="this.explainimage" />
        <img class="xd-border-secondary;" v-bind:src="this.streetviewimage" />  
      </section>

      <Selection
        @city_selected="city_selected"
        :label_city="label_city"
        :user_city_answer="user_city_answer"
      />
      <Explanation_legend
        :prediction_city="prediction_city"
        :explanation="explanation"
      />

      <button
        v-if="prediction_city && explanation == null"
        type="button"
        class="xd-button xd-secondary"
        id="explain"
        v-on:click="explain()"
      >
        <!-- v-show -->
        Why the AI guesses
      </button>
      <button
        v-if="explanation && round<15"
        type="button"
        class="xd-button xd-secondary"
        id="new"
        v-on:click="restart()"
      >
        Next round
      </button>
      <button
        v-if="!prediction_city && user_city_answer"
        type="button"
        class="xd-button xd-secondary"
        id="submit"
        v-on:click="submitFile()"
      >
        What the AI guesses
      </button>
      <SpinningIndicator
        class="indicator"
        v-bind:visible="waitingForExplanation"
      />
    </main>

  </div>
</template>

<script>
import axios from "axios";
import {
  UseCaseHeader,
  SpinningIndicator,
  XAIStudioRibbon,
  GitHubRibbon,
} from "@xai-demonstrator/xaidemo-ui";
import Notification from "@/components/Notification";
import Selection from "@/components/Selection";
import Explanation_legend from "./components/Explanation_legend.vue";

export default {
  name: "App",
  components: {
    UseCaseHeader,
    SpinningIndicator,
    GitHubRibbon,
    XAIStudioRibbon,
    Notification,
    Selection,
    Explanation_legend,
  },
  data() {
    return {
      countrys: [
        {
          country: "Israel",
          citys: [
            {
              city: "Tel Aviv",
              backend: "Tel_Aviv",
            },
            {
              city: "Jerusalem",
              backend: "Westjerusalem",
            },
          ],
        },
        {
          country: "Germany",
          citys: [
            {
              city: "Berlin",
              backend: "Berlin",
            },
            {
              city: "Hamburg",
              backend: "Hamburg",
            },
          ],
        },
      ],
      round: 1,
      useCaseTitle: "Guess the City",
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      explanation: null,
      prediction_country: null,
      prediction_city: null,
      label_city: null,
      user_city_answer: null,
      score_ai: 0,
      score_user: 0,
      msg: "",
      streetviewimage: null,
      explainimage: null,
      waitingForExplanation: false,
     
    };
  },
  async created() {
    this.getMessage();
    this.getStreetview();
  },
  methods: {
    city_selected(value) {
      this.user_city_answer = value;
      if (this.user_city_answer == this.label_city) {
        this.score_user = 1 + this.score_user;
      }
    },
    getMessage() {
      axios
        .get(this.backendUrl + "/msg")
        .then((res) => {
          this.msg = res.data.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getStreetview() {
      axios
        .get(this.backendUrl + "/streetview")
        .then((res) => {
          this.streetviewimage = res.data.image;
          let label = this.label_to_label(res.data.class_label);
          this.label_city = label.city;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    submitFile() {
      this.waitingForExplanation = true;
      const blob = new Blob([this.streetviewimage]);

      let form = new FormData();
      form.append("file", blob);

      axios
        .post(this.backendUrl + "/predict", form, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          let label = this.label_to_label(res.data.class_label);
          this.prediction_city = label.city;
          this.waitingForExplanation = false;
          if(this.prediction_country == this.label_country){
             this.score_ai = this.score_ai + 1;
          }

          if (this.prediction_city == this.label_city) {
            this.score_ai = this.score_ai + 1;
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
    explain() {
      this.waitingForExplanation = true;
      const blob = new Blob([this.streetviewimage]);

      let form = new FormData();
      form.append("file", blob);

      axios
        .post(this.backendUrl + "/explain", form, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((res) => {
          this.explainimage = res.data.image;
          this.waitingForExplanation = false;
          this.explanation = res.data.explanation_id;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    restart() {
      this.explanation = null;
      this.prediction_city = null;
      this.prediction_country = null;
      this.user_city_answer = null;
      this.user_country_answer = null;
      this.getStreetview();
      this.round = this.round + 1;
      console.log(this.round)
    },

    label_to_label(prediction) {
      for (let i in this.countrys) {
        for (let x in this.countrys[i].citys)
          if (prediction == this.countrys[i].citys[x].backend) {
            return {
              country: this.countrys[i].country,
              city: this.countrys[i].citys[x].city,
            };
          }
      }
    },
  },
};
</script>

<style>

#app {
  display: flex;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

main {
  display: flex;
  flex-direction: column;
}

@media screen and (max-width: 450px) {
  #app {
    flex-direction: column;
    padding-left: 0;
    padding-right: 0;
  }
}

@media screen and (min-width: 450px) and (max-height: 650px) {
  #app {
    flex-direction: column;
    padding-left: 0;
    padding-right: 0;
    overflow: auto;
    height: 100vh;
    width: 100vw;
  }


  main {
    flex: 2;
    max-height: calc(100vh - 54px);
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  main section {
    order: 2;
  }
}

@media screen and (min-width: 450px) and (min-height: 650px) {
  #app {
    flex-direction: column;
  }
  main {
    flex-grow: 1;
  }

  body {
    align-items: baseline !important;
  }

  main section {
    padding: 0;
  }
}

img {
  width: 100%;
}
</style>
