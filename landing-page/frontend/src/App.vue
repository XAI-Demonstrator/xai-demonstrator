<template>
  <div id="app">
    <div class="blank-header"><h1>XAI Demonstrator</h1></div>
    <header>
      <h3>Hinterfrage die KI und entdecke Erklärbare Künstliche Intelligenz</h3>
    </header>
    <main>
      <div id="select">
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
          <FloatingInfoButton
        v-bind:info-text="infoText"
        v-bind:info-url="infoUrl"
        v-bind:link-label="linkLabel"/>
    </main>

  </div>
</template>

<script>
import { FloatingInfoButton } from '@xai-demonstrator/xaidemo-ui';

export default {
  name: 'App',
  components: {
    FloatingInfoButton
  },
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
      ],
      infoText: [
        {
          headline: "Der XAI-Demonstrator",
          paragraphs: [
            "Eine KI, die sich dir gegenüber wie ein Team-Mitglied erklärt? Der XAI-Demonstrator zeigt, wie das geht.",
            "Anhand leicht zugänglicher Beispiele veranschautlicht die App die Möglichkeiten von Explainable AI (XAI). " +
            "Live und interaktiv erzeugt sie Erklärungen mit modernen Methoden direkt aus der Forschung.",
            "Damit wird die Vision einer Künstlichen Intelligenz, die nicht länger eine Black Box ist, " +
            "sondern von ihren Nutzerinnen und Nutzern verstanden und hinterfragt werden kann, Realität."
          ]
        }
      ],
      infoUrl: "https://www.uni-ulm.de",
      linkLabel: "Interesse geweckt? Besuche unsere Website!"
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
  height: 100vh;
  width: 100vw;
  display: flex;
}

.blank-header {
  background-color: #77A6F7;
  height: 50px;

  padding-left: 10px;
  display: flex;
  align-items: center;

  font-family: 'Calibri Light', sans-serif;
}

header {
  padding: 15px;
  background-color: #77A6F7;
  font-family: 'Calibri Light', sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  flex: 0;
  border-radius: 5px;
  box-shadow: 2px 2px 5px 2px #eee;
}

header h1, .blank-header h1 {
  color: #fff;
  padding: 0;
  margin: 0;
  font-weight: 400;
  font-size: 25px;
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

#select section {
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

@media screen and (max-width: 450px) {

  #app {
    padding: 60px 7px 7px;
    overflow: scroll;
    flex-direction: column;
  }

  .blank-header {
    top: 0;
    right: 0;
    left: 0;
    position: fixed;
    z-index: 1;
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

}


@media screen and (min-width: 450px) and (max-height: 650px) {
  #app {
    flex-direction: row;
    padding: 60px 7px 7px;
  }

  .blank-header {
    top: 0;
    right: 0;
    left: 0;
    position: fixed;
    z-index: 1;
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
    overflow: auto;
  }

  .blank-header {
    margin-bottom: 10px;
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

}
</style>
