<template>
  <div id="app" class="xd-app">
    <GitHubRibbon url="https://github.com/xai-demonstrator/xai-demonstrator"/>
    <XAIStudioRibbon url="https://www.xai-studio.de"/>
    <UseCaseHeader
        :standalone="!Boolean(backendUrl)"
        :title="useCaseTitle"
        :reload="!experiment"
    />
    <main>
      <Score/>
      <Notification ref="notification"
                    :gameState="gameState"
      />
      <StreetView ref="streetview" :backendUrl="backendUrl"/>
      <Selection v-if="showSelection"
                 @city_selected="judgeRound"
      />
      <button
          v-show="showButton"
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
import {v4 as uuidv4} from "uuidv4";
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
    externalPlayerId() {
      if (this.searchParams.has("player")) {
        return this.searchParams.get("player");
      } else {
        return ""
      }
    },
    experiment() {
      return this.externalPlayerId !== ""
    },
    backendUrl() {
      if (this.externalPlayerId !== "") {
        return this.url + "/" + this.externalPlayerId;
      } else {
        return this.url;
      }
    },
    showSelection() {
      return this.gameState === "guess"
    },
    showButton() {
      switch (this.gameState) {
        case "guess":
          return false
        case "explain":
          return roundStore.explanationId !== ""
        case "finished":
          return !this.experiment
        default:
          return true
      }
    },
    buttonLabel() {
      switch (this.gameState) {
        case "ask":
          return "What do you think?"
        case "explain":
          return "Next round!"
        case "finished":
          return "Start again!"
        default:
          return "Button"
      }
    }
  },

  data() {
    return {
      url: process.env.VUE_APP_BACKEND_URL,
      useCaseTitle: "Guess the City",
      gameState: "start",
      localPlayerId: ""
    };
  },
  async mounted() {
    this.localPlayerId = uuidv4();
    await this.startGame()
  },
  methods: {
    buttonClick() {
      switch (this.gameState) {
        case "ask":
          this.explain()
          break
        case "explain":
          this.startRound()
          break
        case "finished":
          this.startGame()
      }
    },
    startGame() {
      gameStore.round = 0
      gameStore.roundOffset = this.roundOffset
      gameStore.totalNumOfRounds = this.numOfRounds
      gameStore.scoreAI = 0
      gameStore.scoreHuman = 0
      gameStore.gameId = uuidv4()
      if (this.externalPlayerId !== "") {
        gameStore.playerId = this.externalPlayerId
      } else {
        gameStore.playerId = this.localPlayerId
      }
      this.startRound()
    },
    async startRound() {
      this.gameState = "start"
      resetRoundStore()
      gameStore.round = 1 + gameStore.round
      roundStore.currentRound = gameStore.round + gameStore.roundOffset
      await this.guess()
    },
    async guess() {
      this.gameState = "guess"
      await this.$refs.streetview.getStreetview();
    },
    async explain() {
      this.gameState = "explain"
      await this.$refs.streetview.predict()
      await this.$refs.streetview.explain()
    },
    judgeRound(humanResponse) {
      roundStore.humanCity = humanResponse;
      if (roundStore.humanCity === roundStore.trueCity) {
        gameStore.scoreHuman = 1 + gameStore.scoreHuman;
      }
      this.recordRound()
      if (gameStore.round >= gameStore.totalNumOfRounds) {
        this.finishGame()
      } else {
        this.gameState = "ask"
      }
    },
    async recordRound() {
      if (this.experiment) {
        await axios
            .post(this.backendUrl + "/score", {
              ...gameStore,
              ...roundStore
            })
            .catch((error) => {
              console.error(error);
            });
      }
    },
    async finishGame() {
      this.gameState = "finished"
      await this.finalScore()
    },
    async finalScore() {
      if (this.experiment) {
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
