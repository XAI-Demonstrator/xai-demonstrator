<template>


  <div class="configurators" align='center'>
    <h3 class="category_headline">Kategorie B</h3>
    <img class="config_picture" src="../assets/25_Stifte.jpg">
    <p style="text-align:center">Anzahl</p>

    <div className=checkboxgroup>
    <!--  <label><input type="radio" v-model="selection_anzahl" value="0">Keine</label> -->
      <div  class=checkboxgroup align="left">
      <label><input type="radio" name="radio" align="left" v-model="selection_anzahl"
                    value=15>
        <span>15</span>
      </label>
      <label><input type="radio" name="radio" v-model="selection_anzahl"
                    value="200" checked="checked">
        <span> 200</span>
      </label>
     </div>

    </div>
    <p style="text-align:center">Label</p>
    <div className=checkboxgroup>
      <label><input type="radio" name="radio" v-model="selection_label" value="Stift">
        <span> Stift</span>
      </label>
      <label><input type="radio" name="radio" v-model="selection_label" value="Tasse">
        <span> Tasse</span>
      </label>
    </div>
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
      selection_anzahl: '0',
      selection_label: 'Handy'
    }
  }
}
</script>

<style scoped>
.configurator_pencil {
  border: 2px solid powderblue;
  color: black;
  width: 140px;
  height: 400px;
  background-color: #F1DEDB;
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