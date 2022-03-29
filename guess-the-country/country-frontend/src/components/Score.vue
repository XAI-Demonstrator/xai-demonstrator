<template>
  <div class="wrapper">
 
   <section v-if="(this.explanation && this.round==11 )|| ( this.control && this.prediction_city && this.round==10)" class="left xd-section xd-light">
        <p class="short-text">Now you can finish the game!</p>
    </section>
       <section v-else class="left xd-section xd-light">
        <p>Round: {{round}}/10</p>
  </section>
 <!--   <section class="right row xd-section xd-light">
      <p>Score - You: {{score_user}} AI: {{score_ai}}</p>
  </section> --->
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
      explanation: {
        type: String
      },
      control:{
        type: Boolean
      },
      prediction_city:{
        type: String
      },
}
}
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
