<template>
  <div id="app">
    <mt-header fixed title="Review Sentiment" class="navigation-header">
      <a href="/" slot="left" v-if="backendUrl">
        <mt-button icon="back"></mt-button>
      </a>
      <a href="./" slot="right">
        <mt-button><span style="font-size: 16px; font-weight:bold;">↻</span></mt-button>
      </a>
    </mt-header>
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
  </div>
</template>

<script>
import ComposeReview from "@/components/ComposeReview";
import AnalyzeReview from "@/components/AnalyzeReview";
import ExplainAnalysis from "@/components/ExplainAnalysis";


export default {
  name: 'App',
  components: {
    ComposeReview,
    AnalyzeReview,
    ExplainAnalysis
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}

.navigation-header {
  background-color: #77A6F7 !important;
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

  .navigation-header {
    margin: auto;
    max-width: 437px;
  }
}
</style>
