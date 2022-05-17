import {reactive} from 'vue'

export const modelConfig = reactive({
    smartphone: {amount: "0", label: "smartphone"},
    pencil: {amount: "15", label: "pencil"},
    cup: {amount: "15", label: "cup"},
    getModelId() {
      let id = "model_"
      id += this.smartphone.amount
      if (this.smartphone.label === "cup" && this.smartphone.amount !== "0") {
        id += "T"
      }
      id += "_" + this.pencil.amount
      if (this.pencil.label === "cup") {
        id += "T"
      }
      id += "_" + this.cup.amount
      return id
    }
})

export const availableModels = {
    smartphone: {
        amounts: ["0", "15", "200"],
        labels: ["smartphone", "cup"],
        image: "smartphones.jpg",
        name: "A"
    },
    pencil: {
        amounts: ["15", "200"],
        labels: ["pencil", "cup"],
        image: "pencils.jpg",
        name: "B"
    },
    cup: {
        amounts: ["15", "200"],
        labels: ["cup"],
        image: "cups.jpg",
        name: "C"
    }
}
