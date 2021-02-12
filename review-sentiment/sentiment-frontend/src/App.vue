<template>
  <div id="app" class="xd-app">
    <UseCaseHeader v-bind:standalone="!Boolean(backendUrl)"
                   v-bind:title="useCaseTitle"/>
    <main>
      <section class="xd-section xd-light">
        <ComposeReview ref="composer"
                       v-bind:introduction-text="introductionTexts[reviewTopic]"
                       v-bind:default-review="defaultReviews[reviewTopic]"
                       v-bind:show-intro="!numberOfStars"
                       v-on:review-changed="reviewTextChanged"/>
        <AnalyzeReview ref="analyzer"
                       v-bind:review-text="reviewTextToAnalyze"
                       v-on:analysisRequested="analysisRequested"
                       v-on:analysisCompleted="analysisCompleted"/>
      </section>
      <section v-show="numberOfStars" class="xd-section xd-light">
        <ExplainAnalysis ref="explainer"
                         v-bind:review-text="reviewTextToAnalyze"/>
      </section>
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
      infoLinkLabel: "Weitere Informationen",
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
    flex-direction: column;
  }

}

@media screen and (min-width: 450px) and (max-height: 650px) {

  #app {
    flex-direction: column;
    align-items: center;
  }

  main {
    width: 450px;
  }

}

@media screen and (min-width: 450px) and (min-height: 650px) {

  #app {
    flex-direction: column;
  }

}
</style>
