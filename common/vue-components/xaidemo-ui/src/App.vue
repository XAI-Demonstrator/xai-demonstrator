<template>
  <div id="app">
  <UseCaseHeader/>
  <FloatingInfoButton/>
  </div>
</template>

<script>
import UseCaseHeader from "@/components/UseCaseHeader";
import FloatingInfoButton from "@/components/FloatingInfoButton";

export default {
  name: "App",
  components: {FloatingInfoButton, UseCaseHeader}
}
</script>

<style>
* {
  box-sizing: border-box;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}

@media screen and (min-width: 450px) {
  body {
    background-color: #FFFFFF;
  }

  #app {
    margin: 40px auto auto;
    max-width: 425px;
    border: 1px solid #D3E3FC;
    padding: 1em 5px 5px;
  }
}
</style>