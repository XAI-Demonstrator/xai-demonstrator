<template>
  <div id="app">
    <mt-header fixed title="XAI Demonstrator" class="navigation-header">
    </mt-header>
    <mt-cell v-for="useCase in useCases" :key="useCase.title" :title="useCase.title" :label=useCase.label is-link :to=useCase.route></mt-cell>
  </div>
</template>

<script>

export default {
  name: 'App',
  components: {},
  data() {
    return {
      useCases: [
        {
          title: "Review Sentiment",
          label: "Customer Review Sentiment",
          route: "/sentiment/"
        },
        {
          title: "Visual Inspection",
          label: "Visual Inspection Use Case",
          route: "/inspection/"
        }]
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}

.navigation-header {
  background-color: #77A6F7 !important;
}

@media screen and (min-width: 450px) {
  body {
    background-color: #FFFFFF;
  }

  #app {
    margin: 40px auto auto;
    max-width: 425px;
    border: 1px solid #D3E3FC;
    padding: 5px;
  }

  .navigation-header {
    margin: auto;
    max-width: 437px;
  }
}
</style>
