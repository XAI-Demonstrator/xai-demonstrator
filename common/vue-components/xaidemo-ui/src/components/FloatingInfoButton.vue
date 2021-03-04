<template>
  <div id="info-button">
    <transition name="slide">
      <div id="info-popup" class="popup" v-if="popupVisible">
        <div id="info-content">
          <section v-for="part in infoText" v-bind:key="part.header" class="xd-section xd-light">
            <h3>{{ part.headline }}</h3>
            <p v-for="paragraph in part.paragraphs" v-bind:key="paragraph" v-html="paragraph"></p>
          </section>
          <a v-if="infoUrl" v-bind:href="infoUrl" class="xd-button xd-secondary xd-section">
            {{ linkLabel }}
          </a>
        </div>
      </div>
    </transition>
    <div id="icon-container">
      <transition name="fade" mode="out-in">
        <div class="icon xd-red" v-if="popupVisible" v-on:click="closePopup" key="close">
          <img svg-inline src="../assets/close.svg" alt="Close"/>
        </div>
        <div class="icon xd-primary" v-else v-on:click="openPopup" key="open">
          <img svg-inline src="../assets/info.svg" alt="Info"/>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: "FloatingInfoButton",
  props: {
    infoText: {
      type: Array,
      default: function () {
        return [
          {
            headline: "Headline 1",
            paragraphs:
                ["Some general information... With more lines, and many, many more.",
                  "We can also have another paragraph if needed."]
          },
          {
            headline: "Headline 2",
            paragraphs: [
              "More detailed stuff.",
              "Some stuff <a href='/'>with links</a>."
            ]
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
  min-height: 70px;
  flex-grow: 0;
}

#info-popup {
  margin-top: 42px;
  padding: 12px 8px 8px;
  height: calc(100% - 42px);
  width: 100%;
  background-color: #fff;
  box-shadow: inset 0 4px 12px rgba(120, 120, 120, 0.4);
}

.popup {
  top: 0;
  right: 0;
  bottom: auto;
  left: auto;
  position: fixed;
  transition: .3s ease-out;
  z-index: 99;
}

.slide-enter,
.slide-leave-active {
  transform: translate3d(100%, 0, 0);
}

#info-content {
  display: flex;
  align-items: center;
  flex-direction: column;
  max-height: 100%;
  overflow: scroll;
  padding-bottom: 70px;
}

#info-content section p {
  font-size: 0.9em;
  text-align: justify;
}

#icon-container {
  position: fixed;
  bottom: 8px;
  right: 8px;
  z-index: 9999;
}

.icon {
  width: 50px;
  height: 50px;
  border-radius: 100%;

  box-shadow: 2px 4px 8px rgba(120, 120, 120, 0.4);
  z-index: 9999;

  display: flex;
  align-items: center;
  justify-content: center;
}

.icon svg {
  height: 55%;
  width: 55%;
}

.icon span {
  display: flex;
  align-items: center;
  justify-content: center;

  height: 100%;
  font-size: 25px;
  color: #EBEBEB;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

@media screen and (min-width: 450px) and (min-height: 650px) {

  #info-popup {
    max-width: 432px;
    top: calc(50% - 310px + 42px + 12px);
    right: auto;
    left: auto;
    bottom: auto;
    box-shadow: none;
    height: calc(624px - 42px - 12px);
    overflow: hidden;
    padding: 0;
    margin: 0;
  }

  .slide-enter-active,
  .slide-leave-active {
    transform: none;
    transition: opacity 0.6s ease-out;
  }

  .slide-enter,
  .slide-leave-to {
    transform: none;
    opacity: 0;
  }

  #info-content {
    padding: 0 4px 4px;
    overflow: auto;
  }

  #icon-container {
    position: inherit;
    min-height: 70px;
    margin: 0;
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
  }
}

</style>