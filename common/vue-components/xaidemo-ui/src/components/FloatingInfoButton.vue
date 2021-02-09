<template>
  <div id="info-button">
    <mt-popup class="info-popup" position="right" v-model="popupVisible" v-bind:modal="false">
      <div class="info-content">
        <section v-for="part in infoText" v-bind:key="part.header">
          <h3>{{ part.headline }}</h3>
          <p>{{ part.text }}</p>
        </section>
        <a v-if="infoUrl" v-bind:href="infoUrl" class="button">
          {{ linkLabel }}
        </a>
      </div>
      <div class="icon-container">
        <div class="icon close" v-on:click="closePopup">
          <span>X</span>
        </div>
      </div>
    </mt-popup>
    <div class="icon-container">
      <div class="icon open" v-on:click="openPopup">
        <span>?</span>
      </div>
    </div>
  </div>
</template>

<script>
import {Popup} from 'mint-ui';

export default {
  name: "FloatingInfoButton",
  components: [
    Popup
  ],
  props: {
    infoText: {
      type: Array,
      default: function () {
        return [
          {
            headline: "Headline 1",
            text: "Some general information... With more lines, but never with another paragraph."
          },
          {
            headline: "Headline 2",
            text: "More detailed stuff"
          }
        ]
      }
    },
    infoUrl: {
      type: String,
      default: "/"
    },
    linkLabel: {
      type: String,
      default: "Learn more!"
    }
  },
  data: function () {
    return {
      popupVisible: false
    }
  },
  methods: {
    openPopup() {
      this.popupVisible = true;
    },
    closePopup() {
      this.popupVisible = false;
    }
  }
}
</script>

<style scoped>
#info-button {
  min-height: 65px;
}

.info-popup {
  margin-top: 20px;
  height: calc(100% - 40px);
  width: 100%;
  background-color: #eee;
  padding: 10px;
}

.info-content {
  display: flex;
  align-items: flex-start;
  flex-direction: column;
  max-height: 100%;
  overflow: scroll;
}

.info-content section {
  width: 100%;
  margin-bottom: 10px;
  padding: 15px 10px;
  background-color: #D3E3FC;
  border-radius: 5px;
  box-shadow: 2px 2px 5px 0 #eee;
}

.info-content section h3 {
  margin: 0;
  padding: 0;
  font-size: 1em;
  font-weight: 600;
}

.info-content section p {
  margin: 0;
  font-size: 0.8em;
  padding: 5px 0 0;
  text-align: justify;
}

.info-content a.button {
  width: 100%;
  background-color: #00887A;
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  border-radius: 5px;
}

.icon-container {
  position: fixed;
  bottom: 15px;
  right: 15px;
  z-index: 99;
}

.icon {
  width: 50px;
  height: 50px;
  border-radius: 100%;

  box-shadow: 0 4px 8px #ccc;
}

.open {
  background-color: #77A6F7;
}

.close {
  background-color: darkred;
}

.icon span {
  display: flex;
  align-items: center;
  justify-content: center;

  height: 100%;
  font-size: 25px;
  color: #ffffff;
}
</style>