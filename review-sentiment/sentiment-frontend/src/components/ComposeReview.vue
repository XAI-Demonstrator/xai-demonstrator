<template>
  <div>
    <p v-if="showIntro && !text" class="intro-text">{{ introductionText }} Gebe deine Bewertung ein oder nutze das Beispiel:</p>
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

p {
  margin-block-start: 0;
}

.intro-text {
  text-align: left;
  font-size: 1em;
}

.text-input {
  width: 100%;
  outline: none;
  border: 1px solid #77A6F7;
}

.text-input:focus {
  border-color: #00887a;
}
</style>
