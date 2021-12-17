<template>
  <div id="app" class="xd-app">
    <GitHubRibbon url="https://github.com/xai-demonstrator/xai-demonstrator"/>
    <XAIStudioRibbon url="https://www.xai-studio.de"/>
    <UseCaseHeader
        v-bind:standalone="!Boolean(backendUrl)"
        v-bind:title="useCaseTitle"/>
    <main>
      <section class="xd-section xd-light">
        {{ msg }}
        <p>Your Score: {{ score_user }} and AI Score: {{ score_ai }}</p>
      </section>
      <section class="xd-section xd-light">
        <img class="xd-border-secondary" :src="url"/>
      </section>
      <section style="display: none; align-content: flex-end;    flex-wrap: wrap;    align-items: baseline;"
               class="xd-section xd-light" id="legend">
        <ul class="legend">
          <li><span class="positiv"></span> {{ prediction }}</li>
          <li><span class="negativ"></span> {{ other }}</li>
        </ul>
      </section>
      <section class="xd-section xd-light" id="radio"
               style="display: flex;    align-content: flex-end;    flex-wrap: wrap;    align-items: baseline;">
        <input type="radio" id="Tel-Aviv" name="City" value="Tel-Aviv" checked>
        <label for="Tel-Aviv">Tel-Aviv</label>
        <input type="radio" id="Berlin" name="City" value="Berlin">
        <label for="Berlin">Berlin</label>
        <button type="button" class="xd-button xd-secondary" style="width:auto; margin-left: auto;"
                v-on:click="answer()">Was I right?
        </button>
      </section>
      <button style="display: none;" type="button" class="xd-button xd-secondary" id="explain" v-on:click="explain()">
        Explain it to me
      </button>
      <button style="display: none;" type="button" class="xd-button xd-secondary" id="new" v-on:click="restart()">Start
        again
      </button>
      <button type="button" class="xd-button xd-secondary" id="submit" v-on:click="submitFile()">What the AI says
      </button>
          <SpinningIndicator class="indicator" v-bind:visible="waitingForExplanation"/>

    </main>
    <FloatingInfoButton
      v-bind:info-text="infoText"
      v-bind:info-url="infoUrl"
      v-bind:link-label="linkLabel"/>
  </div>
</template>

<script>
import axios from 'axios'
import {UseCaseHeader, FloatingInfoButton, SpinningIndicator, XAIStudioRibbon, GitHubRibbon} from '@xai-demonstrator/xaidemo-ui'

