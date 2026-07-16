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
                        probability: (Math.random() * 100).toFixed(6),
                        class_label: label,
                        class_id: 4
                    }
                },
            {
                timing: 1000
            }
        )

            this.post("/explain", () => ({
                    image: 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAG4AAADgCAIAAABtg8QEAAACyUlEQVR4nO3QVVIQAAAAURQVMRGxA0GxuzsQscDu7vb+v97Cmd3ZE7zZHRhYsHBw0eIlQ0uHly1fsXLV6pE1o2vH1q3fsHHT5i1bt20f3zExuXPX1O49e/ftP3Dw0OEjR48dP3Hy1OkzZ8+dv3Dx0uUrV69NX5+5MXvz1u07d+fm791/8PDR4ydPnz1/8fLV6zdv373/8PHT5y9fv33/8fPX7z9/1Zo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1dVwroZo6rpVQTR3XSqimjmslVFPHtRKqqeNaCdXUca2Eauq4VkI1ddx/1f4BkHd8dHEnmT0AAAAASUVORK5CYII=',
                    explanation_strs: {
                        de: "Die Vorhersage wurde getroffen, da auf dem Bild die Konzepte <strong>Bildschirm</strong>, <strong>rechteckige Form</strong> und <strong>zylindrische Form</strong> erkannt wurden.",
                        en: "The prediction was made because the concepts <strong>screen</strong>, <strong>rectangular form</strong>, and <strong>cylindrical form</strong> were detected in the image."
                    },
                    conceptScores: [
                        {concept: {de: "Bildschirm", en: "screen"}, score: 0.31314950730820795},
                        {concept: {de: "rechteckige Form", en: "rectangular form"}, score: 0.15505504631539418},
                        {concept: {de: "zylindrische Form", en: "cylindrical form"}, score: 0.09723404950990615},
                        {concept: {de: "Griff", en: "handle"}, score: 0.08705633503492316},
                        {concept: {de: "Linse", en: "lens"}, score: 0.06984529651253744},
                        {concept: {de: "kompakte Rundform", en: "compact rounded form"}, score: -0.04590072711063772},
                        {concept: {de: "Tasten und Knöpfe", en: "keys and buttons"}, score: 0.034283461568002944},
                        {concept: {de: "ovale Form", en: "oval form"}, score: 0.020987912941632866},
                        {concept: {de: "runde Form", en: "round form"}, score: 0.017443794514502304},
                        {concept: {de: "runde Öffnung", en: "circular opening"}, score: -0.007875994371659372}
                    ]
                }),
                {timing: 2000})

        },
    })

    return server
}
