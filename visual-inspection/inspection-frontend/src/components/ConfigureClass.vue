<template>
  <div class="configurators">
    <h3 class="category_headline">{{ $t('category') + ' ' + className }}</h3>
<!--    <img v-bind:alt="className" class="config_picture" :src="require(`@/assets/${image}`)">-->
    <p style="text-align:center">{{ $t('amount') }}</p>

    <div class=checkboxgroup>

      <label v-for="(amount, index) in amounts" v-bind:key="amount">
        <input type="radio"
               v-bind:value="amount"
               v-model="modelConfig[classKey].amount"
               v-bind:name="'amounts-' + classKey + '-' + index">
        {{ amount }} </label>
    </div>

    <p style="text-align:center">{{ $t('label') }}</p>
    <div class=checkboxgroup>
      <label v-for="(label, index) in labels" v-bind:key="label">
        <input type="radio"
               v-model="modelConfig[classKey].label"
               v-bind:name="'labels-'  + classKey + '-' + index"
               v-bind:value="label">
        {{ $t(label) }}</label>
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
/*.configurator_cup {*/
/*  border: 2px solid powderblue;*/
/*  color: black;*/
/*  width: 140px;*/
/*  height: 400px;*/
/*  background-color: #EFFBF8;*/
/*  border-radius: 10px;*/
/*}*/

/*.image {*/
/*  max-height: 100%;*/
/*  height: 100%;*/
/*  width: 100%;*/
/*  align-self: flex-start;*/
/*  order: 1;*/
/*  justify-content: center;*/
/*  align-items: flex-start;*/
/*}*/

/*.checkboxgroup {*/
/*  display: inline-block;*/
/*  text-align: left;*/
/*}*/

/*.checkboxgroup label {*/
/*  display: block;*/
/*}*/

/*.configurator-menu {*/
/*  display: flex;*/
/*}*/

/*.configurators {*/
/*  margin: 5px;*/
/*  border-radius: 25px;*/
/*  width: 140px;*/
/*  height: 400px;*/
/*  text-align: left;*/
/*}*/

/*.category_headline {*/
/*  text-align: center;*/
/*}*/

/*.config_picture {*/
/*  width: 135px;*/
/*  float: left;*/
/*  margin-top: 6px;*/
/*  margin-bottom: 6px;*/
/*}*/

/*#smartphone_config {*/
/*  background-color: #E2E6EC;*/
/*  box-shadow: #E2E6EC 2px 2px;*/
/*}*/

/*#pencil_config {*/
/*  background-color: #F1DEDB;*/
/*  box-shadow: #F1DEDB 2px 2px;*/
/*}*/

/*#cup_config {*/
/*  background-color: #EFFBF8;*/
/*  box-shadow: #EFFBF8 2px 2px;*/
/*}*/

/*!*The following Code is for getting Radio-Buttons with a square design*/
/*  instead of the old-school Radio-Buttons. It is based on the following StackOverflow-Thread;*/
/*  https://stackoverflow.com/questions/24516958/styling-radio-buttons-into-a-square*!*/
/*input {*/
/*  display: none;*/
/*}*/

/*label {*/
/*  display: inline-block;*/
/*  padding: 5px 10px;*/
/*  cursor: pointer;*/
/*}*/

/*label span {*/
/*  position: relative;*/
/*  line-height: 22px;*/
/*}*/

/*label span:before,*/
/*label span:after {*/
/*  content: '';*/
/*}*/


/*label span:before {*/
/*  border: 1px solid #222021;*/
/*  width: 20px;*/
/*  height: 20px;*/
/*  margin-right: 10px;*/
/*  display: inline-block;*/
/*  vertical-align: top;*/
/*}*/

/*label span:after {*/
/*  background: #222021;*/
/*  width: 14px;*/
/*  height: 14px;*/
/*  position: absolute;*/
/*  top: 2px;*/
/*  left: 4px;*/
/*  transition: 300ms;*/
/*  opacity: 0;*/
/*}*/

/*label input:checked + span:after {*/
/*  opacity: 1;*/
/*}*/
</style>