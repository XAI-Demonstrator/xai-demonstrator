<template>
  <div id="app" class="xd-app">
    <GitHubRibbon url="https://github.com/xai-demonstrator/xai-demonstrator"/>
    <XAIStudioRibbon url="https://www.xai-studio.de"/>
    <UseCaseHeader
        v-bind:standalone="!Boolean(backendUrl)"
        v-bind:title="useCaseTitle"/>
    <main>
        <Score :round="round" :label_country="label_country" :score_user = "score_user"  :score_ai = "score_ai"/>
        <Notification :prediction_city="prediction_city" :msg="msg" :label_country="label_country" :label_city="label_city" :user_city_answer="user_city_answer"  :user_country_answer="user_country_answer" :explanation="explanation"/>
        
        <section class="xd-section xd-light">
        <img class="xd-border-secondary;" v-bind:src="this.streetviewimage"/>
        </section>
   
        <Selection @city_selected="city_selected" @country_selected="country_selected" :label_city="label_city" :label_country="label_country" :user_city_answer="user_city_answer" :user_country_answer="user_country_answer" />
        <Explanation_legend :prediction_city="prediction_city" :explanation="explanation"/>


      <button v-if="prediction_city && explanation == null" type="button" class="xd-button xd-secondary" id="explain" v-on:click="explain()"> <!-- v-show --> 
        Explain it to me
      </button>
      <button v-if="explanation" type="button" class="xd-button xd-secondary" id="new" v-on:click="restart()">Start <!-- v-show --> 
        again
      </button>
      <button :disabled="!user_city_answer" v-if="!prediction_city" type="button"  class="xd-button xd-secondary" id="submit" v-on:click="submitFile()">What the AI says
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
import {UseCaseHeader, FloatingInfoButton, SpinningIndicator, XAIStudioRibbon, GitHubRibbon} from '@xai-demonstrator/xaidemo-ui';
import Score from '@/components/Score';
import Notification from '@/components/Notification';
import Selection from '@/components/Selection';
import Explanation_legend from './components/Explanation_legend.vue';

export default {
  name: 'App',
  components: {
    UseCaseHeader,
    FloatingInfoButton,
    SpinningIndicator,
    GitHubRibbon,
    XAIStudioRibbon,
    Score,
    Notification,
    Selection,
    Explanation_legend
  },
  data() {
    return {
        countrys: [
        {
          country: 'Israel',
          citys: [
             {
          city: 'Tel Aviv',
          backend: 'Tel_Aviv'
          },
          {
          city: 'Westjerusalem',
          backend: 'Westjerusalem'
          }
          ]       
          },
        {
          country: 'Germany',
          citys: [
             {
          city: 'Berlin',
          backend: 'Berlin'
        },
        {
          city: 'Hamburg',
          backend: 'Hamburg'
        },
          ]
        },
      ],
      round: 1,
      useCaseTitle: 'Guess the country',
      backendUrl: process.env.VUE_APP_BACKEND_URL,
      explanation: null,
      prediction_country: null,
      prediction_city: null,
      label_city: null,
      label_country: null,
      user_country_answer: null,
      user_city_answer: null,
      score_ai: 0,
      score_user: 0,
      msg: '',
      streetviewimage: null,
      waitingForExplanation: false,
      infoUrl: 'https://xai-demonstrator.github.io/#use-case-ii',
      infoLinkLabel: 'Interesse geweckt? Hier gibt’s mehr Infos!',
      infoText: [
        {
          headline: 'Land erkennen',
          paragraphs: [
            'Du interagierst mit einer KI, die ein Google Streetview Foto einer Stadt zuordnen kann. Aber eine KI ist nie perfekt!',
            'Durch die Wahl verschiedener Bilder entdeckst du, für welche  die KI zuverlässig ist, aber insbesondere auch, wo sie an ihre Grenzen stößt.',
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
    this.getMessage()
    this.getStreetview()
  },
  methods: {
    city_selected(value){
       this.user_city_answer = value;
        if(this.user_city_answer == this.label_city){
         this.score_user = 1 +  this.score_user
      }
    },
    country_selected(value){
      this.user_country_answer = value;
      if(this.user_country_answer == this.label_country){
         this.score_user = 1 +  this.score_user
      }
    },
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
          let label = this.label_to_label(res.data.class_label)
           this.label_country = label.country
           this.label_city = label.city 
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
           let label = this.label_to_label(res.data.class_label)
           this.prediction_country = label.country
           this.prediction_city = label.city 
            this.waitingForExplanation = false
            if(this.prediction_city == this.label_city){
                this.score_ai = this.score_ai + 1
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
          this.explanation = res.data.explanation_id 
      })
        .catch((error) => {
          console.error(error)
        })
    },

    restart() {
        this.explanation = null
        this.prediction_city = null
        this.prediction_country = null
        this.user_city_answer = null
        this.user_country_answer = null
        this.getStreetview()
        this.round = this.round + 1 
        },

    label_to_label(prediction){
      for(let i in this.countrys){
        for(let x in this.countrys[i].citys)
          if(prediction == this.countrys[i].citys[x].backend){
            return {
              country: this.countrys[i].country, 
              city: this.countrys[i].citys[x].city
            }
          }
      }
    }


  }
}

</script>

<style>
#app {
  display: flex;
  justify-content: space-between;
  position: relative;
  overflow: hidden;
}

main {
  display: flex;
  flex-direction: column;
}

@media screen and (max-width: 450px) {
  #app {
    flex-direction: column;
    padding-left: 0;
    padding-right: 0;
  }

}

@media screen and (min-width: 450px) and (max-height: 650px) {
  #app {
    flex-direction: column;
    padding-left: 0;
    padding-right: 0;
    overflow: auto;
    height: 100vh;
    width: 100vw;
  }

  main {
    flex: 2;
    max-height: calc(100vh - 54px);
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    justify-content: flex-start;
    flex-wrap: wrap;
  }

  main section {
    order: 2;

  }
}

@media screen and (min-width: 450px) and (min-height: 650px) {

  #app {
    flex-direction: column;
  }
  main {
    flex-grow: 1;
  }

  main section {
    padding: 0;
  }

}

img {
  width: 100%;

}


</style>
