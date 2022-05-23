<template>
  <div class="main xd-section xd-light">
    <h3>{{ $t('category') + ' ' + className }}</h3>

    <div class="configuration">
      <div class="image">
        <img v-bind:alt="className" class="config_picture" :src="require(`@/assets/${image}`)">
      </div>

      <div class="options">

        <div class="group">
          <strong> {{ $t('amount') }}</strong>
          <label v-for="(amount, index) in amounts" v-bind:key="amount">
            <input type="radio"
                   v-bind:value="amount"
                   v-model="modelConfig[classKey].amount"
                   v-bind:name="'amounts-' + classKey + '-' + index">
            <span>{{ amount }}</span> </label>
        </div>

        <div class="group">
          <strong> {{ $t('label') }}</strong>
          <label v-for="(label, index) in labels" v-bind:key="label">
            <input type="radio"
                   v-model="modelConfig[classKey].label"
                   v-bind:name="'labels-'  + classKey + '-' + index"
                   v-bind:value="label">
            <span>{{ $t(label) }}</span></label>
        </div>

      </div>

    </div>
  </div>
</template>

<script>
import {modelConfig} from '@/modelConfig.js'

export default {
  name: "ConfigureClass",
  props: {
    amounts: {
      type: Array
    },
    labels: {
      type: Array
    },
    image: {
      type: String,
    },
    className: {
      type: String
    },
    classKey: {
      type: String
    }
  },
  data() {
    return {
      modelConfig: modelConfig
    }
  }
}
</script>

<i18n>
{
  "de": {
    "category": "Kategorie",
    "amount": "Anzahl",
    "label": "Label",
    "smartphone": "Handy",
    "pencil": "Stift",
    "cup": "Tasse"
  },
  "en": {
    "category": "Category",
    "amount": "Number of samples",
    "label": "Label",
    "smartphone": "Phone",
    "pencil": "Pencil",
    "cup": "Cup"
  }
}
</i18n>

<style scoped>
.main {
  display: flex;
  flex-direction: column;
  margin: 0;
}

.main h3 {
  margin-bottom: 4px;
}

.configuration {
  display: flex;
  flex-direction: row;
}

.image {
  width: 50%;
}

.image img {
  max-width: 200px;
}

.options {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  margin-left: 12px;
}

.group {
  display: flex;
  flex-direction: column;
}

@media screen and (max-width: 450px) {
  .main {
    margin-bottom: 12px;
  }

  .configuration {
    justify-content: left;
  }

  .image img {
    max-width: 150px;
  }

}

@media screen and (min-width: 450px) and (max-height: 650px) {
  .main {
    margin-right: 8px;
    max-width: 100vw;
    width: 300px;
  }

  .image img {
    width: 100%;
    max-height: 150px;
  }

  .configuration {
    height: 100%;
  }
}

@media screen and (min-width: 450px) and (min-height: 650px) {
  .main {
    margin-bottom: 8px;
  }

  .configuration {
    justify-content: left;
  }

}

/*  https://stackoverflow.com/questions/24516958/styling-radio-buttons-into-a-square* */
input {
  display: none;
}

label {
  display: inline-block;
  padding: 5px 10px;
  cursor: pointer;
}

label span {
  position: relative;
}

label span:before,
label span:after {
  content: '';
}

label span:before {
  border: 1px solid #323232;
  border-radius: 3px;
  width: 20px;
  height: 20px;
  margin-right: 8px;
  display: inline-block;
  vertical-align: top;
}

label span:after {
  background: #323232;
  border-radius: 3px;
  width: 22px;
  height: 22px;
  position: absolute;
  top: 0;
  left: 0;
  transition: 300ms;
  opacity: 0;
}

label input:checked + span:after {
  opacity: 1;
}
</style>