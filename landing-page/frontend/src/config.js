// This setup is based on https://medium.com/dzangolab/vue-js-environment-variables-799fc080d736
const config = {

    useCases: [
        {
            logo: require('@/assets/sentiment-stars.svg'),
            title: "Stimmung erkennen",
            description: "Entdecke, wie die KI die Stimmung in einem Text bestimmt!",
            route: "/sentiment/",
            include: parse(process.env.VUE_APP_SENTIMENT, false)
        },
        {
            logo: require('@/assets/inspection-eye.svg'),
            title: "Gegenstände erkennen",
            description: "Finde heraus, woran die KI Gegenstände auf Bildern erkennt!",
            route: "/inspection/",
            include: parse(process.env.VUE_APP_INSPECTION, false)
        },
        {
            logo: require('@/assets/inspection-eye.svg'),
            title: "Guess the Country",
            description: "Kannst du besser als die KI zwischen Tel-Aviv und Berlin unterscheiden?",
            route: "/country/",
            include: parse(process.env.VUE_APP_COUNTRY, false)
        }
    ]
}

function parse (value, fallback) {
  if (typeof value === 'undefined') {
    return fallback
  }
  switch (typeof fallback) {
    case 'boolean' :
      return !!JSON.parse(value)
    case 'number' :
      return JSON.parse(value)
    default :
      return value
  }
}

export {
  config
}
export default {
  install (Vue) {
    Vue.appConfig = config
    Vue.config.globalProperties.$appConfig = config
  }
}
