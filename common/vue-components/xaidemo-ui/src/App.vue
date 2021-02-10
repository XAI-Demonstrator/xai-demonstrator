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
  #app {
    padding: 60px 7px 7px;
    overflow: scroll;
    flex-direction: column;
  }
}

@media screen and (min-width: 450px) and (max-height: 650px) {
  #app {
    flex-direction: row;
    padding: 60px 7px 7px;
  }
}

@media screen and (min-width: 450px) and (min-height: 650px) {

  body {
    background-color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100vw;
    height: 100vh;
  }

  #app {
    max-width: 450px;
    border: 1px solid #ddd;
    box-shadow: 2px 2px 5px 2px #eee;
    padding: 7px;
    height: auto;
    min-height: 640px;
    flex-direction: column;
  }
}

</style>