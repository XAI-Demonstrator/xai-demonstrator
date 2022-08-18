<template>
  <div>
      <section v-show="!explanation" class="xd-section xd-light" >
        <!-- Question -->
        <section v-show="sequence_mode==='classic'&&!user_city_answer
                  || sequence_mode==='recommender'&&!prediction_city
                  || sequence_mode==='basic'&&!user_city_answer">  
          <p v-show= "sequence_mode==='classic'">Your guess: Where has this Google Streetview picture been taken?</p>
          <p v-show= "sequence_mode==='basic'||sequence_mode==='recommender'">Where has this Google Streetview picture been taken?</p>
        </section>   
        <!-- User guess -->
        <section v-show="sequence_mode==='classic'&&user_city_answer && !prediction_city
                  || sequence_mode==='recommender'&&user_city_answer
                  || sequence_mode==='basic' && user_city_answer">  
          <p class="short-text">Your guess is: {{user_city_answer}}</p>
        </section>
        <!-- control group (without explanation), AI guess -->
        <section v-show="sequence_mode==='classic'&&prediction_city && control
                  || sequence_mode==='recommender'&& prediction_city&&!user_city_answer && control"> 
          <p class="short-text">My guess is: {{prediction_city}}</p>
        </section>
        <!-- treatment group (with explanation), AI guess -->
        <section v-show=" sequence_mode ==='classic' && prediction_city && !control
                  || sequence_mode==='recommender' &&prediction_city&&!user_city_answer && !control"> 
          <p>My guess is: {{prediction_city}}
          <br>In particular, the colored areas below have helped me form my guess. </p>
          <p v-show= "sequence_mode==='recommender'">What is your guess?</p>
        </section>
      </section>
  </div>
</template>
<script>
export default {
  name: "Notification",
  props: {
      msg: {
          type: String,
          default: "Hello"
      },
       label_city: {
          type: String
      },
      user_city_answer: {
          type: String
      },
      prediction_city: {
        type: String
      },
      control:{
        type: Boolean
      },
      sequence_mode: {
        type: String
      },
  },

 data() {
    return {
    }
 }
}
</script>
<style scoped>
.xd-section:last-child{
    text-align: center;
    margin-bottom: 12px;
}
.short-text{
  line-height: 2;
}

</style>
