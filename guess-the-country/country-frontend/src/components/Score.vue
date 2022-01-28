<template>
  <div class="wrapper">
    <section class="left xd-section xd-light">
        <p>Round: {{round}}</p>
  </section>
    <section class="right row xd-section xd-light">
      <p>Score - You: {{score_user}} AI: {{score_ai}}</p>
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
      }
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
    flex: 2; 
}

.wrapper>.right{
 text-align: center;
 flex: 8;

}

.xd-section:last-child{
    margin-bottom: 12px;
}
</style>
