import {Server} from 'miragejs'

export function makeServer({environment = "development"} = {}) {

    let server = new Server({
        environment,

        routes() {
            this.post("/predict", () => ({
                prediction_id: 'abc',
                prediction: [0.0, 0.0, 1.0, 0.0, 0.0]
            }))

            this.post("/explain", () => ({
                prediction: {
                    prediction_id: 'abc',
                    prediction: [0.0, 0.0, 1.0, 0.0, 0.0]
                },
                explanation: {
                    explanation_id: 'def',
                    explanation: [
                        ["Super", 0.7],
                        ["Pizza", 0.3],
                        ["und", null],
                        ["schneller", 0.2],
                        ["Service", -0.4],
                        ["-", null],
                        ["gerne", 0.3],
                        ["bald", 0.02],
                        ["wieder", -0.07],
                        ["!", null],
                        ["!", null]
                    ]
                }
            }))


        },
    })

    return server
}
