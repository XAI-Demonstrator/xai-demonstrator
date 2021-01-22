<template>
  <div>
    <mt-button class="my-button" v-on:click="buttonClicked">Woran erkennst du das?</mt-button>
  </div>
</template>

<script>
export default {
  name: "ExplainInspection",
  methods: {
    buttonClicked() {
      this.$emit("explanationRequested")
    }
  }
}
</script>

<style scoped>
.my-button {
  background-color: #77A6F7;
  border-radius: 0;
  font-size: 1em;
  font-weight: normal;
  height: auto;
  padding: 10px;
}
</style>