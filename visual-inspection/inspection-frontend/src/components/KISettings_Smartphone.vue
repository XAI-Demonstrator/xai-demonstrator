<template>
    <div class="configurator_smartphone" align = 'left'>
        <h2>Kategorie A</h2>
        <p style = "text-align:center">Anzahl</p>

        <div class = checkboxgroup>
        <label><input type = "radio" v-model="selection_anzahl" value="0">Keine</label>
        <label><input type = "radio" v-model="selection_anzahl" value="15">15</label>
        <label><input type = "radio" v-model="selection_anzahl" value="200">200</label>
        </div>
        <p style = "text-align:center">Label</p>
        <div class = checkboxgroup>
        <label><input type = "radio" v-model="selection_label" value="Handy">Handy</label>
        <label><input type = "radio" v-model="selection_label" value="Tasse">Tasse</label>
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
  props: ['id'],
  data() {
    return {
      img: require('../assets/table.jpg'),
      selection_amount1: 'Keine',
      selection_amount2: '15',
      selection_amount3: '200',
      selection_label1: 'Handy',
      selection_label2: 'Stift',
      selection_label3: 'Tasse',

      conf: {
        id1: {
          amount: ["0", "15", "200"],
          labels: ["Handy", "Tasse"]
        },
        "id2": {
          "amount": ["15", "200"],
          "labels": ["Stift", "Tasse"]
        },
        data() {
          return {
            img: require('../assets/25_Handys.jpg'),
            selection_anzahl: '0',
            selection_label: 'Handy'
          }
        }
      }
    }
  }
}
</script>

<style scoped>
.configurator_smartphone {
  border: 2px solid powderblue;
  color: black;
  width: 150px;
  height: 400px;
  background-color: #E2E6EC;
}
.image {
    max-height: 100%;
    height: 1%;
    width: 1%;
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