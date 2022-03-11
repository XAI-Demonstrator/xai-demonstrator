<template>
  <div>
      <section  v-if="explanation" 
               class="xd-section xd-light" id="legend">
        <ul class="legend">
          <li><span class="positiv"></span> Pixels that significantly determine the AI’s guess:</li>
          <li>{{ prediction_city }}</li>
        </ul>
      </section>
    </div>
</template>
<script>
export default {
  name: "Explanation_legend",
  props: {
      prediction_city: { 
          type: String,
      },
      explanation: {
      
      }
  },
 data() {
    return {
    }
 }
}
</script>
<style scoped>
.xd-section:last-child{
    margin-bottom: 12px;
}
.legend {
  list-style: none;
}

.legend span {
  border: 1px solid #ccc;
  float: left;
  width: 12px;
  height: 12px;
  margin: 2px;
}

.legend .negativ {
  background-color: #fe5e55;
}

.legend .positiv {
  background-color: rgb(215, 102, 255);
}

</style>