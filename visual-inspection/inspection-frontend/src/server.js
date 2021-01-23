import {Server} from 'miragejs'

export function makeServer({environment = "development"} = {}) {

    const labels = ["Hund", "Katze", "Ziege"]

    let server = new Server({
        environment,

        routes() {
            this.post("/predict", () => ({
                prediction_id: 'abc',
                class_label: labels[Math.floor(Math.random() * labels.length)],
                class_id: 4
            }))

            this.post("/explain", () => ({
                explanation_id: 'def',
                explanation: "Hat Ohren"
            }))

        },
    })

    return server
}
