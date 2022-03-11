<template>
  <div id="app" class="xd-app">
    <GitHubRibbon url="https://localhost/" />
    <XAIStudioRibbon url="https://www.xai-studio.de" />
    <UseCaseHeader title="UI Demo Use Case" v-bind:standalone="standalone" v-bind="study"/>
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
        <button class="xd-button xd-primary" v-on:click="waiting = !waiting">
          <label>Toggle Indicator</label>
        </button>
      </section>
      <section class="xd-section xd-light">
        <button class="xd-button xd-primary" v-on:click="extraSections += 1">
          <label>Add another section</label>
        </button>
      </section>
      <section class="xd-section xd-border-secondary">
        <p>Sometimes, we are just waiting...</p>
        <MultiBounce v-bind:umberOfDots="3" dot-class="xd-secondary"/>
      </section>
      <section class="xd-section xd-light">
        <h3>Section Headline</h3>
        <p>
          We also like to have a multi-paragraph text.
          It should be long.
        </p>
        <p>
          We need this to see how our scrolling behavior is.
          Otherwise, it is too difficult to test.
        </p>
      </section>
      <section v-for="sec in parseInt(extraSections)"
               class="xd-section xd-light" v-bind:key="sec">
        <p>This is section {{ sec }}!</p>
      </section>
    </main>
    <FloatingInfoButton/>
    <SpinningIndicator v-bind:visible="waiting"/>
  </div>
</template>

<script>
import UseCaseHeader from "@/components/UseCaseHeader";
import FloatingInfoButton from "@/components/FloatingInfoButton";
import SpinningIndicator from "@/components/SpinningIndicator";
import MultiBounce from "@/components/MultiBounce";
import GitHubRibbon from "@/components/GitHubRibbon";
import XAIStudioRibbon from "@/components/XAIStudioRibbon";

export default {
  name: "App",
  components: {XAIStudioRibbon, GitHubRibbon, MultiBounce, FloatingInfoButton, UseCaseHeader, SpinningIndicator},
  data: function () {
    return {
      standalone: true,
      waiting: false,
      extraSections: 0,
      study: false,
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
  background-color: silver;
}

#app {
  display: flex;
  justify-content: space-between;
  position: relative;
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
    flex-direction: column;
  }
}

@media screen and (min-width: 450px) and (min-height: 650px) {
  #app {
    flex-direction: column;
  }
}
</style>