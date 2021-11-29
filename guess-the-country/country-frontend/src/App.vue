<template>
  <div id="app" class="xd-app">
    <UseCaseHeader title="XAI Streetview" v-bind:standalone="true" />
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
    </main>
    <SpinningIndicator class="indicator" v-bind:visible="waitingForExplanation"/>
    <FloatingInfoButton
      v-bind:info-text="infoText"
      v-bind:info-url="infoUrl"
      v-bind:link-label="linkLabel"/>
    <SpinningIndicator/>

    <NotificationGroup group="foo">
      <div class="fixed inset-0 flex items-start justify-end p-6 px-4 py-6 pointer-events-none">
        <div class="w-full max-w-sm">
          <Notification
            v-slot="{ notifications, close }"
            enter="transform ease-out duration-300 transition"
            enter-from="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
            enter-to="translate-y-0 opacity-100 sm:translate-x-0"
            leave="transition ease-in duration-500"
            leave-from="opacity-100"
            leave-to="opacity-0"
            move="transition duration-500"
            move-delay="delay-300"
          >
            <div
              class="w-full max-w-sm mt-4 overflow-hidden bg-white rounded-lg shadow-lg pointer-events-auto ring-1 ring-black ring-opacity-5"
              v-for="notification in notifications"
              :key="notification.id"
            >
              <div class="p-4">
                <div class="flex items-start">
                  <div class="flex-shrink-0">
                    <svg class="w-6 h-6 text-green-400" xmlns="http://www.w3.org/2000/svg" fill="none"
                         viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                  </div>
                  <div class="ml-3 w-0 flex-1 pt-0.5">
                    <p class="font-semibold text-gray-800">{{ notification.title }}</p>
                    <p class="text-sm font-semibold text-gray-500">{{ notification.text }}</p>
                  </div>
                  <div class="flex flex-shrink-0 ml-4">
                    <button @click="close(notification.id)"
                            class="inline-flex text-gray-400 bg-white rounded-md hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-400">
                      <span class="sr-only">Close</span>
                      <svg class="w-5 h-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor"
                           aria-hidden="true">
                        <path fill-rule="evenodd"
                              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                              clip-rule="evenodd"/>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </Notification>
        </div>
      </div>
    </NotificationGroup>

    <NotificationGroup group="bottom">
      <div class="fixed inset-x-0 bottom-0 flex items-start justify-end p-6 px-4 py-6 pointer-events-none">
        <div class="w-full max-w-sm">
          <Notification
            v-slot="{ notifications }"
            enter="transform ease-out duration-300 transition"
            enter-from="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-4"
            enter-to="translate-y-0 opacity-100 sm:translate-x-0"
            leave="transition ease-in duration-500"
            leave-from="opacity-100"
            leave-to="opacity-0"
            move="transition duration-500"
            move-delay="delay-300"
          >
            <div
              class="flex w-full max-w-sm mx-auto mt-4 overflow-hidden bg-white rounded-lg shadow-md"
              v-for="notification in notifications"
              :key="notification.id"
            >
              <div class="flex items-center justify-center w-12 bg-red-500">
                <svg class="w-6 h-6 text-white fill-current" viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg">
                  <path
                    d="M20 3.36667C10.8167 3.36667 3.3667 10.8167 3.3667 20C3.3667 29.1833 10.8167 36.6333 20 36.6333C29.1834 36.6333 36.6334 29.1833 36.6334 20C36.6334 10.8167 29.1834 3.36667 20 3.36667ZM19.1334 33.3333V22.9H13.3334L21.6667 6.66667V17.1H27.25L19.1334 33.3333Z"
                  ></path>
                </svg>
              </div>

              <div class="px-4 py-2 -mx-3">
                <div class="mx-3">
                  <span class="font-semibold text-red-500">{{ notification.title }}</span>
                  <p class="text-sm text-gray-600">{{ notification.text }}</p>
                </div>
              </div>
            </div>
          </Notification>
        </div>
      </div>
    </NotificationGroup>

  </div>
</template>

<script>
import {notify} from 'notiwind'
import axios from 'axios'
import UseCaseHeader from '@xai-demonstrator/xaidemo-ui'
import FloatingInfoButton from '@xai-demonstrator/xaidemo-ui'
import SpinningIndicator from '@xai-demonstrator/xaidemo-ui'

export default {
  name: 'App',
  components: {
    UseCaseHeader,
    FloatingInfoButton,
    SpinningIndicator
  },
  data () {
    return {
      prediction: 'Israel',
      other: 'Germany',
      score_ai: 0,
      score_user: 0,
      tasks: [],
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
  async created () {
    if (document.cookie == '') {
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
    getMessage () {
      axios.get('/msg')
        .then((res) => {
          this.msg = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getStreetview () {
      axios.get('/streetview')
        .then((res) => {
          this.url = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
    submitFile () {
      var result
      this.waitingForExplanation = true
      if (this.url.search('Israel') == -1) {
        result = 'Berlin'
      } else {
        result = 'Tel-Aviv'
      }
      // const config = { headers: {'Content-Type': 'application/json'} };
      axios.post('/predict/image3/?url=' + this.url).then((res) => {
        this.prediction = res.data[0]
        if (result == res.data[0]) {
          this.score_ai = parseInt(document.cookie.split('; ')
            .find(row => row.startsWith('AI='))
            .split('=')[1])
          this.score_ai = this.score_ai + 1

          document.cookie = 'AI=' + this.score_ai + '; Secure'
          console.log(document.cookie)
          notify({
            group: 'foo',
            title: 'Success',
            text: 'The AI predicted: ' + res.data[0] + ' and it was actually taken in ' + result
          }, 5000)
        } else {
          notify({
            group: 'bottom',
            title: 'Wrong',
            text: 'The AI predicted: ' + res.data[0] + ' and it was actually taken in ' + result
          }, 5000)
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
    explain () {
      this.waitingForExplanation = true
      axios.post('/predict/explain2/?url=' + this.url).then((res) => {
        this.url = res.data

        if (this.prediction == 'Tel-Aviv') {
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
    restart () {
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

    answer () {
      var answer
      if (document.getElementById('Tel-Aviv').checked == true) {
        answer = 'Tel-Aviv'
      } else {
        answer = 'Berlin'
      }

      var result
      if (this.url.search('Israel') == -1) {
        result = 'Berlin'
      } else {
        result = 'Tel-Aviv'
      }
      if (result == answer) {
        this.score_user = parseInt(document.cookie.split('; ')
          .find(row => row.startsWith('User='))
          .split('=')[1])
        this.score_user = this.score_user + 1
        document.cookie = 'User=' + this.score_user + '; Secure'
        console.log(document.cookie)
        notify({
          group: 'foo',
          title: 'Success',
          text: 'The picture was taken in ' + result
        }, 3000)
      } else {
        notify({
          group: 'bottom',
          title: 'Wrong',
          text: 'The picture was taken in ' + result
        }, 3000)
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
