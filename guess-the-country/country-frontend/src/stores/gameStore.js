import { reactive } from "vue";

export const gameStore = reactive({
  round: 0,
  roundOffset: 0,
  totalNumOfRounds: 0,
  scoreAi: 0,
  scoreHuman: 0,
  gameId: "",
  playerId: "",
});
