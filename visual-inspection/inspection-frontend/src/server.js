import {Server} from 'miragejs'

export function makeServer({environment = "development"} = {}) {

    const labels = ["kein Hund", "keine Katze", "keine Ziege"]

    let server = new Server({
        environment,

        routes() {
            this.post("/predict", () => ({
                prediction_id: 'abc',
                class_label: labels[Math.floor(Math.random() * labels.length)],
                class_id: 4,
               class_percentage : 1.0
            }),
                {timing: 2000})

            this.post("/explain", () => ({
                    image: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAG4AAADgCAIAAABtg8QEAAACyUlEQVR4nO3QVVIQAAAAURQVMRGxA0GxuzsQscDu7vb+v97Cmd3ZE7zZHRhYsHBw0eIlQ0uHly1fsXLV6pE1o2vH1q3fsHHT5i1bt20f3zExuXPX1O49e/ftP3Dw0OEjR48dP3Hy1OkzZ8+dv3Dx0uUrV69NX5+5MXvz1u07d+fm791/8PDR4ydPnz1/8fLV6zdv373/8PHT5y9fv33/8fPX7z9/1Zo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1ddx/1f4BkHd8dHEnmT0AAAAASUVORK5CYII='
                }),
                {timing: 4000})

        },
    })

    return server
}
