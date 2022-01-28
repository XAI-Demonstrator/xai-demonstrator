<template>
  <div>
      <section  v-if="explanation" 
               class="xd-section xd-light" id="legend">
        <ul class="legend">
          <li><span class="positiv"></span> {{ prediction_city }}</li>
          <li><span class="negativ"></span> Other classes </li>
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
  background-color: #63fe45;
}

</style>