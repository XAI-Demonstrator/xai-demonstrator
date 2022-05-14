// This setup is based on https://medium.com/dzangolab/vue-js-environment-variables-799fc080d736
const config = {

    useCases: [
        {
            logo: require('@/assets/sentiment-stars.svg'),
            title: "sentiment-title",
            description: "sentiment-description",
            route: "/sentiment/",
            include: parse(process.env.VUE_APP_SENTIMENT, false)
        },
        {
            logo: require('@/assets/inspection-eye.svg'),
            title: "inspection-title",
            description: "inspection-description",
            route: "/inspection/",
            include: parse(process.env.VUE_APP_INSPECTION, false)
        },
        {
            logo: require('@/assets/inspection-eye.svg'),
            title: "country-title",
            description: "country-description",
            route: "/country/",
            include: parse(process.env.VUE_APP_COUNTRY, false)
        },
        {
            logo: require('@/assets/inspection-eye.svg'),
            title: "education-title",
            description: "education-description",
            route: "/education/",
            include: parse(process.env.VUE_APP_EDUCATION, false)
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
