import {reactive} from 'vue'
import config from "@/assets/config.json"

export const roundStore = reactive({
    trueCity: "",
    trueCountry: "",
    aiCity: "",
    aiCountry: "",
    humanCity: "",
    humanCountry: "",
    currentRound: 0,
})

export function resetRoundStore() {
    roundStore.trueCity = ""
    roundStore.trueCountry = ""
    roundStore.aiCity = ""
    roundStore.aiCountry = ""
    roundStore.humanCity = ""
    roundStore.humanCountry = ""
    roundStore.currentRound = 0
}

export function setGroundTruth(backendLabel) {
    if (Object.prototype.hasOwnProperty.call(config, backendLabel)) {
        roundStore.trueCity = config[backendLabel].city
        roundStore.trueCountry = config[backendLabel].country
    }
}

export function setAiResponse(backendLabel) {
    console.log("Setting AI response")
    console.log(backendLabel)
    if (Object.prototype.hasOwnProperty.call(config, backendLabel)) {
        roundStore.aiCity = config[backendLabel].city
        roundStore.aiCountry = config[backendLabel].country
    }
}
