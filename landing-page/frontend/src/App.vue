<template>
  <div id="app">
    <header v-on:click="toMainMode">
      <h1>XAI-Demonstrator</h1>
      <h3>Hinterfrage die KI und entdecke Erklärbare Künstliche Intelligenz</h3>
    </header>
    <main>
      <transition name="fade" mode="out-in">
        <div id="select" v-if="!infoMode" key="select">
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
        </div>
        <div v-else id="info" key="info">
          <section>
            <div class="description">
              <h3>Der XAI-Demonstrator</h3>
              <p>
                Eine KI, die sich dir gegenüber wie ein Team-Mitglied erklärt?
                Der XAI-Demonstrator zeigt, wie das geht.
              </p>
              <p>
                Anhand leicht zugänglicher Beispiele veranschautlicht die App die Möglichkeiten von
                Explainable AI (XAI).
                Live und interaktiv erzeugt sie Erklärungen mit modernen Methoden direkt aus der Forschung.
              </p>
              <p>
                Damit wird die Vision einer Künstlichen Intelligenz, die nicht länger eine Black Box ist,
                sondern von ihren Nutzerinnen und Nutzern verstanden und hinterfragt werden kann, Realität.
              </p>
              <a class="button" href="https://www.uni-ulm.de">Interesse geweckt? Besuche unsere Website!</a>
            </div>
          </section>
        </div>
      </transition>
    </main>
    <footer>
      <p>Der XAI-Demonstrator ist ein Projekt der Universität Ulm.</p>
      <transition name="fade" mode="out-in">
        <div v-if="!infoMode" class="icon" v-on:click="toInfoMode" key="infoButton">i</div>
        <div v-else class="icon close" v-on:click="toMainMode" key="mainButton">&#215;</div>
      </transition>
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
        },
        // {
        //   logo: "https://upload.wikimedia.org/wikipedia/commons/c/c2/Android_Emoji_26c5.svg",
        //   title: "Visual Inspection",
        //   description: "Woran erkennt eine KI das Wetter? Finde es heraus!",
        //   route: "/inspection/"
        // }
        // ,
        // {
        //   logo: "https://upload.wikimedia.org/wikipedia/commons/c/c2/Android_Emoji_26c5.svg",
        //   title: "Visual Inspection",
        //   description: "Woran erkennt eine KI das Wetter? Finde es heraus!",
        //   route: "/inspection/"
        // }
        // ,
        // {
        //   logo: "https://upload.wikimedia.org/wikipedia/commons/c/c2/Android_Emoji_26c5.svg",
        //   title: "Visual Inspection",
        //   description: "Woran erkennt eine KI das Wetter? Finde es heraus!",
        //   route: "/inspection/"
        // }
      ],
      infoMode: false
    }
  },
  created() {
    document.title = "XAI Demonstrator"
  },
  methods: {
    toInfoMode() {
      this.infoMode = true;
    },
    toMainMode() {
      this.infoMode = false;
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
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #fff;
  height: 100vh;
  width: 100vw;
  display: flex;
}

header {
  padding: 15px;
  background-color: #77A6F7;
  font-family: 'Calibri Light', sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex: 0;
  border-radius: 5px;
  box-shadow: 2px 2px 5px 2px #eee;
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

#select {
  display: flex;
  flex-direction: column;
}

#select a {
  text-decoration: none;
  display: block;
}

#select a:visited {
  color: #2c3e50;
}

section {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  padding: 15px 10px;
  background-color: #D3E3FC;
  border-radius: 5px;
  box-shadow: 2px 2px 5px 0 #eee;
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

section a.button {
  width: 100%;
  background-color: #00887A;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  border-radius: 5px;
  margin-top: 15px;
}

.description {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  align-self: stretch;
  flex-grow: 1;
  padding: 0 15px;
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
  padding: 5px 0 0;
  text-align: justify;
}

footer {
  display: flex;
  align-items: flex-end;
}

footer p {
  font-size: 0.7em;
  color: #ccc;
  font-family: 'Calibri Light', sans-serif;
  padding: 0;
  margin: 0;
}

footer div.icon {
  height: 60px;
  width: 60px;
  border-radius: 30px;
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
  box-shadow: 2px 2px 5px 3px #eee;
}

footer div.close {
  background-color: #CC0000;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .5s;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

@media screen and (max-width: 450px) {

  #app {
    padding: 15px 7px 7px;
    overflow: scroll;
    flex-direction: column;
  }

  header {
    height: auto;
    min-height: 280px;
  }

  main {
    flex: 1;
  }

  #select a {
    margin-top: 15px;
  }

  #info section {
    margin-top: 15px;
  }

  footer {
    margin-top: 15px;
    flex: 0;
    flex-direction: row;
    align-items: flex-end;
    justify-content: space-between;
  }

  footer p {
    padding-right: 15px;
  }

}


@media screen and (min-width: 450px) and (max-height: 650px) {
  #app {
    flex-direction: row;
    padding: 10px;
  }

  header {
    width: auto;
    min-width: 280px;
  }

  main {
    flex-shrink: 1;
    flex-grow: 1;
    overflow: scroll;
    padding: 0 5px 0 15px;
  }

  #select a {
    margin: 0 0 15px;
  }

  #info section {
    margin: 0 0 15px;
  }

  footer {
    flex-shrink: 2;
    flex-grow: 2;
    flex-direction: column-reverse;
    justify-content: flex-start;
    margin: 0;
  }

  footer p {
    display: none;
    padding-left: 15px;
    padding-right: 0;
    text-align: right;
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
    padding: 10px;
    height: auto;
    min-height: 640px;
    flex-direction: column;
  }

  header {
    height: auto;
    min-height: 280px;
  }

  main {
    flex: 1;
  }

  #select a {
    margin-top: 15px;
  }

  #info section {
    margin-top: 15px;
  }

  footer {
    margin-top: 15px;
    flex: 0;
    flex-direction: row;
    align-items: flex-end;
    justify-content: space-between;
  }

}
</style>
