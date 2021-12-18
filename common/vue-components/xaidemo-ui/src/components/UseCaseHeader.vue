<template>
  <div id="navigation-header" class="xd-primary">
    <div class="header-icon">
      <a href="/" v-if="!standalone || !embedded">
        <img svg-inline src="../assets/arrow-left.svg" alt="Back"/>
      </a>
    </div>
    <div class="header-title">{{ title }}</div>
    <div class="header-icon">
      <a v-bind:href="reloadUrl">
        <img svg-inline src="../assets/reload.svg" alt="Reload"/>
      </a>
    </div>
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
    },
    embedded() {
      const uri = window.location.search.substring(1);
      let params = new URLSearchParams(uri);
      return params.has("embedded")
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
  height: 42px;
  width: 50px;
  flex-grow: 0;
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon:first-child {
  padding-left: 8px;
}

.header-icon:last-child {
  padding-right: 8px;
}

.header-icon a {
  height: 100%;
  width: 100%;

  display: flex;
  align-items: center;
}

.header-icon:first-child a {
  justify-content: flex-start;
}

.header-icon:last-child a {
  justify-content: flex-end;
}

.header-icon svg {
  max-height: 28px;
  max-width: 28px;
}

.header-title {
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