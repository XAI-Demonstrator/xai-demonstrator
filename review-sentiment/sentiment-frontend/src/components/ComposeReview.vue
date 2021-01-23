<template>
  <div>
    <p v-if="showIntro" class="intro-text">{{ introductionText }} Gebe deine Bewertung ein oder nutze das Beispiel:</p>
    <mt-field label=""
              v-bind:placeholder="defaultReview"
              type="textarea" rows="3" v-model="text"
              v-on:input="reviewChanged"
              class="text-input" id="review-input-field"></mt-field>
  </div>
</template>
<script>
export default {
  name: 'ComposeReview',
  data() {
    return {
      text: ''
    }
  },
  props: [
    "introductionText",
    "defaultReview",
    "showIntro"
  ],
  methods: {
    reviewChanged() {
      this.$emit('reviewChanged', this.text)
    }
  }
}
</script>
<style scoped>
p {
  margin-block-start: 0;
}
.intro-text {
  text-align: left;
  padding-left: 5px;
  padding-right: 5px;
  font-size: 1em;
}

.text-input {
  border: 1px solid #D3E3FC;
}
</style>
