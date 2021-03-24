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
import axios from "axios";

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
      useCaseTitle: "Stimmung erkennen",
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
          headline: "Stimmung erkennen",
          paragraphs: [
            "Du interagierst mit einer KI, die anhand eines Bewertungstexts vorhersagt, wie viele Sterne das bewertete Produkt erhält. Aber eine KI ist nie perfekt!",
            "XAI hilft dir, die Einschätzung der KI und ihre Zuverlässigkeit besser zu bewerten."
          ]
        },
        {
          headline: "Was steckt dahinter?",
          paragraphs: [
            "Die KI baut auf dem von Google entwickelten BERT-Modell auf und ordnet einem Text einem bis fünf Sterne zu, je nachdem, wie negativ bzw. positiv die Bewertung ausfällt.",
            "Die Erklärungen werden mit Hilfe von gradientenbasierten XAI-Methoden erzeugt, die den Einfluss einzelner Silben und Wörter auf das Endresultat ermitteln.",
            "<small>Modell: <a href='https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment'>NLPTown bert-base-multilingual-uncased-sentiment</a> via <a href='https://huggingface.co/models'>Hugging Face Model Hub</a>, Erklärungen: <a href='https://captum.ai/'>Captum</a></small>"
          ]
        }
      ],
      infoUrl: "https://xai-demonstrator.github.io/#use-case-i",
      infoLinkLabel: "Interesse geweckt? Hier gibt’s mehr Infos",
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
    document.title = this.useCaseTitle + " – XAI Demonstrator"
  },
  mounted() {
    axios.get(this.backendUrl + '/load')
        .then()
        .catch(error => {
          console.log(error)
        })
  }
}
</script>

<style>
#app {
  display: flex;
}

main {
  flex-grow: 1;
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