<template>
  <div id="app" class="xd-app">
    <GitHubRibbon url="https://github.com/xai-demonstrator/xai-demonstrator"/>
    <XAIStudioRibbon url="https://www.xai-studio.de"/>
    <UseCaseHeader
        v-bind:standalone="!Boolean(backendUrl)"
        v-bind:title="useCaseTitle"
    />
    <main>
      <Score/>
      <Notification ref="notification"
                    :playerInControlGroup="playerInControlGroup"
                    :sequenceMode="sequenceMode"
                    :backendUrl="backendUrl"
      />
      <StreetView ref="streetview" :backendUrl="backendUrl"/>
      <Selection v-if="showSelection"
                 @city_selected="judgeRound"
      />
      <button
          v-show="!showSelection"
          type="button"
          class="xd-button xd-secondary"
          v-on:click="buttonClick"
      >
        {{ buttonLabel }}
      </button>
    </main>
  </div>
</template>

<script>
import axios from "axios";
import {GitHubRibbon, UseCaseHeader, XAIStudioRibbon,} from "@xai-demonstrator/xaidemo-ui";
import Notification from "@/components/Notification";
import Selection from "@/components/Selection";
import Score from "@/components/Score.vue";
import {gameStore} from "@/stores/gameStore";
import {roundStore, resetRoundStore} from "@/stores/roundStore";
import StreetView from "@/components/StreetView.vue";

export default {
  name: "App",
  components: {
    StreetView,
    UseCaseHeader,
    GitHubRibbon,
    XAIStudioRibbon,
    Notification,
    Selection,
    Score,
  },
  computed: {
    searchParams() {
      const uri = window.location.search.substring(1);
      return new URLSearchParams(uri);
    },
    sequenceMode() {
      if (this.searchParams.has("modus")) {
        return this.searchParams.get("modus")
      } else {
        return process.env.VUE_APP_IMAGE_SEQUENCE_MODE
      }
    },
    numOfRounds() {
      if (this.searchParams.has("num_of_rounds")) {
        return this.searchParams.get("num_of_rounds")
      } else {
        return JSON.parse(process.env.VUE_APP_NR_OF_ROUNDS)
      }
    },
    roundOffset() {
      if (this.searchParams.has("round_offset")) {
        return JSON.parse(this.searchParams.get("round_offset"))
      } else {
        return 0
      }
    },
    playerInControlGroup() {
      return this.searchParams.has("control");
    },
    playerId() {
      if (this.searchParams.has("player")) {
        return this.searchParams.get("player");
      } else {
        return ""
      }
    },
    round() {
      return gameStore.round
    },
    scoreAI() {
      return gameStore.scoreAI
    },
    scoreHuman() {
      return gameStore.scoreHuman
    },
    gameFinished() {
      return (gameStore.round === gameStore.totalNumOfRounds)
    },
    backendUrl() {
      if (this.playerId !== "") {
        return this.url + "/" + this.playerId;
      } else {
        return this.url;
      }
    },
    buttonLabel() {
      if (this.gameFinished) {
        return "Start again!"
      } else {
        return "Button!"
      }
    },
    showSelection() {
      if (this.sequenceMode === 'classic' || this.sequenceMode === 'basic') {
        return (roundStore.humanCity === "")
      } else if (this.sequenceMode === 'recommender') {
        if (this.playerInControlGroup) {
          return (roundStore.aiCity !== "" && roundStore.humanCity !== "")
        } else {
          return (roundStore.aiCity !== "" && roundStore.humanCity !== "")
        }
      } else {
        return false
      }
    },
  },

  data() {
    return {
      url: process.env.VUE_APP_BACKEND_URL,
      useCaseTitle: "Guess the City",
    };
  },
  async mounted() {
    await this.$refs.notification.getMessage();
    await this.startGame()
  },
  methods: {
    buttonClick() {
      if (this.gameFinished) {
        this.startGame()
      } else {
        this.$refs.streetview.explain()
      }
    },
    startGame() {
      gameStore.round = 0
      gameStore.roundOffset = this.roundOffset
      gameStore.totalNumOfRounds = this.numOfRounds
      gameStore.scoreAI = 0
      gameStore.scoreHuman = 0
      this.startRound()
    },
    async startRound() {
      resetRoundStore()
      gameStore.round = 1 + gameStore.round
      roundStore.currentRound = gameStore.round + gameStore.roundOffset
      await this.$refs.streetview.getStreetview();
    },
    judgeRound(humanResponse) {
      roundStore.humanCity = humanResponse;
      if (roundStore.humanCity === roundStore.trueCity) {
        gameStore.scoreHuman = 1 + gameStore.scoreHuman;
      }
      this.recordRound()
      if (gameStore.round < gameStore.totalNumOfRounds) {
        this.startRound()
      } else {
        this.finishGame()
      }
    },
    async recordRound() {
      /* TODO: Only do this if running an experiment */
      await axios
          .post(this.backendUrl + "/score", {
            ...gameStore,
            ...roundStore
          })
          .catch((error) => {
            console.error(error);
          });
    },
    finishGame() {
      console.log("Done")
    },
    async finalScore() {
      /* TODO: Only do this if running an experiment */
      await axios
          .get(this.backendUrl + "/final_score")
          .then((res) => {
            gameStore.round = res.data.rounds;
            gameStore.scoreAI = res.data.ai_score;
            gameStore.scoreHuman = res.data.player_score;
          })
          .catch((error) => {
            console.error(error);
          });
    },
  },
};
</script>

<style>
.header-icon {
  visibility: hidden;
}

#app {
  display: flex;
  justify-content: space-between;
  position: relative;
}

main {
  display: flex;
  flex-direction: column;
  align-items: center;
}

@media screen and (max-width: 450px) {
  #app {
    flex-direction: column;
    padding-left: 0;
    padding-right: 0;
  }
}

@media screen and (min-width: 450px) and (max-height: 650px) {
  #img {
    width: 40%;
  }

  #app {
    margin-left: 20%;
    margin-right: 20%;
    overflow: scroll !important;
  }
}

@media screen and (min-width: 450px) and (min-height: 650px) {
  #app {
    flex-direction: column;
  }

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
