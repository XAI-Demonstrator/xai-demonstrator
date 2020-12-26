<template>
  <div>
    <mt-button type="primary" size="large" v-on:click="toggleButton">Im a button</mt-button>
  </div>
</template>

<script>
export default {
  name: "InspectImage",
  methods: {
    toggleButton() {
      this.$emit("buttonClicked")
    }
  }
}
</script>

<style scoped>

</style>