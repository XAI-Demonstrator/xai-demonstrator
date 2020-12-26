<template>
  <div id="app">
    <mt-header fixed title="Review Sentiment" class="navigation-header">
      <a href="/" slot="left">
        <mt-button icon="back"></mt-button>
      </a>
      <a href="./" slot="right">
        <mt-button><span style="font-size: 16px; font-weight:bold;">↻</span></mt-button>
      </a>
    </mt-header>
    <ComposeReview ref="composer"
                   v-bind:introduction-text="introductionTexts[reviewTopic]"
                   v-bind:default-review="defaultReviews[reviewTopic]"
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
        'movie': 'Wie war der Film, den Sie zuletzt gesehen haben?',
        'restaurant': 'Bewerten Sie bitte kurz Ihren letzten Restaurant-Besuch:',
        'travel': 'Wie hat Ihnen Ihre letzte Reise gefallen?'
      },
      defaultReviews: {
        'movie': 'Die Story war ziemlich vorhersehbar, würde ich nicht empfehlen...',
        'restaurant': 'Super Pizza und schneller Service - gerne bald wieder!!',
        'travel': 'Der Zug kam natürlich zu spät, aber die Aussicht war einmalig!'
      },
      reviewText: '',
      numberOfStars: null,
      reviewTopic: ['movie', 'restaurant', 'travel'][Math.floor(Math.random() * 3)]
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
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

@media screen and (min-width: 500px) {
  #app {
    margin: 60px auto auto;
    max-width: 500px;
    border: 1px solid #2c3e50;
    padding: 5px;
  }

  .navigation-header {
    margin: auto;
    max-width: 512px;
  }
}
</style>
