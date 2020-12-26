import {Server} from 'miragejs'

export function makeServer({environment = "development"} = {}) {

    let server = new Server({
        environment,

        routes() {
            this.post("/predict", () => ({
                prediction_id: 'abc',
                prediction: [0.0, 0.0, 1.0, 0.0, 0.0]
            }))

        },
    })

    return server
}
