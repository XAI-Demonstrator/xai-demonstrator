<template>
  <div class="wrapper">    
   <section  class="left xd-section xd-light">
        <p v-if="round<=nr_of_rounds"> Round: {{round}}/{{nr_of_rounds}} </p>
        <h1 v-else-if="relativeScore>=0.8"> {{String.fromCodePoint(0x1F913)}} {{score_user}} - {{score_ai}} {{String.fromCodePoint(0x1F916)}} </h1>
        <h1 v-else-if="relativeScore>=0.4"> {{String.fromCodePoint(0x1FAE0)}} {{score_user}} - {{score_ai}} {{String.fromCodePoint(0x1F916)}} </h1>
        <h1 v-else> Final Scores: {{String.fromCodePoint(0x1F61E)}} {{score_user}} - {{score_ai}} {{String.fromCodePoint(0x1F916)}} </h1>
   </section>   
  </div>
</template>

<script>
export default {
  name: "Score",
  props: {
      score_user: {
          type: Number,
      },
    score_ai: {
          type: Number,
      },
      round: {
        type: Number,
      },
 user_city_answer: {
   type: String
 },
  nr_of_rounds: {
        type: Number
  }
 },
  computed: {
    relativeScore () {
      return this.score_user / this.nr_of_rounds
    }
  }
};
</script>
<style scoped>

.wrapper {
  display: flex;
  flex-direction: row;
  align-items: stretch;
  width: 100%;
  gap:10px;
}

.wrapper>.left {
  text-align: center;
    flex: 4; 
}

.wrapper>.right{
 text-align: center;
 flex: 6;

}

.xd-section:last-child{
    margin-bottom: 12px;
}
</style>
