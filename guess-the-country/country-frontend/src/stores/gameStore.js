import {reactive} from 'vue'

export const gameStore = reactive({
    round: 0,
    roundOffset: 0,
    totalNumOfRounds: 0,
    scoreAI: 0,
    scoreHuman: 0
})
