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
      <section v-show="user_answer"  class="xd-section xd-light">
        <p v-if="user_answer == label" >Your answer: {{user_answer}} is right</p>
        <p v-else>Your answer: {{user_answer}} is wrong, the right answer ist: {{label}}</p>
      </section>
      <section v-show="prediction"  class="xd-section xd-light">
        <p v-if="prediction == label" >The AI answer: {{prediction}} is right</p>
        <p v-else>The AI answer: {{prediction}} is wrong, the right answer ist: {{label}}</p>
      </section>
      <section class="xd-section xd-light">
        <img class="xd-border-secondary;" v-bind:src="this.streetviewimage"/>
      </section>
      <section  v-if="explanation" style="align-content: flex-end;    flex-wrap: wrap;    align-items: baseline;"
               class="xd-section xd-light" id="legend">
        <ul class="legend">
          <li><span class="positiv"></span> {{ prediction }}</li>
          <li><span class="negativ"></span> Other classes </li>
        </ul>
      </section>

      
      <section v-if="!user_answer" class="xd-section xd-light" id="radio"
               style="display: flex;    align-content: flex-end;    flex-wrap: wrap;    align-items: baseline;">
        
        <input type="radio" id="Tel Aviv" name="City" value="Tel Aviv" checked>
        <label for="Tel Aviv">Tel Aviv</label>
        <input type="radio" id="Berlin" name="City" value="Berlin">
        <label for="Berlin">Berlin</label>
        <input type="radio" id="Westjerusalem" name="City" value="Westjerusalem" checked>
        <label for="Westjerusalem">Westjerusalem</label>
        <input type="radio" id="Hamburg" name="City" value="Hamburg">
        <label for="Hamburg">Hamburg</label>
        <button type="button" class="xd-button xd-secondary" style="width:auto; margin-left: auto;"
                v-on:click="answer()">Was I right?
      </button>
      </section>
      <button v-if="prediction && explanation == null" type="button" class="xd-button xd-secondary" id="explain" v-on:click="explain()"> <!-- v-show --> 
        Explain it to me
      </button>
      <button v-if="explanation" type="button" class="xd-button xd-secondary" id="new" v-on:click="restart()">Start <!-- v-show --> 
        again
      </button>
      <button v-if="!prediction" type="button"  class="xd-button xd-secondary" id="submit" v-on:click="submitFile()">What the AI says
      </button>
          <SpinningIndicator class="indicator" v-bind:visible="waitingForExplanation"/>

    </main>
    <FloatingInfoButton
      v-bind:info-text="infoText"
      v-bind:info-url="infoUrl"
      v-bind:link-label="infoLinkLabel"/>
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
      explanation: null,
      prediction: null,
      label: null,
      user_answer: null,
      score_ai: 0,
      score_user: 0,
      msg: '',
      streetviewimage: null,
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
      document.cookie = 'AI=' + this.score_ai + '; Secure' //Cookies entfernen
      document.cookie = 'User=' + this.score_user + '; Secure'
    } else {
      this.score_ai = parseInt(document.cookie.split('; ')
        .find(row => row.startsWith('AI='))
        .split('=')[1])

      this.score_user = parseInt(document.cookie.split('; ')
        .find(row => row.startsWith('User='))
        .split('=')[1])
    }
    this.getMessage()
    this.getStreetview()
  },
  methods: {
    getMessage() {
      axios.get(this.backendUrl + '/msg')
        .then((res) => {
          this.msg = res.data.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getStreetview() {
      axios.get(this.backendUrl +'/streetview')
       .then(res => {
          this.streetviewimage = res.data.image
          this.label = res.data.class_label
          })
          .catch(error => {
            console.log(error)
          }) 
    },
    submitFile() {
      this.waitingForExplanation = true
      const blob = new Blob([this.streetviewimage]);

      let form = new FormData();
      form.append('file', blob );

      axios.post(this.backendUrl +'/predict', form, {
              headers: {
                    'Content-Type': 'multipart/form-data'
                }
      })
      .then((res) => {
            this.prediction = res.data.class_label
            this.waitingForExplanation = false
            if(this.prediction == this.label){
                this.score_ai = this.score_ai + 1
                document.cookie = 'AI=' + this.score_ai + '; Secure'
            } else {
                document.cookie = 'AI=' + this.score_ai + '; Secure'// Explanation und Prediction ID (visual expection backend) + Label + Methode  
            }
      })
      .catch((error) => {
          console.error(error)
        })
      },
    explain() {
      this.waitingForExplanation = true
      const blob = new Blob([this.streetviewimage]);

      let form = new FormData();
      form.append('file', blob );
      
      axios.post(this.backendUrl +'/explain', form,  {
              headers: {
                    'Content-Type': 'multipart/form-data'
                }
      }).then((res) => {
          this.streetviewimage = res.data.image
          this.waitingForExplanation = false
          this.explanation = res.data.explain_id 
      })
        .catch((error) => {
          console.error(error)
        })
    },

    restart() {
        this.explanation = null
        this.prediction = null
        this.user_answer = null
        this.getStreetview()
    },

    answer() {
      var radios = document.getElementsByName('City');

      for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
         this.user_answer = radios[i].value
          break;
        }
      }

      if(this.user_answer == this.label){
       this.score_user = this.score_user + 1
        document.cookie = 'User=' + this.score_user + '; Secure'
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
