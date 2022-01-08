<template>
  <div id="app" class="xd-app">
    <GitHubRibbon url="https://github.com/xai-demonstrator/xai-demonstrator"/>
    <XAIStudioRibbon url="https://www.xai-studio.de"/>
    <div class="blank-header xd-primary"><h1>{{ $t('xaidemonstrator') }} <span class="beta-label">Beta</span></h1>
    </div>
    <header class="xd-secondary">
      <img v-bind:src="require('@/assets/logo-white.svg')" class="main-logo"/>
      <h3>{{ $t('claim') }}</h3>
    </header>

    <main>
      <div id="select">
        <a v-for="useCase in useCases" :key="useCase.title" v-bind:href="useCase.route">
          <section class="xd-section xd-light">
            <img v-bind:src="useCase.logo" class="logo xd-secondary" :alt="useCase.title"/>
            <div class="description">
              <h3>{{ $t(useCase.title) }}</h3>
              <p>{{ $t(useCase.description) }}</p>
            </div>
            <img class="next" v-bind:src="require('@/assets/arrow-right.svg')"/>
          </section>
        </a>
      </div>

    </main>
    <FloatingInfoButton
        v-bind:info-text="infoText"
        v-bind:info-url="infoUrl"
        v-bind:link-label="linkLabel"/>
  </div>
</template>

<script>
import {FloatingInfoButton} from '@xai-demonstrator/xaidemo-ui';
import {GitHubRibbon} from '@xai-demonstrator/xaidemo-ui';
import {XAIStudioRibbon} from '@xai-demonstrator/xaidemo-ui';

export default {
  name: 'App',
  components: {
    FloatingInfoButton, GitHubRibbon, XAIStudioRibbon
  },
  data() {
    return {
      infoText: [
        {
          headline: this.$t('info1headline'),
          paragraphs: [this.$t('info1paragraph1'), this.$t('info1paragraph2'), this.$t('info1paragraph3')]
        }
      ],
      infoUrl: "https://www.erklaerbare-ki.de/xai-demonstrator/",
      linkLabel: this.$t('infoLinkLabel')
    }
  },
  computed: {
    useCases() {
      return this.$appConfig.useCases.filter(useCase => useCase.include)
    }
  },
  created() {
    document.title = this.$t('xaidemonstrator');
  }
}
</script>

<i18n src="./use-cases.json"></i18n>
<i18n>
{
  "de": {
    "claim": "Hinterfrage die KI und entdecke Erklärbare Künstliche Intelligenz",
    "info1headline": "Der XAI-Demonstrator",
    "info1paragraph1": "Eine KI, die sich dir gegenüber wie ein Team-Mitglied erklärt? Der XAI-Demonstrator zeigt, wie das geht.",
    "info1paragraph2": "Anhand leicht zugänglicher Beispiele veranschaulicht die App die Möglichkeiten von Explainable AI (XAI). Live und interaktiv erzeugt sie Erklärungen mit modernen Methoden direkt aus der Forschung.",
    "info1paragraph3": "Damit wird die Vision einer Künstlichen Intelligenz, die nicht länger eine Black Box ist, sondern von ihren Nutzerinnen und Nutzern verstanden und hinterfragt werden kann, Realität.",
    "infoLinkLabel": "Interesse geweckt? Besuche unsere Website!"
  },
  "en": {
    "claim": "Scrutinize the AI and discover Explainable Artificial Intelligence",
    "info1headline": "The XAI Demonstrator",
    "info1paragraph1": "An AI that acts like a team member and explains its decisions and actions? The XAI Demonstrator shows that it's possible.",
    "info1paragraph2": "Using accessible examples, the app demonstrates the potential of Explainable AI (XAI). All explanations are generated in real time using state-of-the-art XAI methods.",
    "info1paragraph3": "The XAI Demonstrator brings the vision of an AI that is no longer a black box to reality, allowing its users to fully comprehend and challenge its decisions.",
    "infoLinkLabel": "Want to learn more? (in German)"
  }
}
</i18n>

<style>

#app {
  display: flex;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

.blank-header {
  height: 42px;

  padding-left: 12px;
  display: flex;
  align-items: center;
  font-family: 'Calibri Light', sans-serif;
  box-shadow: 0 4px 12px rgba(120, 120, 120, 0.4);
}

.beta-label {
  font-weight: 400;
  font-size: 18px;
  font-variant: all-small-caps;
}

header {
  padding: 10px;
  font-family: 'Calibri Light', sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  flex: 0;
  border-radius: 3px;
  box-shadow: 2px 2px 4px rgba(180, 180, 180, 0.5);
}

header h1, .blank-header h1 {
  color: #EBEBEB;
  padding: 0;
  margin: 0;
  font-weight: 400;
  font-size: 25px;
}

header h2 {
  color: #EBEBEB;
  padding: 0;
  margin: 0;
  font-weight: 400;
  font-size: 35px;
  float: left;
}

header h3 {
  color: #EBEBEB;
  padding: 0;
  margin: 0;
  font-weight: 400;
  align-items: center;
}

.main-logo {
  width: 50%;
  margin-bottom: 1vh;
}

#select {
  display: flex;
  flex-direction: column;
}

#select a {
  color: #323232;
  text-decoration: none;
  display: block;
}

#select a:visited {
  color: #323232;
}

#select section {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
}

section img {
  flex-shrink: 0;
  flex-grow: 0;
}

section img.logo {
  height: 60px;
  width: 60px;
  border-radius: 100%;
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
    min-height: 38.2vh;
  }

  main {
    flex: 1;
  }

  #select a {
    margin-top: 12px;
  }

}


@media screen and (min-width: 450px) and (max-height: 650px) {
  #app {
    flex-direction: row;
    padding-right: 0;
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
    min-width: 38.2vw;
  }

  main {
    flex-shrink: 1;
    flex-grow: 1;
    overflow: scroll;
    padding-left: 8px;
    padding-right: 8px;
  }

  #select a {
    margin: 0 0 12px;
  }

}


@media screen and (min-width: 450px) and (min-height: 650px) {

  #app {
    flex-direction: column;
  }

  .blank-header {
    margin-bottom: 14px;
  }

  header {
    height: auto;
    margin-left: 4px;
    margin-right: 4px;
  }

  main {
    flex: 1;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
  }

  #select a {
    margin-top: 12px;
  }

}
</style>
