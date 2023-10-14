import { reactive } from "vue";

export const gameStore = reactive({
  round: 0,
  roundOffset: 0,
  totalNumOfRounds: 0,
  aiScore: 0,
  humanScore: 0,
  gameId: "",
  playerId: "",
});
