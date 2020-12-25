<template>
  <div>
    <p v-on:click="reviewChanged">{{ introductionText }}</p>
    <mt-field label="" v-bind:placeholder="defaultReview" type="textarea" rows="4" v-model="text"
              v-on:input="reviewChanged"></mt-field>
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
</style>
