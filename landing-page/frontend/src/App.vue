<template>
  <div id="app">
    <header>
      <h1>XAI-Demonstrator</h1>
      <h3>Entdecke Erklärbare Künstliche Intelligenz</h3>
    </header>
    <main>
      <a v-for="useCase in useCases" :key="useCase.title" v-bind:href="useCase.route">
        <section>
          <img v-bind:src="useCase.logo" class="logo" :alt="useCase.title"/>
          <div class="description">
            <h3>{{ useCase.title }}</h3>
            <p>{{ useCase.description }}</p>
          </div>
          <img class="next" src="https://upload.wikimedia.org/wikipedia/commons/7/7b/Octicons-playback-play.svg"/>
        </section>
      </a>
    </main>
    <footer>
      <p>Der XAI-Demonstrator ist ein Projekt der Universität Ulm.</p>
      <a href="/">?</a>
    </footer>
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
          logo: "https://upload.wikimedia.org/wikipedia/commons/1/11/Bon_article.svg",
          title: "Review Sentiment",
          description: "Wie bestimmt eine KI, wie viele Sterne eine Bewertung verdient?",
          route: "/sentiment/"
        },
        {
          logo: "https://upload.wikimedia.org/wikipedia/commons/c/c2/Android_Emoji_26c5.svg",
          title: "Visual Inspection",
          description: "Woran erkennt eine KI das Wetter? Finde es heraus!",
          route: "/inspection/"
        }
      ]
    }
  },
  created() {
    document.title = "XAI Demonstrator"
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
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #fff;
  padding: 15px 7px 7px;
  height: 100vh;
  overflow: scroll;
  display: flex;
  flex-direction: column;
}

header {
  padding: 15px;
  height: auto;
  min-height: 280px;
  background-color: #77A6F7;
  font-family: 'Calibri Light', sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex: 0;
}

header h1 {
  color: #fff;
  padding: 0;
  margin: 0;
  font-weight: 400;

}

header h3 {
  color: #fff;
  padding: 0;
  margin: 0;
  font-weight: 400;
}

main {
  display: flex;
  flex-direction: column;
  flex: 1;
}

main a {
  text-decoration: none;
  color: inherit;
  display: block;
  margin-top: 15px;
}

section {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  padding: 15px 10px;
  background-color: #D3E3FC;
}

section img {
  flex-shrink: 0;
  flex-grow: 0;
}

section img.logo {
  height: 60px;
  width: 60px;
  background-color: #00887A;
  border-radius: 30px;
}

section img.next {
  height: 50px;
  width: 15px;
}

.description {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  flex-grow: 1;
  padding: 0 15px 10px
}

.description h3 {
  margin: 0;
  padding: 0;
  font-size: 1em;
  font-weight: 600;
}

.description p {
  margin: 0;
  font-size: 0.8em;
  padding: 2px 0 0;
}

footer {
  margin-top: 15px;
  flex: 0;
  display: flex;
  flex-direction: row;
  align-items: flex-end;
  justify-content: space-between;
}

footer p {
  font-size: 0.7em;
  padding-right: 15px;
  color: #ccc;
  font-family: 'Calibri Light', sans-serif;
}

footer a {
  height: 70px;
  width: 70px;
  border-radius: 35px;
  flex-shrink: 0;
  flex-grow: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #77A6F7;
  text-decoration: none;
  color: #fff;
  font-size: 3em;
  font-weight: 400;
}

@media screen and (min-width: 450px) {
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
    border: 5px solid #D3E3FC;
    padding: 10px;
    height: auto;
    min-height: 640px;
    overflow: visible;
  }

}
</style>
