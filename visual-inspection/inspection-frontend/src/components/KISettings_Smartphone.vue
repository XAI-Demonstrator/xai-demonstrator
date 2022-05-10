<template>
  <div  class="configurators">
    <h3 class="category_headline">Kategorie A</h3>
    <img align="left" class="config_picture" src="../assets/25_Handys.jpg">
    <p style="text-align:center">Anzahl</p>

    <div v-if="id === 'id1'" class=checkboxgroup align="left">
      <label><input type="radio" name="radio" align="left" v-model="selection_amount1"
                    value=this.conf[id][amount][0] checked="checked">
        <span> {{ conf[id]["amount"][0] }}</span>
      </label>
      <label><input type="radio" name="radio" v-model="selection_amount1"
                    value="conf[id][amount][1]">
        <span> {{ conf[id]["amount"][1] }}</span>
      </label>
      <label><input type="radio" name="radio" v-model="selection_amount1"
                    value="conf[id][amount][2]">
        <span> {{ conf[id]["amount"][2] }}</span>
      </label>
     </div>

    <div v-if="id === 'id2'" class=checkboxgroup>
      <label><input type="radio" name="radio" v-model="selection_amount2"
                    value="conf[id][amount][0]" checked="checked">
        <span> {{ conf[id]["amount"][0] }}</span>
      </label>
      <label><input type="radio" name="radio" v-model="selection_amount2"
                    value="conf[id][amount][1]">
        <span> {{ conf[id]["amount"][1] }}</span>
      </label>
    </div>

    <div v-if="id === 'id3'" class=checkboxgroup>
      <label><input type="radio" v-model="selection_amount3"
                    value="conf[id][amount][0]" checked="checked">{{ conf[id]["amount"][0] }}</label>
      <label><input type="radio" v-model="selection_amount3"
                    value="conf[id][amount][1]">{{ conf[id]["amount"][1] }}</label>
    </div>


    <p style="text-align:center">Label</p>
    <div v-if="id === 'id1'" class=checkboxgroup>
      <label><input type="radio" v-model="selection_label1" value="conf[id][labels][0]" checked="checked">
        <span> {{conf[id]["labels"][0]}}</span>
      </label>
      <label><input type="radio" v-model="selection_label1" value="conf[id][labels][1]">
        <span>{{conf[id]["labels"][1]}}</span>
      </label>
    </div>

    <div v-if="id === 'id2'" class=checkboxgroup>
      <label><input type="radio" v-model="selection_label2" value='conf[id][labels][0]' checked="checked">{{conf[id]["labels"][0]}}</label>
      <label><input type="radio" v-model="selection_label2" value='conf[id][labels][1]'>{{conf[id]["labels"][1]}}</label>
    </div>

    <div v-if="id === 'id3'" class=checkboxgroup>
      <label><input type="radio" v-model="selection_label3" value="conf[id][labels][0]" checked="checked">{{conf[id]["labels"][0]}}</label>
    </div>
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
  width: 140px;
  height: 400px;
  border-radius: 10px;

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