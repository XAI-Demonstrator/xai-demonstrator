<template>
  <div id="app">
    <UseCaseHeader v-bind:standalone="!Boolean(backendUrl)"/>
    <ComposeReview ref="composer"
                   v-bind:introduction-text="introductionTexts[reviewTopic]"
                   v-bind:default-review="defaultReviews[reviewTopic]"
                   v-bind:show-intro="!numberOfStars"
                   v-on:reviewChanged="reviewTextChanged"/>
    <AnalyzeReview ref="analyzer"
                   v-bind:review-text="reviewTextToAnalyze"
                   v-bind:num-of-stars="numberOfStars"
                   v-on:analysisRequested="analysisRequested"
                   v-on:analysisCompleted="analysisCompleted"/>
    <ExplainAnalysis ref="explainer"
                     v-bind:is-active="numberOfStars"
                     v-bind:review-text="reviewTextToAnalyze"/>
    <FloatingInfoButton v-bind:info-text="infoText"
                        v-bind:info-url="infoUrl"
                        v-bind:link-label="infoLinkLabel"/>
  </div>
</template>

<script>
import ComposeReview from "@/components/ComposeReview";
import AnalyzeReview from "@/components/AnalyzeReview";
import ExplainAnalysis from "@/components/ExplainAnalysis";
import {FloatingInfoButton, UseCaseHeader} from "@xai-demonstrator/xaidemo-ui";


export default {
  name: 'App',
  components: {
    ComposeReview,
    AnalyzeReview,
    ExplainAnalysis,
    FloatingInfoButton,
    UseCaseHeader
  },
  data() {
    return {
      introductionTexts: {
        'movie': 'Wie war der Film, den du zuletzt gesehen hast?',
        'restaurant': 'Wie war dein letzter Restaurant-Besuch?',
        'travel': 'Wie hat dir deine letzte Reise gefallen?'
      },
      defaultReviews: {
        'movie': 'Die Story war ziemlich vorhersehbar, würde ich nicht empfehlen...',
        'restaurant': 'Super Pizza und schneller Service - gerne bald wieder!!',
        'travel': 'Der Zug kam natürlich zu spät, aber die Aussicht war einmalig!'
      },
      infoText: [
        {
          headline: "Review Sentiment",
          paragraphs: ["Kunden-Reviews sind sehr populär im Internet."]
        },
        {
          headline: "Hinter den Kulissen",
          paragraphs: ["Die Reviews werden von einem modernen NLP-Modell analysiert.",
            "Es kann auch mit anderen Sprachen als Deutsch umgehen, z.B. Französisch oder Englisch."
          ]
        }
      ],
      infoUrl: "/",
      infoLinkLabel: "More Information",
      reviewText: '',
      numberOfStars: null,
      reviewTopic: ['movie', 'restaurant', 'travel'][Math.floor(Math.random() * 3)],
      backendUrl: process.env.VUE_APP_BACKEND_URL
    }
  },
  methods: {
    reviewTextChanged(value) {
      this.reviewText = value
      this.$refs.analyzer.resetComponent()
      this.$refs.explainer.resetComponent()
      this.numberOfStars = null
    },

    analysisRequested() {
      this.$refs.explainer.resetComponent()
      this.numberOfStars = null
    },

    analysisCompleted(value) {
      this.numberOfStars = value
    }
  },
  computed: {
    reviewTextToAnalyze() {
      return this.reviewText || this.defaultReviews[this.reviewTopic]
    }
  },
  created() {
    document.title = "Review Sentiment – XAI Demonstrator"
  }
}
</script>

<style>
* {
  box-sizing: border-box;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}

.mint-indicator-wrapper {
  background-color: #00887A !important;
}

.mint-spinner-snake {
  border-top-color: #D3E3FC !important;
  border-bottom-color: #D3E3FC !important;
  border-left-color: #D3E3FC !important;
}

@media screen and (min-width: 450px) {
  body {
    background-color: #FFFFFF;
  }

  #app {
    margin: 40px auto auto;
    max-width: 425px;
    border: 1px solid #D3E3FC;
    padding: 1em 5px 5px;
  }
}
</style>
