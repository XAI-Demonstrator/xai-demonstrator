<template>
  <div>
    <p class="intro-text">{{ introductionText }}</p>
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
    "defaultReview"
  ],
  methods: {
    reviewChanged() {
      this.$emit('reviewChanged', this.text)
    }
  }
}
</script>
<style scoped>
.intro-text {
  text-align: left;
  padding-left: 5px;
  padding-right: 5px;
  font-size: 1em;
}

.text-input {
  border: 1px solid #77A6F7;
}
</style>
