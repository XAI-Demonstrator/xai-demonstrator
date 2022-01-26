<template>
  <div id="app" class="xd-app">
    <GitHubRibbon url="https://github.com/xai-demonstrator/xai-demonstrator"/>
    <XAIStudioRibbon url="https://www.xai-studio.de"/>
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
import {FloatingInfoButton, UseCaseHeader, XAIStudioRibbon, GitHubRibbon} from "@xai-demonstrator/xaidemo-ui";
import axios from "axios";

export default {
  name: 'App',
  components: {
    ComposeReview,
    AnalyzeReview,
    ExplainAnalysis,
    FloatingInfoButton,
    UseCaseHeader,
    XAIStudioRibbon,
    GitHubRibbon
  },
  data() {
    return {
      useCaseTitle: this.$t('title'),
      introductionTexts: {
        'movie': this.$t('movie-prompt'),
        'travel': this.$t('travel-prompt')
      },
      defaultReviews: {
        'movie': this.$t('movie-example'),
        'travel': this.$t('travel-example')
      },
      infoText: [
        {
          headline: this.$t('title'),
          paragraphs: [this.$t('info1paragraph1'), this.$t('info1paragraph2')]
        },
        {
          headline: this.$t('info2headline'),
          paragraphs:  [this.$t('info2paragraph1'), this.$t('info2paragraph2'), this.$t('info2paragraph3')]
        }
      ],
      infoUrl: "https://www.erklaerbare-ki.de/xai-demonstrator/",
      infoLinkLabel: this.$t('infoLinkLabel'),
      reviewText: '',
      numberOfStars: null,
      reviewTopic: ['movie', 'travel'][Math.floor(Math.random() * 2)],
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
    document.title = this.useCaseTitle + " – XAI-Demonstrator"
  },
  async mounted() {
    await axios.get(this.backendUrl + '/load')
        .then()
        .catch(error => {
          console.log(error)
        })
  }
}
</script>

<i18n>
{
  "de": {
    "title": "Stimmung erkennen",
    "movie-prompt": "Wie war der Film, den du zuletzt gesehen hast?",
    "movie-example": "Die Story war ziemlich vorhersehbar, würde ich nicht empfehlen...",
    "travel-prompt": "Wie hat dir deine letzte Reise gefallen?",
    "travel-example": "Der Zug kam natürlich zu spät, aber die Aussicht war einmalig!",
    "info1paragraph1": "Du interagierst mit einer KI, die anhand eines Bewertungstexts vorhersagt, wie viele Sterne das bewertete Produkt erhält. Aber eine KI ist nie perfekt!",
    "info1paragraph2": "XAI hilft dir, die Einschätzung der KI und ihre Zuverlässigkeit besser zu bewerten.",
    "info2headline": "Was steckt dahinter?",
    "info2paragraph1": "Die KI baut auf dem von Google entwickelten BERT-Modell auf und ordnet einem Text einem bis fünf Sterne zu, je nachdem, wie negativ bzw. positiv die Bewertung ausfällt.",
    "info2paragraph2": "Die Erklärungen werden mit Hilfe von gradientenbasierten XAI-Methoden erzeugt, die den Einfluss einzelner Silben und Wörter auf das Endresultat ermitteln.",
    "info2paragraph3": "<small>Modell: <a href='https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment'>NLPTown bert-base-multilingual-uncased-sentiment</a> via <a href='https://huggingface.co/models'>Hugging Face Model Hub</a>, Erklärungen: <a href='https://captum.ai/'>Captum</a></small>",
    "infoLinkLabel": "Interesse geweckt? Hier gibt’s mehr Infos!"
  },
  "en": {
    "title": "Sentiment Analysis",
    "movie-prompt": "What did you think about the latest movie you watched?",
    "movie-example": "The story was pretty predictable, wouldn't recommend it...",
    "travel-prompt": "Did you enjoy your last trip?",
    "travel-example": "Of course, the train was late, but the view was spectacular!",
    "info1paragraph1": "You're interacting with an AI that based on a text can predict how many stars the reviewed product will receive. But an AI is never perfect!",
    "info1paragraph2": "XAI helps you to understand the AI's decision and assess its reliability.",
    "info2headline": "What's going on behind the scenes?",
    "info2paragraph1": "The AI is based on Google's BERT model and assigns a number of stars based on how negative or positive the sentiment of the review is.",
    "info2paragraph2": "The explanations are generated using gradient-based XAI methods that determine the influence of individual syllables and words on the AI's assessment.",
    "info2paragraph3": "<small>Model: <a href='https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment'>NLPTown bert-base-multilingual-uncased-sentiment</a> via <a href='https://huggingface.co/models'>Hugging Face Model Hub</a>, Explanations: <a href='https://captum.ai/'>Captum</a></small>",
    "infoLinkLabel": "Want to learn more? (in German)"
  }
}
</i18n>

<style>
#app {
  display: flex;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
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
