<template>
  <div class="navigation-header">
    <div class="header-icon"><a href="/" v-if="!standalone">❮</a></div>
    <div class="header-title">{{ title }}</div>
    <div class="header-icon"><a v-bind:href="reloadUrl">↻</a></div>
  </div>
</template>

<script>
export default {
  name: "UseCaseHeader",
  props: {
    standalone: {
      type: Boolean,
      default: false
    },
    title: {
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
  background-color: #77A6F7;
  height: 50px;

  top: 0;
  right: 0;
  left: 0;
  position: fixed;
  z-index: 1;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;

  padding-left: 5px;
  padding-right: 5px;
}

.header-icon {
  width: 50px;
  height: 50px;
  flex-grow: 0;
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: space-around;
}

.header-icon a {
  text-decoration: none;
  color: white;
  font-size: 25px;
}

.header-icon a:visited {
  color: white;
}

.header-icon a:hover {
  color: white;
}

.header-title {
  color: white;
  font-size: 18px;
  font-weight: 400;
}

@media screen and (min-width: 450px) {
  .navigation-header {
    margin: auto;
    max-width: 437px;
  }
}
</style>