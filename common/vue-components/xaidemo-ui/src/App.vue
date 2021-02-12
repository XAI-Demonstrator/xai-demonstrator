<template>
  <div id="app" class="xd-app">
    <UseCaseHeader title="UI Demo Use Case" v-bind:standalone="standalone"/>
    <main>
      <section class="xd-section xd-light">
        <p>So much content!</p>
      </section>
      <section class="xd-section xd-light">
        <button class="xd-button xd-secondary" v-on:click="standalone = !standalone">
          <label>Toggle Standalone</label>
        </button>
      </section>
      <section class="xd-section xd-border-primary">
        <button class="xd-button xd-primary" v-on:click="standalone = !standalone">
          <label>Toggle Standalone</label>
        </button>
      </section>
    </main>
    <FloatingInfoButton/>
  </div>
</template>

<script>
import UseCaseHeader from "@/components/UseCaseHeader";
import FloatingInfoButton from "@/components/FloatingInfoButton";

export default {
  name: "App",
  components: {FloatingInfoButton, UseCaseHeader},
  data: function () {
    return {
      standalone: true
    }
  }
}
</script>

<style>
* {
  box-sizing: border-box;
}

body {
  padding: 0;
  margin: 0;
}

#app {
  display: flex;
  justify-content: space-between;
}

main {
  flex-grow: 1;
}

@media screen and (max-width: 450px) {
  #app {
    flex-direction: column;
  }
}

@media screen and (min-width: 450px) and (max-height: 650px) {
  #app {
    flex-direction: row;
  }
}

@media screen and (min-width: 450px) and (min-height: 650px) {
  #app {
    flex-direction: column;
  }
}
</style>