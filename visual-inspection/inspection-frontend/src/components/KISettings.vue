<template>

    <div class="configurators">
        <h3 class="category_headline">{{header}}</h3>
        <img class="config_picture" :src="require(`@/assets/${pic_filename}`)">
        <p style = "text-align:center">Anzahl</p>

        <div class = checkboxgroup>
 
        <label v-for="(amount, index) in amounts" v-bind:key="amount"> <input type = "radio"
                                                                              v-bind:name="name_radio_amount"
                                                                              v-model="selection_amount"
                                                                              v-bind:value="amount"
                                                                              v-bind:checked="index === 0">
          <span> {{amount}}</span></label>
        </div>

        <p style = "text-align:center">Label</p>
        <div class = checkboxgroup>

        <label v-for="(label, index) in labels" v-bind:key="label"> <input type = "radio"
                                                                           v-bind:name="name_radio_label"
                                                                           v-model="selection_label"
                                                                           v-bind:value="label"
                                                                           v-bind:checked="index === 0">
          <span> {{label}}</span></label>
        </div>

      <br>
      {{selection_amount}}
      {{selection_label}}


    </div>




</template>

<script>
    export default {
        name: "KISettings",
        props: {
            amounts: {
              type: Array,
              default:()=> ['0', '15', '200'],
            },
            labels: {
              type: Array, 
              default:()=> ['Handy', 'Tasse', 'Smartphone']
            },
          header: {
              type: String,
              default: 'Kategorie A'
          },
          pic_filename: {
              type: String,
              default: "25_Handys.jpg"
          },
          name_radio_amount: {
              type:String,
              default: 'smartphone_amount'
          },
          name_radio_label: {
              type:String,
              default: 'smartphone_label'
          }
        },
        components: {
        },
        data(){
            return{
                selection_amount: '0',
                selection_label: 'Tasse',
            }
        }
    }
</script>

<style scoped>
.configurator_cup {
  border: 2px solid powderblue;
  color: black;
  width: 140px;
  height: 400px;
  background-color: #EFFBF8;
  border-radius: 10px;
}
.image {
    max-height: 100%;
    height: 100%;
    width: 100%;
    align-self: flex-start;
    order: 1;
    justify-content: center;
    align-items: flex-start;
}
.checkboxgroup {
  display: inline-block;
  text-align: left;
}
.checkboxgroup label {
  display: block;
}
</style>