<template>
  <div id="app">
    <UseCaseHeader v-bind:standalone="!Boolean(backendUrl)"
                   v-bind:title="useCaseTitle"/>
    <main>
      <ComposeReview ref="composer"
                     v-bind:introduction-text="introductionTexts[reviewTopic]"
                     v-bind:default-review="defaultReviews[reviewTopic]"
                     v-bind:show-intro="!numberOfStars"
                     v-on:reviewChanged="reviewTextChanged"/>
      <AnalyzeReview ref="analyzer"
                     v-bind:review-text="reviewTextToAnalyze"
                     v-on:analysisRequested="analysisRequested"
                     v-on:analysisCompleted="analysisCompleted"/>
      <ExplainAnalysis ref="explainer"
                       v-bind:is-active="numberOfStars"
                       v-bind:review-text="reviewTextToAnalyze"/>
    </main>
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
      useCaseTitle: "Review Sentiment",
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

body {
  padding: 0;
  margin: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #fff;
  height: 100vh;
  width: 100vw;
  display: flex;
}

main {
  flex-grow: 1;
}

.mint-indicator-wrapper {
  background-color: #00887A !important;
}

.mint-spinner-snake {
  border-top-color: #D3E3FC !important;
  border-bottom-color: #D3E3FC !important;
  border-left-color: #D3E3FC !important;
}

@media screen and (max-width: 450px) {

  #app {
    padding: 60px 7px 7px;
    overflow: scroll;
    flex-direction: column;
  }

}

@media screen and (min-width: 450px) and (max-height: 650px) {

  #app {
    flex-direction: row;
    padding: 60px 7px 7px;
  }

}

@media screen and (min-width: 450px) and (min-height: 650px) {

  body {
    background-color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100vw;
    height: 100vh;
  }

  #app {
    max-width: 450px;
    border: 1px solid #ddd;
    box-shadow: 2px 2px 5px 2px #eee;
    padding: 8px;
    height: auto;
    min-height: 640px;
    flex-direction: column;
    overflow: auto;
  }

}
</style>
