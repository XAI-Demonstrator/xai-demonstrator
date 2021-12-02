<template>
      <a v-if="url" v-bind:href="url" aria-label="Visit the XAI Studio" class="studio-logo">
        <img svg-inline src="../assets/xai-studio-logo.svg" aria-hidden="true" class="studio-logo" />
      </a>
</template>

<script>
export default {
  name: "XAIStudioRibbon",
  props: {
    url: {
      type: String,
      default: ""
    }
  }
}
</script>

<style scoped>
.studio-logo {
  position: fixed;
  bottom: 10px;
  right: 10px;
  border: 0;
}

@media screen and (max-width: 450px) {
  .studio-logo {
    display: none;
  }
}

@media screen and (min-width: 450px) and (max-height: 825px) {
  .studio-logo {
    display: none;
  }
}

@media screen and (min-width: 450px) and (min-height: 825px) {
  .studio-logo {
    display: inline;
  }
}
</style>