<template>
  <div>
    <p v-on:click="reviewChanged" class="intro-text">{{ introductionText }}</p>
    <mt-field label="" v-bind:placeholder="defaultReview" type="textarea" rows="4" v-model="text"
              v-on:input="reviewChanged" class="text-input"></mt-field>
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
}

.text-input {
  border: 1px solid darkslategray;
}
</style>
