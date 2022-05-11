<template>

    <div class="configurators">
        <h3 class="category_headline">Kategorie C</h3>
        <img class="config_picture" src="../assets/25_Tassen.jpg">
        <p style = "text-align:center">Anzahl</p>

        <div class = checkboxgroup>
      <!--  <label><input type = "radio" v-model="selection_anzahl_cup" value="0">Keine</label> -->
        <label><input type = "radio" name="amount_cup" v-model="selection_amount_cup" value="15" checked="checked">
          <span> 15</span>
        </label>
        <label><input type = "radio" name="amount_cup" v-model="selection_amount_cup" value="200" >
          <span> 200</span>
        </label>
        </div>
        <p style = "text-align:center">Label</p>
        <div class = checkboxgroup>
        <label><input type = "radio" name="data_cup" v-model="selection_label_cup" value="Tasse" checked="checked">
          <span> Tasse</span>
        </label>
        </div>

      <br>
      {{selection_amount_cup}}
      {{selection_label_cup}}


    </div>




</template>

<script>
    export default {
        name: "KISettings",
        components: {
        },
        data(){
            return{
                img: require('../assets/table.jpg'),
                selection_amount_cup: '15',
                selection_label_cup: 'Tasse'
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