export default {
  name: 'App',
  components: {
    UseCaseHeader,
    FloatingInfoButton,
    SpinningIndicator,
    GitHubRibbon,
    XAIStudioRibbon
  },
  data() {
    return {
      useCaseTitle: 'Guess the country',
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      prediction: 'Israel',
      other: 'Germany',
      score_ai: 0,
      score_user: 0,
      msg: '',
      url: '',
      waitingForExplanation: false,
      infoUrl: 'https://xai-demonstrator.github.io/#use-case-ii',
      infoLinkLabel: 'Interesse geweckt? Hier gibt’s mehr Infos!',
      infoText: [
        {
          headline: 'Gegenstände erkennen',
          paragraphs: [
            'Du interagierst mit einer KI, die einen Gegenstand in einem Bildausschnitt erkennen kann. Aber eine KI ist nie perfekt!',
            'Durch die Wahl verschiedener Bildausschnitte entdeckst du, für welche Bereiche die KI zuverlässig ist, aber insbesondere auch, wo sie an ihre Grenzen stößt.',
            'Die automatisch erzeugten Erklärungen helfen dir, zu verstehen, wie die KI vorgeht und warum sie manchmal falsche Schlüsse zieht.'

          ]
        }, {
          headline: 'Was steckt dahinter?',
          paragraphs: [
            'Die KI ist ein tiefes neuronales Netz, das 1000 verschiedene Objekte erkennen kann.',
            'Die Erklärungen werden mit der XAI-Methode <em><abbr>LIME</abbr></em> (<strong>L</strong>ocal <strong>I</strong>nterpretable <strong>M</strong>odel-Agnostic <strong>E</strong>xplanations) generiert. Die Erklärung entspricht einer graphischen Hervorhebung von Bildbereichen, die für die Entscheidung der KI besonders relevant sind.',
            "<small>Modell: Neuronales Netz auf Basis von <a href='https://www.tensorflow.org/api_docs/python/tf/keras/applications/mobilenet_v2'>MobileNetV2 for Keras</a>, Erklärungen: <a href='https://github.com/marcotcr/lime'>LIME</a><br />Bild: Melinda Pack (Unsplash), <a href='https://creativecommons.org/publicdomain/zero/1.0/deed.en'>CC0</a> 1.0, via <a href='https://commons.wikimedia.org/wiki/File:Camera_keys_notebook_coffee_(Unsplash).jpg'>Wikimedia Commons</a></small>"
          ]
        }]
    }
  },
  async created() {
    if (document.cookie === '') {
      document.cookie = 'AI=' + this.score_ai + '; Secure'
      document.cookie = 'User=' + this.score_user + '; Secure'
    } else {
      this.score_ai = parseInt(document.cookie.split('; ')
        .find(row => row.startsWith('AI='))
        .split('=')[1])

      this.score_user = parseInt(document.cookie.split('; ')
        .find(row => row.startsWith('User='))
        .split('=')[1])
    }
    console.log(document.cookie)
    this.getMessage()
    this.getStreetview()
  },
  methods: {
    getMessage() {
      axios.get('/msg')
        .then((res) => {
          this.msg = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getStreetview() {
      axios.get('/streetview')
        .then((res) => {
          this.url = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
    submitFile() {
      var result
      this.waitingForExplanation = true
      if (this.url.search('Israel') === -1) {
        result = 'Berlin'
      } else {
        result = 'Tel-Aviv'
      }
      // const config = { headers: {'Content-Type': 'application/json'} };
      axios.post('/predict/image3/?url=' + this.url).then((res) => {
        this.prediction = res.data[0]
        if (result === res.data[0]) {
          this.score_ai = parseInt(document.cookie.split('; ')
            .find(row => row.startsWith('AI='))
            .split('=')[1])
          this.score_ai = this.score_ai + 1

          document.cookie = 'AI=' + this.score_ai + '; Secure'
          console.log(document.cookie)
         /* notify({
            group: 'foo',
            title: 'Success',
            text: 'The AI predicted: ' + res.data[0] + ' and it was actually taken in ' + result
          }, 5000) */
        } else {
       /*   notify({
            group: 'bottom',
            title: 'Wrong',
            text: 'The AI predicted: ' + res.data[0] + ' and it was actually taken in ' + result
          }, 5000) */
        }

        document.getElementById('radio').style.display = 'none'
        document.getElementById('explain').style.display = 'block'
        document.getElementById('submit').style.display = 'none'

        this.waitingForExplanation = false
      })
        .catch((error) => {
          console.error(error)
        })
    },
    explain() {
      this.waitingForExplanation = true
      axios.post('/predict/explain2/?url=' + this.url).then((res) => {
        this.url = res.data

        if (this.prediction === 'Tel-Aviv') {
          this.other = 'Berlin'
        } else {
          this.other = 'Tel-Aviv'
        }
        document.getElementById('explain').style.display = 'none'
        document.getElementById('submit').style.display = 'none'
        document.getElementById('new').style.display = 'block'
        document.getElementById('legend').style.display = 'flex'
        this.waitingForExplanation = false
      })
        .catch((error) => {
          console.error(error)
        })
    },
    restart() {
      axios.post('/restart?url=' + this.url).then((res) => {
        document.getElementById('legend').style.display = 'none'
        document.getElementById('explain').style.display = 'none'
        document.getElementById('submit').style.display = 'block'
        document.getElementById('new').style.display = 'none'
        this.url = ''
        this.msg = res.data
        window.location.reload()
      })
        .catch((error) => {
          console.error(error)
        })
    },

    answer() {
      var answer
      if (document.getElementById('Tel-Aviv').checked === true) {
        answer = 'Tel-Aviv'
      } else {
        answer = 'Berlin'
      }

      var result
      if (this.url.search('Israel') === -1) {
        result = 'Berlin'
      } else {
        result = 'Tel-Aviv'
      }
      if (result === answer) {
        this.score_user = parseInt(document.cookie.split('; ')
          .find(row => row.startsWith('User='))
          .split('=')[1])
        this.score_user = this.score_user + 1
        document.cookie = 'User=' + this.score_user + '; Secure'
/*
        notify({
          group: 'foo',
          title: 'Success',
          text: 'The picture was taken in ' + result
        }, 3000) */
      } else {
   /*     notify({
          group: 'bottom',
          title: 'Wrong',
          text: 'The picture was taken in ' + result
        }, 3000) */
      }
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
  position: relative;
  overflow: hidden;
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

.alert {
  width: 100%;
}

img {
  width: 100%;

}

.btn {
  margin-top: 10px;
}

.legend {
  list-style: none;
}

.legend span {
  border: 1px solid #ccc;
  float: left;
  width: 12px;
  height: 12px;
  margin: 2px;
}

.legend .negativ {
  background-color: #fe5e55;
}

.legend .positiv {
  background-color: #63fe45;
}
</style>
