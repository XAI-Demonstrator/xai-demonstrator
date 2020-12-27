<template>
  <div>
    <mt-button type="primary" size="large" v-on:click="toggleButton" class="my-button">Ist das ein Hund?</mt-button>
  </div>
</template>

<script>
export default {
  name: "InspectImage",
  methods: {
    toggleButton() {
      this.$emit("buttonClicked")
    }
  },
  created() {
    document.title = "Visual Inspection – XAI Demonstrator"
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