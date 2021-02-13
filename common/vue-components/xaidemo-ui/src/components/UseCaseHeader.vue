<template>
  <div id="navigation-header" class="xd-primary">
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
      default: true
    },
    title: {
      type: String,
      default: ""
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
#navigation-header {
  height: 42px;

  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-between;

  box-shadow: 0 4px 12px rgba(120, 120, 120, 0.4);
}

.header-icon {
  width: 42px;
  height: 42px;
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

@media screen and (max-width: 450px) {
  #navigation-header {
    top: 0;
    right: 0;
    left: 0;
    position: fixed;
    z-index: 1;
  }
}

@media screen and (min-width: 450px) and (max-height: 650px) {
  #navigation-header {
    top: 0;
    right: 0;
    left: 0;
    position: fixed;
    z-index: 1;
  }
}

@media screen and (min-width: 450px) and (min-height: 650px) {
  #navigation-header {
    margin-bottom: 8px;
  }
}

</style>