<template>

  <div className="configurator_pencil" align='left'>
    <h2>Kategorie B</h2>
    <p style="text-align:center">Anzahl</p>

    <div className=checkboxgroup>
    <!--  <label><input type="radio" v-model="selection_anzahl" value="0">Keine</label> -->
      <label><input type="radio" v-model="selection_anzahl" value="15">15</label>
      <label><input type="radio" v-model="selection_anzahl" value="200">200</label>
    </div>
    <p style="text-align:center">Label</p>
    <div className=checkboxgroup>
      <label><input type="radio" v-model="selection_label" value="Handy">Stift</label>
      <label><input type="radio" v-model="selection_label" value="Tasse">Tasse</label>
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
  width: 150px;
  height: 400px;
  background-color: #F1DEDB;
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