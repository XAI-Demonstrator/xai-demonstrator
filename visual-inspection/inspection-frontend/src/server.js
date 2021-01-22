import {Server} from 'miragejs'

export function makeServer({environment = "development"} = {}) {

    let server = new Server({
        environment,

        routes() {
            this.post("/predict", () => ({
                prediction_id: 'abc',
                class_label: "Hund",
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
