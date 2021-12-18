<template>
  <div>
    <p v-if="showIntro && !text" class="intro-text">{{ introductionText }}</p>
    <p v-if="showIntro && !text" class="intro-text">Gib deine Bewertung ein oder nutze das Beispiel:</p>
    <textarea
        v-bind:placeholder="defaultReview"
        v-model="text"
        rows="4"
        class="text-input"
        id="review-input-field">
    </textarea>
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
  watch: {
    text: function () {
      this.$emit('review-changed', this.text)
    }
  }
}
</script>
<style scoped>
.intro-text {
  text-align: left;
}

.text-input {
  width: 100%;
  outline: none;
  border: none;
  border-radius: 5px;
  padding: 8px;
  margin-top: 8px;
  margin-bottom: 8px;
  font-size: 1em;
}

.text-input:focus {
  border-color: #00887a;
}
</style>
