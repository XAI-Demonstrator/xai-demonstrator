import {Server} from 'miragejs'

export function makeServer({environment = "development"} = {}) {

    const labels =
        {
            "de": ["kein Hund", "keine Katze", "keine Ziege"],
            "en": ["not a dog", "not a cat", "not a goat"]
        }

    let server = new Server({
        environment,

        routes() {
            this.post("/predict", (schema, request) => {
                    console.log(Array.from(request.requestBody.keys(), entry => entry))
                    console.log(request.requestBody.get("language"))

                    let locale = "de"
                    if (request.requestBody.get("language") === "en") {
                        locale = "en"
                    }
                    let label = labels[locale][Math.floor(Math.random() * labels[locale].length)]
                    if (request.requestBody.get("model_id") === "model_0_15_15") {
                        label = 'Digital Education'
                    }

                    return {
                        prediction_id: 'abc',
                        class_label: label,
                        class_id: 4
                    }
                },
            {
                timing: 1000
            }
        )

            this.post("/explain", () => ({
                    image: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAG4AAADgCAIAAABtg8QEAAACyUlEQVR4nO3QVVIQAAAAURQVMRGxA0GxuzsQscDu7vb+v97Cmd3ZE7zZHRhYsHBw0eIlQ0uHly1fsXLV6pE1o2vH1q3fsHHT5i1bt20f3zExuXPX1O49e/ftP3Dw0OEjR48dP3Hy1OkzZ8+dv3Dx0uUrV69NX5+5MXvz1u07d+fm791/8PDR4ydPnz1/8fLV6zdv373/8PHT5y9fv33/8fPX7z9/1Zo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1ddx/1f4BkHd8dHEnmT0AAAAASUVORK5CYII='
                }),
                {timing: 2000})

        },
    })

    return server
}
