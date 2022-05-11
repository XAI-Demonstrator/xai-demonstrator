<template>
  <div  class="configurators">
    <h3 class="category_headline">Kategorie A</h3>
    <img align="left" class="config_picture" src="../assets/25_Handys.jpg">
    <p style="text-align:center">Anzahl</p>

    <div class=checkboxgroup align="left">
      <label><input type="radio" name="amount_smartphone" align="left" v-model="selection_amount_smartphone"
                    value="0" checked="checked">
        <span> 0 </span>
      </label>
      <label><input type="radio" name="amount_smartphone" v-model="selection_amount_smartphone"
                    value="15">
        <span> 15 </span>
      </label>
      <label><input type="radio" name="amount_smartphone" v-model="selection_amount_smartphone"
                    value="200">
        <span> 200 </span>
      </label>
     </div>




    <p style="text-align:center">Label</p>
    <div class=checkboxgroup>
      <label><input type="radio" name="data_smartphone" v-model="selection_label_smartphone" value="Handy" checked="checked">
        <span> Handy</span>
      </label>
      <label><input type="radio" name="data_smartphone" v-model="selection_label_smartphone" value="Tasse">
        <span> Tasse </span>
      </label>
    </div>


    <br>
    {{selection_amount_smartphone}}
    {{selection_label_smartphone}}

    <!--
    <div class="image">

        <img v-bind:src="img" alt = "Alt Text" >
    </div>
    -->
  </div>


</template>

<script>
export default {
  name: "KISettings",
  components: {},
  data() {
    return {
      img: require('../assets/table.jpg'),
      selection_amount_smartphone: '0',
      selection_label_smartphone: 'Handy',

    }
  }
}

</script>

<style scoped>
.configurator_smartphone {
  border: 2px solid powderblue;
  color: black;
  width: 140px;
  height: 400px;
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