<template>
  <mt-header fixed v-bind:title="title" class="navigation-header">
    <a href="/" slot="left" v-if="!standalone">
      <mt-button icon="back"></mt-button>
    </a>
    <a v-bind:href="reloadUrl" slot="right">
      <mt-button><span style="font-size: 16px; font-weight:bold;">↻</span></mt-button>
    </a>
  </mt-header>
</template>

<script>
import { Header } from 'mint-ui';

export default {
  name: "UseCaseHeader",
  components: [
      Header
  ],
  props: {
    standalone : {
      type: Boolean,
      default: true
    },
    title : {
      type: String,
      default: "Use Case"
    }
  },
  computed: {
    reloadUrl() {
      return "./" + window.location.search
    }
  }
}
</script>

<style scoped>
.navigation-header {
  background-color: #77A6F7 !important;
}

@media screen and (min-width: 450px) {
  .navigation-header {
    margin: auto;
    max-width: 437px;
  }
}
</style>